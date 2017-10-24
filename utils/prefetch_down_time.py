import os
import sys
import time
import hashlib
import urllib2
import itertools
import threading
import multiprocessing
import cPickle as pickle
import multiprocessing.pool
from itertools import chain
from datetime import datetime as dt
from swift.common.swob import Response
from sys import argv, getsizeof, stderr
from collections import deque, OrderedDict
from swift.common.internal_client import InternalClient
from swiftclient.service import SwiftService, SwiftError


TOTALSECONDS = 60 #allowed time diff in seconds between previous and next object
PROB_THRESHOLD = 0.5 #minimum probability to be prefetched
N_THREADS = 5 #number of threads in the download threadpool
AUTOSAVE = 300 #autosave chain each X seconds
MAX_PREFETCHED_SIZE =  1073741824 #1Gb of prefetched object
CHAINSAVE = '/tmp/chain.p'
PROXY_PATH = '/etc/swift/proxy-server.conf'

acc_status= [200]

prefetched_objects = OrderedDict()

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):  # @NoSelf
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
 
def download(oid, acc, container, name, u_agent, token, delay=0, request_tries=5):
    print 'Prefetching object with InternalClient: ' + oid + ' after ' + str(delay) + ' seconds of delay.'
    time.sleep(delay) 
    start_time = dt.now()
    swift = InternalClient(PROXY_PATH, u_agent, request_tries=request_tries)
    headers = {}
    headers['X-Auth-Token'] = token
    headers['X-No-Prefetch'] = 'True'
    status, head, it = swift.get_object(acc, container, name, headers, acc_status)
    data = [el for el in it]
    end_time = dt.now()
    diff = end_time - start_time
    return (oid, data, head, diff)
    

class JITPrefetching(object):
    
    __metaclass__ = Singleton
    
    def __init__(self, global_conf, filter_conf, logger):
        self.logger = logger
        self.chain = Chain(logger)
        #self.chain.auto_save(AUTOSAVE)
        self.pool = NoDaemonPool(processes=N_THREADS)
        
    def execute(self, req_resp, app_iter, requests_data):
        
        method = requests_data['method']
        if 'HTTP_X_NO_PREFETCH' not in req_resp.environ:
            if method.upper() == 'GET':
                self.chain.load_chain()
                print "BSC: filter prefetch GET Method"
                object_path = req_resp.environ['PATH_INFO']
                oid = (hashlib.md5(object_path).hexdigest())
                print 'BSC: Prefetched ' + str(len(prefetched_objects)) + ' objects with total size ' + str(total_size(prefetched_objects))
                data = self.get_prefetched(oid)
                self.add_object_to_chain(oid, requests_data)
                self.prefetch_objects(oid, req_resp)

                if data:
                    req_resp.response_headers ={}
                    req_resp.response_headers['X-object-prefetched'] = 'True'
                    return iter(data)

        return req_resp.environ['wsgi.input']

    def get_prefetched(self, oid):
        if oid in prefetched_objects:
            data, resp_headers = prefetched_objects[oid]
            print 'BSC prefetch Filter - Object '+oid+' in cache'              

            return data
        return False
        
    def prefetch_objects(self, oid, req_resp):
        objs = self.chain.get_probabilities(oid)
        for oid, o in objs:
            print o.object_to_string()
        token = req_resp.environ['HTTP_X_AUTH_TOKEN']
        acc = 'AUTH_' + req_resp.environ['HTTP_X_TENANT_ID']
        user_agent =  req_resp.environ['HTTP_USER_AGENT']
        path = req_resp.environ['PATH_INFO']
        server_add = req_resp.environ['REMOTE_ADDR']
        server_port = req_resp.environ['SERVER_PORT']
        
        for oid, obj in objs:
            if oid not in prefetched_objects:
                self.pool.apply_async(download, args=(oid, acc, obj.container, obj.name, user_agent, token, obj.time_stamp, ), callback=self.log_result)

    def log_result(self, result):
        oid, data, headers, down_time = result
        if data:
            while total_size(prefetched_objects) > MAX_PREFETCHED_SIZE:
                prefetched_objects.popitem(last=True)
            self.chain.add_down_time(oid, down_time)
            prefetched_objects[oid] = (data, headers)
            print 'Object ' + oid + ' downloaded in ' + str(down_time.total_seconds()) + ' seconds.'



    def add_object_to_chain(self, oid, requests_data):
        container = requests_data['container']
        object_name = requests_data['object']
        self.chain.add(oid, object_name, container)
        self.chain.save_chain()
        self.chain.chain_stats()
        

class Chain():

    def __init__(self, logger=''):
        print "Init Chain"
        self.logger = logger     
        self._chain = {}
        self._last_oid = None
        self._last_ts = None

    def __del__(self):
        with open(CHAINSAVE, 'wb') as fp:
            pickle.dump(self._chain, fp)

    def load_chain(self):
        try:
            with open(CHAINSAVE, 'rb') as fp:
                self._chain = pickle.load(fp)
        except: 
            pass

    def save_chain(self):
        with open(CHAINSAVE, 'wb') as fp:
            pickle.dump(self._chain, fp)

    def auto_save(self, timer=300):
        threading.Timer(timer, self.auto_save).start()

    def add_down_time(self, oid, ts):
        for o in self._chain:
            objs = self._get_object_chain(o)
            for obj in filter(lambda x: x.id()==oid, objs):
                obj.add_down_time(ts)

    def _get_object_chain(self, oid):
        if oid in self._chain:
            return sorted(self._chain[oid], key=lambda x: x.hits, reverse=True)
        return []

    def _set_object_chain(self, oid, objs_list):
        self._chain[oid] = objs_list

    def add(self, oid, name, container):
        if oid not in self._chain:
            self._chain[oid] = []
    
        diff = self._check_time_diff()
        if diff:
            objs = self._get_object_chain(self._last_oid)
            found = False
            for o in filter(lambda x: x.id()==oid, objs):
                o.hit()
                o.set_ts(diff)
                found = True
            if not found:
                objs.append(ChainObject(oid, name, container, diff))
            self._set_object_chain(self._last_oid, objs)
        self._last_oid = oid
        self._last_ts = dt.now()

    def _check_time_diff(self):
        if self._last_ts:
            diff = dt.now() - self._last_ts
            if diff.total_seconds() < TOTALSECONDS:
                return diff

    def chain_stats(self):
        self.chain_length()
        for o in self._chain:
            print "\tOBJECT: " + o
            for och in self._chain[o]:
                print "\t\tnext: " + och.object_to_string()

    def chain_length(self):
        print "Chain length: " + str(len(self._chain))

    def get_probabilities(self, oid):
        probs1 = self._probabilities(self._get_object_chain(oid))
        probs2 = dict()
        for oi in probs1:
            pr = self._probabilities(self._get_object_chain(oi))
            pr = {k: ProbObject(v.container, v.name, v.probability*probs1[oi].probability, v.time_stamp) for k, v in pr.items()}
            probs2.update(pr)
        for oi in probs2:
            if oi in probs1:
                probs1[oi].probability += probs2[oi].probability
            else:
                probs1[oi] = probs2[oi]
        objs =  filter(lambda (a,b): b.probability>PROB_THRESHOLD, probs1.iteritems())
        return sorted(objs, key=lambda (a,b): b.probability, reverse=True)

    def _probabilities(self, chain):
        total_hits = sum(o.hits for o in chain)
        return {o.id(): ProbObject(o.object_container, o.object_name, o.hits/float(total_hits), o.get_ts()) for o in chain}
 

class ProbObject():
    def __init__(self, container, name, prob, ts=0):
        self.container = container
        self.name = name
        self.probability = prob
        self.time_stamp = ts

    def object_to_string(self):
        return "CONTAINER: " + self.container + " NAME: " + self.name + " P: " + str(self.probability)


class ChainObject():

    def __init__(self, id, name, container, ts):
        self.object_id = id
        self.object_name = name
        self.object_container = container
        self.hits = 1
        self.time_stamp = ''
        self.down_time = 0
        self.set_ts(ts)

    def object_to_string(self):
        return "ID:" + self.object_id + " HITS:" + str(self.hits) + " TS:" + str(self.get_ts())

    def get_object_name(self):
        return self.object_container + " " + self.object_name

    def hit(self):
        self.hits += 1  

    def add_down_time(self, ts):
        if self.down_time == 0:
            self.down_time = ts
        elif ts.total_seconds() > self.down_time.total_seconds():
            self.down_time = ts

    def set_ts(self, ts):
        if not self.time_stamp:
            self.time_stamp = ts
        elif ts.total_seconds() < self.time_stamp.total_seconds():
            self.time_stamp = ts

    def get_ts(self):
        if self.down_time == 0:
            return self.time_stamp.total_seconds()
        elif self.down_time.total_seconds() > self.time_stamp.total_seconds():
            return 0
        else:
            return self.time_stamp.total_seconds() - self.down_time.total_seconds()
        
    def id(self):
        return self.object_id

class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

class NoDaemonPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess


def total_size(o, handlers={}):
    """ Returns the approximate memory footprint an object and all of its contents.

    Automatically finds the contents of the following builtin containers and
    their subclasses:  tuple, list, deque, dict, set and frozenset.
    To search other containers, add handlers to iterate over their contents:

        handlers = {SomeContainerClass: iter,
                    OtherContainerClass: OtherContainerClass.get_elements}

    """
    dict_handler = lambda d: chain.from_iterable(d.items())
    all_handlers = {tuple: iter,
                    list: iter,
                    deque: iter,
                    dict: dict_handler,
                    set: iter,
                    frozenset: iter,
                   }
    all_handlers.update(handlers)     # user handlers take precedence
    seen = set()                      # track which object id's have already been seen
    default_size = getsizeof(0)       # estimate sizeof object without __sizeof__

    def sizeof(o):
        if id(o) in seen:       # do not double count the same object
            return 0
        seen.add(id(o))
        s = getsizeof(o, default_size)
       
        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(o)

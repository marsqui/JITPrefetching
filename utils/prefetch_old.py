from swift.common.swob import Response
from swift.common.internal_client import InternalClient
from swiftclient.service import SwiftService, SwiftError
import itertools
import threading
from sys import argv
import multiprocessing
import multiprocessing.pool
from datetime import datetime as dt
import cPickle as pickle
import hashlib
import urllib2
import time
import os

TOTALSECONDS = 60
PROB_THRESHOLD = 0.2
N_THREADS = 5
AUTOSAVE = 30
CHAINSAVE = '/tmp/chain.p'
PROXY_PATH = '/etc/swift/proxy-server.conf'

acc_status= [200]

prefetched_objects = {}

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):  # @NoSelf
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


 
def download(oid, acc, container, name, u_agent, token, delay=0, request_tries=5):
    print 'Prefetching object with InternalClient: ' + oid + ' after ' + str(delay.total_seconds()) + ' seconds of delay.'
    time.sleep(delay.total_seconds())
    swift = InternalClient(PROXY_PATH, u_agent, request_tries=request_tries)
    headers = {}
    headers['X-Auth-Token'] = token
    headers['X-No-Prefetch'] = 'True'
    status, head, it = swift.get_object(acc, container, name, headers, acc_status)
    print 'Request to Swift - Response Status: ' + str(status) + ' Response headers: ' + str(head)
    data = [el for el in it]
    return (oid, data, head)

def download_curl(oid, server_add, server_port, path, token, delay=0, request_tries=5):
    print 'Prefetching object with Curl: ' + oid + ' after ' + str(delay.total_seconds()) + ' seconds of delay.'
    time.sleep(delay.total_seconds())
    swift = 'http://'+server_add+':'+str(server_port)+path
    req = urllib2.Request(swift)
    req.add_header('X-Auth-Token', token)
    req.add_header('X-No-Prefetch', 'True')

    res = urllib2.urlopen(req)
    print 'Request to: ' + swift + ' Response Status: ' + str(res.code) + ' Response headers: ' + str(res.info())

    return (oid, res.read(), res.info())

def download_swiftclient(oid, container, name, delay=0, request_tries=5):
    try:
        print 'Prefetching object with SwiftClient: ' + oid + ' after ' + str(delay.total_seconds()) + ' seconds of delay.'
        time.sleep(delay.total_seconds())

        _opts = {"auth_version": '2.0',  # Should be '2.0'
                    "os_username": environ.get('OS_USERNAME'),
                    "os_password": environ.get('OS_PASSWORD'),
                    "os_tenant_name": environ.get('OS_TENANT_NAME'),
                    "os_auth_url": environ.get('OS_AUTH_URL'),
                    "retries": request_tries,
                    }
        headers = {"header": ["X-No-Prefetch:True"]}

        with SwiftService(options=_opts) as swift:
            for down_res in swift.download(
                    container=container,
                    objects=[name],
                    options=headers):
                if down_res['success']:
                    print("'%s' downloaded" % down_res['object'])
                    return (oid, down_res['object'], down_res['response_dict']['headers'])
                else:
                    print("'%s' download failed" % down_res['error'])
                    return (oid, [], down_res['response_dict']['headers'])
    except Error as e:
        pass


def log_result(result):
    oid, data, headers = result
    if data:
        prefetched_objects[oid] = (data, headers)
    print 'BSC: Prefetched ' + str(len(prefetched_objects)) + ' objects.'

class JITPrefetching(object):
    
    __metaclass__ = Singleton
    
    def __init__(self, global_conf, filter_conf, logger):
        self.logger = logger
        self.chain = Chain(logger)
        self.chain.auto_save(AUTOSAVE)
        
        
    def execute(self, req_resp, app_iter, requests_data):
        
        method = requests_data['method']
        if 'HTTP_X_NO_PREFETCH' not in req_resp.environ:
            if method.upper() == 'GET':
                self.logger.info("BSC: filter prefetch GET Method")

                object_path = req_resp.environ['PATH_INFO']
                oid = (hashlib.md5(object_path).hexdigest())

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
            # return Response(app_iter=iter(data),
            #                 headers=resp_headers,
            #                 request=req_resp) 
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
        pool = NoDaemonPool(processes=N_THREADS)
        for oid, obj in objs:
            if oid not in prefetched_objects:
                pool.apply_async(download, args=(oid, acc, obj.container, obj.name, user_agent, token, obj.time_stamp, ), callback=log_result)
                #pool.apply_async(download_swiftclient, args=(oid, obj.container, obj.name, obj.time_stamp, ), callback=log_result)
                #pool.apply_async(download_curl, args=(oid, server_add, server_port, path, token, obj.time_stamp, ), callback=log_result)


    def add_object_to_chain(self, oid, requests_data):
        container = requests_data['container']
        object_name = requests_data['object']
        self.chain.add(oid, object_name, container)
        self.chain.chain_stats()



class Chain():

    def __init__(self, logger):
        self.logger = logger     
        self._chain = {}
        self.load_chain()
        self._last_oid = None
        self._last_ts = None

    def load_chain(self):
        try:
            with open(CHAINSAVE, 'rb') as fp:
                self._chain = pickle.load(fp)
        except: 
            pass

    def auto_save(self, timer=300):
        threading.Timer(timer, self.auto_save).start()
        with open(CHAINSAVE, 'wb') as fp:
            pickle.dump(self._chain, fp)


    def _get_object_chain(self, oid):
        if oid in self._chain:
            return sorted(self._chain[oid], key=lambda x: x.hits, reverse=True)
        return []

    def _set_object_chain(self, oid, objs_list):
        self._chain[oid] = objs_list

    def add(self, oid, name, container):
        if oid not in self._chain:
            self._chain[oid] = []
        else:
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
        self.logger.info("CHAIN OBJECTS: " + str(len(self._chain)))
        for o in self._chain:
            self.logger.info("   OBJECT: " + o)
            for och in self._chain[o]:
                self.logger.info("     next: " + och.object_to_string())

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
        return {o.id(): ProbObject(o.object_container, o.object_name, o.hits/float(total_hits), o.time_stamp) for o in chain}
 

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
        self.set_ts(ts)

    def object_to_string(self):
        return "ID:" + self.object_id + " HITS:" + str(self.hits) + " TS:" + str(self.time_stamp.total_seconds())

    def get_object_name(self):
        return self.object_container + " " + self.object_name

    def hit(self):
        self.hits += 1  

    def set_ts(self, ts):
        if not self.time_stamp:
            self.time_stamp = ts
        elif ts.total_seconds() < self.time_stamp.total_seconds():
                self.time_stamp = ts

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
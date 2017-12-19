import csv
import numpy as np
import matplotlib.pyplot as plt
import datetime

trace = '/home/msiquier/IOSTACK/ArcturTrace/to_execute_arctur_equispaced.csv'
trace2 = '/home/msiquier/IOSTACK/ArcturTrace/arctur_trace_final.csv'

self.chain = dict()

with open(trace, 'rb') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    for row in data:

        site = row[0]
        #for trace:
        date = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f')
        #for trace2:
        date = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
        oid = row[3]
        object_name = site + '_' + str(oid) + '_' + str(row[4]) + row[6]

        if site not in self.chain:
            self.chain[site] = Chain()
        self.chain[site].add(oid, object_name, site)
        data = self.get_prefetched(site, oid, objname)
                    self.prefetch_objects(site, oid, account, request)


class Chain():

    def __init__(self, logger=None, chainsave='chain.p', maxseconds=60, prth=0.5, twolevels=False): 
        self.logger = logger
        self._chain = {}
        self._chainsave = chainsave
        self._maxseconds = maxseconds
        self._prth = prth
        self._twolevels = twolevels
        self._last_oid = None
        self._last_ts = None

    def __del__(self):
        with open(self._chainsave, 'wb') as fp:
            pickle.dump(self._chain, fp)


    def save_chain(self):
        with open(self._chainsave, 'wb') as fp:
            pickle.dump(self._chain, fp)

    def auto_save(self, timer=30):
        self.save_chain()
        eventlet.sleep(timer)
        self.auto_save(timer)
        

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


    def add_down_time(self, oid, ts):
        for obj in self._chain:
            objs = self._get_object_chain(obj)
            for o in filter(lambda x: x.id()==oid, objs):
                o.set_down_time(ts)
            self._set_object_chain(obj, objs)


    def _check_time_diff(self):
        if self._last_ts:
            diff = dt.now() - self._last_ts
            if diff.total_seconds() < self._maxseconds:
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
        if self._twolevels:
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
        objs =  filter(lambda (a,b): b.probability>self._prth, probs1.iteritems())
        return sorted(objs, key=lambda (a,b): b.probability, reverse=True)

    def _probabilities(self, chain):
        total_hits = sum(o.hits for o in chain)
        return {o.id(): ProbObject(o.object_container, o.object_name, o.hits/float(total_hits), (o.time_stamp.total_seconds()-o.down_time)) for o in chain}
 

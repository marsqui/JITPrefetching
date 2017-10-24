import cPickle as pickle


CHAINSAVE = '/tmp/chain.p'

        
def main():
	chain = Chain()
	print chain.chain_stats()


class Chain():

    def __init__(self):
        self._chain = {}
        self.load_chain()

  
    def load_chain(self):
        try:
            with open(CHAINSAVE, 'rb') as fp:
                self._chain = pickle.load(fp)
        except: 
            pass

    def chain_stats(self):
        self.chain_length()
        for o in self._chain:
            print "\tOBJECT: " + o
            for och in self._chain[o]:
                print "\t\tnext: " + och.object_to_string()

    def chain_length(self):
        print "Chain length: " + str(len(self._chain))


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

if __name__ == "__main__":
    main()
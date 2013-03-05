#!/usr/bin/env python3
import networkx as nx
#import numpypy as np
import sys
if sys.version.find("PyPy") != -1:
    import numpypy as np
else:
    import numpy as np
#from numpypy.random import randint
#from numpypy.random import rand
import random
from random import random as rand
from multiprocessing import Pool

def randint(n):
    return random.randint(0, n - 1)

def randweight(l):
    r = rand()
    s = 0
    for i, v in enumerate(l):
        s += v
        if s >= r:
            return i
    print("Weigthed random not working.")
    assert False


eps = 1e-10

class System:
    def __init__(self, n, generator, genargs=None, phi=0.5, eta=0.5):
        """
        phi: probability of rewiring
        eta: fraction of heterophil (type 1) agents
        """
        self.graph = generator(n, *genargs)
        self.opinions = np.array([randint(2) for i in range(n)], dtype=int)
        self.types = np.array([0 if rand() > eta else 1 for i in range(n)],
                dtype=int)
        self.phi = phi
        self.n = n
        self.m = sum(self.opinions)
    
    def update_link(self, i):
        n = self.n
        neis = list(self.graph.edge[i].keys())
        degs = np.array([self.graph.degree().values()])
        candidates = np.ones(n, dtype=int)
        candidates[i] = 0
        #candidates[neis] = 0
        candidates[neis] = [0] * len(neis) # pypy
        oi = self.opinions[i]

        if self.types[i] == 0:    
            candidates[self.opinions[candidates] != oi] = 0
        else:
            candidates[self.opinions[candidates] == oi] = 0

        #candidates = np.nonzero(candidates)[0]
        candidates = [k for k in range(n) if candidates[k] == 1] # pypy
        degs = degs[candidates]
        
        if list(candidates):

            #newnei = candidates[randint(len(candidates))]
            newnei = candidates(randweight(degs/sum(degs)));
            self.graph.add_edge(i, newnei)

            if neis:
                oldnei = neis[randint(len(neis))]

                # if oldnei is now alone, reconnect it randomly
                # too keep the graph connected
                if len(list(self.graph.edge[oldnei].keys())) <= 1:
                    cands = list(set(range(self.n)).difference([i, oldnei]))
                    c = cands[randint(len(cands))]
                    self.graph.add_edge(oldnei, c)
                
                self.graph.remove_edge(i, oldnei)


        
    def update_state(self, i):
        neis = list(self.graph.edge[i].keys())
        oi = self.opinions[i]
        if sum(self.opinions[neis] == oi) < 0.5 * len(neis):
            self.m += -2*oi + 1
            self.opinions[i] = (oi + 1) % 2

    def update(self):
        i = randint(self.n)
        if rand() < self.phi:
            self.update_link(i)
        else:
            self.update_state(i)


    def run(self):
        t = 0
        while True:
            self.update()
            t += 1.0/self.n
            if self.m == 0 or self.m == self.n: 
                return t
            elif not nx.is_connected(self.graph):
                print(nx.connected_components(self.graph))
                return t
            
def simulate(tup):
    phi, eta = tup
    S = System(100, nx.generators.barabasi_albert_graph, [4], phi, eta)
    return S.run()

if __name__ == "__main__":
    pool = Pool(processes=2)
    runs = 10

    f = open("grid{0}.dat".format(runs), 'w')
    f.write("# phi eta t\n")

    for phi in [x * 0.05 for x in range(1,20)]:
        for eta in [x * 0.05 for x in range(1,20)]:
            ls = [(phi, eta)] * runs
            ts = map(simulate, ls)
            f.write("{0} {1} {2}\n".format(phi, eta, np.mean(ts)))

        f.flush()




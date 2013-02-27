#!/usr/bin/env python3
import networkx as nx
import numpy as np
from numpy.random import randint
from numpy.random import rand
from multiprocessing import Pool

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
        candidates = np.ones(n, dtype=int)
        candidates[i] = 0
        candidates[neis] = 0
        oi = self.opinions[i]

        if self.types[i] == 0:    
            candidates[self.opinions[candidates] != oi] = 0
        else:
            candidates[self.opinions[candidates] == oi] = 0

        candidates = np.nonzero(candidates)[0]
        
        if neis:
            self.graph.remove_edge(i, neis[randint(len(neis))])
        if list(candidates):
            newnei = candidates[randint(len(candidates))]
            self.graph.add_edge(i, newnei)
        
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
            t += 1/self.n
            if self.m == 0 or self.m == self.n 
                return t
            else if not nx.is_connected(self.graph):
                return t
                
            
def eval(tup):
    phi, eta = tup
    S = System(100, nx.generators.barabasi_albert_graph, [4], phi, eta)
    return S.run()

if __name__ == "__main__":
    print("testing...")
    pool = Pool(processes=8)
    runs = 100
    ts = {}

    f = open("grid.dat", 'w')
    print("# phi eta t",file=f)

    for phi in np.linspace(0.05,0.95,19):
        for eta in np.linspace(0.05,0.95,19):
            ts = pool.map(eval, [(phi, eta)] * runs)
            print(phi, eta, np.mean(ts), file=f, flush=True)


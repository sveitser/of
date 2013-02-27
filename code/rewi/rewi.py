#!/usr/bin/env python3
import networkx as nx
import numpy as np
from numpy.random import randint
from numpy.random import rand

class System:
    def __init__(self, n, generator, genargs=None, phi=0.5, eta=0.5):
        """
        phi: probability of rewiring
        eta: fraction of heterophil (type 1) agents
        """
        self.graph = generator(n, *genargs)
        self.opinions = [randin(2) if for i in range(n)]
        self.types = [0 if rand() > eta else 1 for i in range(n)]
        self.phi = phi
    
    def update_link(self, i):
        neis = self.graph.edge[i]
        self.graph.remove_edge(i, neis[randint(len(neis)))
        strangers = list(set(range(n)).difference(self.graph.edge[i] + [i]))
        self.graph.add_edge(i, strangers[randint(len(strangers))])
        

    def update_state(self, i):


    def update(self, fun):
        
    

if __name__ == "__main__":
    print("testing...")
    S = System(100, nx.generators.barabasi_albert_graph, [4], 0.5, 0.1)


    print(S.graph.degree())

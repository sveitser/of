#!/usr/bin/env python3
import networkx as nx
import numpy as np


# barabasi_albert_graph(n, m, seed=None)
class System:
    def __init__(self, generator, n, m=None):
        self.graph = generator(n, m)
        self.states = [np.random.randint(2) for i in range(n)]
    
    def update(self, fun):

def update(graph):
    

if __name__ == "__main__":
    print("testing...")

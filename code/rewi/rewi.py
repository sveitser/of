#!/home/mantony/code/bin/pypy
import networkx as nx
import sys
if sys.version.find("PyPy") != -1:
    import numpypy as np
else:
    import numpy as np
import random
from random import random as rand
from multiprocessing import Pool
import time

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
        degs = np.array(self.graph.degree().values())
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
            newnei = candidates[randweight(degs/float(sum(degs)))];

            if neis:
                oldnei = neis[randint(len(neis))]

                # if oldnei would become isolated don't do anything
                if len(list(self.graph.edge[oldnei].keys())) <= 1:
                    return
                                
                self.graph.add_edge(i, newnei)
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
            if self.m == 0 or self.m == self.n or t >= 1000: 
                return t
            #elif not nx.is_connected(self.graph):
            #    print(nx.connected_components(self.graph))
            #    return t

    def degree_dist(self):
        degs = self.graph.degree().values()
        d = np.zeros(self.n, dtype=int)
        for n in degs:
            d[n] += 1
        return d

    def degree_dist_type(self):
        degs = self.graph.degree().values()
        d = np.zeros([2, self.n], dtype=int)
        for n, t in zip(degs, self.types):
            d[t, n] += 1
        return d


    def draw(self):
        nx.draw(self.graph)
        nx.draw_networkx_nodes(self.graph, pos=nx.spring_layout(S.graph),
                 node_color=["r" if x==0 else "b" for x in S.types])


            
def simulate(tup):
    phi, eta = tup
    S = System(100, nx.generators.barabasi_albert_graph, [3], phi, eta)
    return S.run()

def grid(nproc, runs):
    tstart = time.time()
    pool = Pool(processes=nproc)
    runs = 100
    f = open("data/grid{0}.dat".format(runs), 'w')
    f.write("# phi eta t\n")

    for phi in [x * 0.025 for x in range(1,20)]:
        for eta in [x * 0.05 for x in range(1,20)]:
            ls = [(phi, eta)] * runs
            ts = pool.map(simulate, ls)
            ts.sort()
            f2 = open("data/ts_phi{0}_eta{1}.dat".format(phi,eta), 'w')
            for t in ts:
                f2.write("{0}\n".format(t))
            
            f.write("{0} {1} {2}\n".format(phi, eta, np.mean(ts)))
            
        f.flush()

    print("nproc {0}, {1} s\n".format(nproc,time.time() - tstart))


def degs(dummy):
    S = System(100, nx.generators.barabasi_albert_graph, [3], phi, eta)
    t = S.run()
    return S.degree_dist_type()

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("usage: ./rewi.py nproc nruns/test")
        exit(1)
    elif sys.argv[1] == "test":
        S = System(100, nx.generators.barabasi_albert_graph, [3], 0.5, 0.5)
        t = S.run()
        print("Consensus Time: {0}".format(t))
        print("degree dist:")
        print(S.degree_dist())
        print("degree dist by type:")
        print(S.degree_dist_type())
        S.draw()
        exit(0)
    else:
    	nproc = int(sys.argv[1])

    phi = float(sys.argv[3])
    eta = float(sys.argv[4])
    nruns = int(sys.argv[2])

    pool = Pool(processes=nproc)
    res = pool.map(degs, [0] * nruns)
    m = np.mean(res, 0)
    print(m)

    np.savetxt("data/ddist_type_phi{0}_eta{1}_n{2}.dat".format(phi,eta,nruns), m)


   



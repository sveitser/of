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
    assert False

class System:
    def __init__(self, n, generator, genargs=None, phi=0.5, eta=0.5,
             majority="weighted"):
        """
        phi: probability of rewiring
        eta: fraction of heterophilic (type 1) agents
        """
        self.graph = generator(n, *genargs)
        self.opinions = np.array([randint(2) for i in range(n)], dtype=int)
        self.types = np.array([0 if rand() > eta else 1 for i in range(n)],
                dtype=int)
        self.phi = phi
        self.n = n
        self.m = sum(self.opinions)
        if majority == "weighted":
            self.majority = self.majority_weighted
        elif majority == "unweighted":
            self.majority = self.majority_unweighted
        else:
            assert False
    
    def update_link(self, i):
        n = self.n
        neis = self.graph.neighbors(i)
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

    def majority_weighted(self, i):
        neis = self.graph.neighbors(i)
        degs = self.graph.degree(neis)
        w = np.zeros(2, dtype=int)
        for op, key in zip(self.opinions[neis], degs):
            w[op] += degs[key]
        
        if w[0] > w[1]:
            return 0
        elif w[1] > w[0]:
            return 1
        else: 
            return None

    def majority_unweighted(self, i):
        neis = self.graph.neighbors(i)
        z = sum(self.opinions[neis] == 0)
        half = len(neis) / 2.0
        if z > half:
            return 0
        elif z < half:
            return 1
        else:
            return None


    def update_state(self, i):
        oi = self.opinions[i]
        maj = self.majority(i)
        if maj != None and maj != oi:
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
            if self.m == 0 or self.m == self.n or t >= 100: 
                return t

    def degree_dist(self):
        degs = self.graph.degree().values()
        d = np.zeros(self.n, dtype=int)
        for n in degs:
            d[n] += 1
        return d.tolist() # pypy pool/numpypy fix

    def degree_dist_type(self):
        degs = self.graph.degree().values()
        d = np.zeros([2, self.n], dtype=int)
        for n, t in zip(degs, self.types):
            d[t, n] += 1
        return d.tolist() # pypy pool/numpypy fix


    def draw(self):
        nx.draw(self.graph)
        nx.draw_networkx_nodes(self.graph, pos=nx.spring_layout(S.graph),
                 node_color=["r" if x==0 else "b" for x in S.types])
                
def simulate(tup):
    phi, eta = tup
    S = System(100, nx.generators.barabasi_albert_graph, [3], phi, eta)
    return S.run()

def grid(runs, rule):
    pool = Pool()
    f = open("data/grid{0}_{1}.dat".format(runs, rule), 'w')
    f.write("# phi eta t\n")

    for phi in [x * 0.025 for x in range(1,20)]:
        for eta in [x * 0.05 for x in range(1,20)]:
            ls = [(phi, eta)] * runs
            ts = pool.map(simulate, ls)
            ts.sort()
            f2 = open("data/ts_phi{0}_eta{1}_{2}.dat".format(phi, eta, rule),
                    'a')
            for t in ts:
                f2.write("{0}\n".format(t))
            
            f.write("{0} {1} {2}\n".format(phi, eta, np.mean(ts)))
            
        f.flush()

def consensus_time_distribution(nruns, phi, eta, maj_rule):
    pool = Pool()
    def ct(i):
        S = System(100, nx.generators.barabasi_albert_graph, [3], phi, eta,
                maj_rule)
        return S.run()

    ts = pool.map(ct,range(nruns))
    ts.sort()
    f = open("data/ts_phi{0}_eta{1}_{2}.dat".format(phi, eta, maj_rule), 'a')
    for t in ts:
        f.write("{0}\n".format(t))

def dd(tup):
    phi, eta, maj_rule = tup
    S = System(100, nx.generators.barabasi_albert_graph, [3], phi, eta,
           maj_rule)
    S.run()
    return S.degree_dist_type()

def degs(nruns, phi, eta, maj_rule):
    pool = Pool()
    dss = pool.map(dd, [(phi, eta, maj_rule)] * nruns)
    ds = np.mean(dss, 0)
    f = open("data/ddist_type_{0}_phi{1}_eta{2}_n{3}.dat".format(maj_rule,
            phi, eta, nruns),
            'w')
    for d in ds:
        for v in d:
            f.write("{0} ".format(v))
        f.write("\n")

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("usage: ./rewi.py nruns/test rule symtype (phi eta)")
        exit(1)
    elif sys.argv[1] == "test":
        S = System(100, nx.generators.barabasi_albert_graph, [3], 0.5, 0.5,
                majority="unweighted")
        t = S.run()
        print("Consensus Time: {0}".format(t))
        print("degree dist:")
        print(S.degree_dist())
        print("degree dist by type:")
        print(S.degree_dist_type())
        S.draw()
        exit(0)

    nruns = int(sys.argv[1])
    maj_rule = sys.argv[2]
    symtype = sys.argv[3]
    if symtype == "grid":
        grid(nruns, maj_rule)
    else:
        phi = float(sys.argv[4])
        eta = float(sys.argv[5])
        if symtype  == "consensus_time_dist":
            consensus_time_distribution(nruns, phi, eta, maj_rule)
        elif symtype == "degree_distribution":
            degs(nruns, phi, eta, maj_rule)








    #pool = Pool(processes=nproc)
    #res = pool.map(degs, [0] * nruns)
    #m = np.mean(res, 0)
    #print(m)



   



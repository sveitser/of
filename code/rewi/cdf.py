from rewi import *
from multiprocessing import Pool


if __name__ == "__main__":
    pool=Pool(processes=8)
    phi = 0.9
    for eta in [0.1, 0.5, 0.9]:
        runs = 10000
        ts = pool.map(simulate, [(phi, eta)] * runs)
        ts.sort()
        f = open("data/ecdf_phi{0}_eta{1}.dat".format(phi,eta),'a')
        for t in ts:
            f.write("{0}\n".format(t))

    

    

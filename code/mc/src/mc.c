/*
 *  Implementation of opinion formation model for benchmarking against julia
 *  version. Bottleneck here seems to be the RNG.
 */
#include <fstream>
#include <ctime>
#include <omp.h>
#include <boost/random.hpp> 
#include <boost/format.hpp>

int main(int argc, char *argv[]){
  if(argc < 3){
    printf("usage: mc N p (nruns = 1000) (tmax)\n");
    exit(1);
  }
 
  const int N = atoi(argv[1]);                // number of agents
  const int n = 3;                            // number of opinions
  double p = atof(argv[2]);                   // degree of homophily
  double tmax = 1e9 * N;                      // max number of MC steps
  int nruns = 1000;
  if(argc > 3){nruns = atoi(argv[3]);}
  if(argc > 4){tmax = atof(argv[4]) * N;}

  std::ofstream fout(str(boost::format("data/N%d_p%.3f.dat") % N % p).c_str());

  double q = 1.0 - p;
  double dN = 1.0 / N;
  double eta = 10;
  p = p * eta / N;
  q = q * eta / N;

  
  #pragma omp parallel for
  for(int run = 0; run < nruns; ++run){
    boost::lagged_fibonacci607 lf(time(NULL) + clock() + run);
    int* s = (int *) malloc(N * sizeof(int));
    double m[n];
    for(int k = 0; k < n; ++k)
      m[k] = 1.0 / n;
    for(int k = 0; k < N; ++k)
      s[k] = k % n;
    double t = 0.0;
    while(t < tmax){
      ++t;
      int a = lf() * N;
      int oa = s[a];
      int neiops[n] = {0};
      for(int j = 0; j < N; ++j){
        double r = lf();
        if(s[j] == oa){
          if(r < p){
            neiops[s[j]] += 1;
          }        
        }else{
          if(r < q){
            neiops[s[j]] += 1;
          }
        }
      }
      int n_maj = - 1;
      int maj_op = - 1;
      for(int k = 0; k < n; ++k){
        if(neiops[k] >= n_maj){
          n_maj = neiops[k];
          maj_op = k;
        }
      }

      if(maj_op == oa){
        continue;
      }

      int nmajority = 0;
      for(int k = 0 ; k < n; ++k){
        if(neiops[k] >= n_maj){
          ++nmajority;
        }
      }
      if(nmajority > 1){
        continue;
      }
      
      m[maj_op] += dN;
      m[oa] -= dN;
      s[a] = maj_op;
      int done = 0;
      for(int k = 0 ; k < n; ++k){
        if(m[k] > 1.0 - dN){
          done = 1;
        } 
      }
      if(done)
        break;
    }
    // printf("%.5f\n",t/N);
    fout << t/N << "\n";
    free(s);
  }
  fout.close();
  return 0;
}


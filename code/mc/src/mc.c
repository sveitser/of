/*
 *  Implementation of opinion formation model for benchmarking against julia
 *  version. Bottleneck is the RNG.
 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>
#include <boost/random/lagged_fibonacci.hpp> // so much faster than rand() !?


const int n = 3;    // number of opinions

int main(int argc, char *argv[]){
  if(argc < 3){
    printf("usage: mc N p (nruns = 1000) (tmax)\n");
    exit(1);
  }
 
  int nruns = 1000;
  int N = atoi(argv[1]);
  double p = atof(argv[2]);
  double tmax = 1e9 * N;
  if(argc > 3){nruns = atoi(argv[3]);}
  if(argc > 4){tmax = atof(argv[4]) * N;}

  srand(time(NULL));

  double q = 1.0 - p;
  double dN = 1.0 / N;
  srand(time(NULL) + clock());

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
    printf("%.5f\n",t/N);
    free(s);
  }
  return 0;
}


/*
 *  Implementation of opinion formation model for benchmarking against julia
 *  version. Bottleneck is the RNG.
 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>
#include <boost/random/lagged_fibonacci.hpp> // so much faster than rand() !?


#define n 3         // number of opinions
#define N 900       // number of agents


int main(int argc, char *argv[]){
  if(argc < 2){
    printf("usage: mc p (nruns) (tmax)\n");
    exit(1);
  }
 
  int nruns = 1000;
  double p = atof(argv[1]);
  double tmax = 1e9 * N;
  if(argc > 2){nruns = atoi(argv[2]);}
  if(argc > 3){tmax = atof(argv[3]) * N;}

  double q = 1.0 - p;
  double dN = 1.0 / N;
  srand(time(NULL) + clock());

  double eta = 10;
  p = p * eta / N;
  q = q * eta / N;

  int run = 0;
  
  #pragma omp parallel for
  for(run = 0; run < nruns; ++run){
    boost::lagged_fibonacci607 lf(time(NULL) + clock());
    int s[N] = {0};
    double m[n];
    int k = 0;
    for( ; k < n; ++k)
      m[k] = 1.0 / n;
    int i = 0;
    for( ; i < N; ++i)
      s[i] = i % n;
    double t = 0.0;
    while(t < tmax){
      ++t;
      int a = lf() * N;
      int oa = s[a];
      int neiops[n] = {0};
      int j = 0;
      for( ; j < N; ++j){
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
      int k = 0;
      for( ; k < n; ++k){
        if(neiops[k] >= n_maj){
          n_maj = neiops[k];
          maj_op = k;
        }
      }

      if(maj_op == oa){
        continue;
      }

      int nmajority = 0;
      k = 0;
      for( ; k < n; ++k){
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
      k = 0;
      int done = 0;
      for( ; k < n; ++k){
        if(m[k] > 1.0 - dN){
          done = 1;
        } 
      }
      if(done)
        break;
    }
    printf("%.5f\n",t/N);
    if(int(t) % 100 == 0)
      fflush(stdout);
  }
  return 0;
}


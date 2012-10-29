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
  if(argc < 4){
    std::cerr << "usage: mc n (opinions) N (players) p (homophily) ";
    std::cerr << "(nruns = 1000) (tmax)" << std::endl;
    exit(1);
  }
 
  const int n = atoi(argv[1]);                // number of opinions
  const int N = atoi(argv[2]);                // number of agents
  const double p_abs = atof(argv[3]);         // degree of homophily
  double tmax = 1e9 * N;                      // max number of MC steps
  int nruns = 1000;
  if(argc > 4){nruns = atoi(argv[4]);}
  if(argc > 5){tmax = atof(argv[5]) * N;}


  const double q_abs = 1.0 - p_abs;
  const double dN = 1.0 / N;
  const double eta = 10;
  const double p = p_abs * eta / N;
  const double q = q_abs * eta / N;

  double* results = (double *) calloc(nruns, sizeof(double));
  
  #pragma omp parallel for
  for(int run = 0; run < nruns; ++run){
    boost::lagged_fibonacci607 lf(time(NULL) + clock() + run);
    int* s = (int *) calloc(N, sizeof(int));
    double* m = (double *) calloc(n, sizeof(double));
    for(int k = 0; k < n; ++k)
      m[k] = 1.0 / n;
    for(int k = 0; k < N; ++k)
      s[k] = k % n;
    double t = 0.0;
    while(t < tmax){
      ++t;
      int a = lf() * N;
      int oa = s[a];
      int* neiops = (int *) calloc(n, sizeof(int));
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

      int nmajority = 0;
      for(int k = 0 ; k < n; ++k){
        if(neiops[k] >= n_maj){
          ++nmajority;
        }
      }
            
      free(neiops);

      if(nmajority > 1 || maj_op == oa){
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
    results[run] = t/N;
    free(s);
    free(m);
  }

  std::ofstream fout(str(boost::format(
          "data/n%d_N%d_p%.3f.dat") % n % N % p_abs).c_str(),
          std::ios_base::app);
  for(int i = 0; i < nruns; ++i)
    fout << results[i] << std::endl;
  fout.close();
  free(results);
  return 0;
}


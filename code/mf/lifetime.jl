#!/usr/bin/julia
load("distributions.jl")
binom = Distributions.Binomial
pmf = Distributions.pmf

function timeev(p, N, eta)
  L = zeros(N + 1, N + 1)
  
  function death_loop(M)
    if M == N   
      return 0 
    end
    if M == 1
      B1 = binom(1, 0)
    else
      B1 = binom(M - 1, p * eta / N)
    end
    B2 = binom(N - M, (1 - p) * eta / N)
    d = 0
    for k in 0 : M - 1
        for l in k + 1 : N - M
            d += pmf(B1, k) * pmf(B2, l)
        end
    end
    return M / N * d
  end

  function death(M)
    if M == N   
      return 0 
    end
    if M == 1
      B1 = binom(1, 0)
    else
      B1 = binom(M - 1, p * eta / N)
    end
    B2 = binom(N - M, (1 - p) * eta / N)
    p2 = reverse(cumsum(pmf(B2, N - M : -1 : 0)))
    ds = pmf(B1, 0 : M - 1)
    d = 0
    for k in 0 : M - 1
      if k < N - M 
        d += ds[k + 1] * p2[k + 2]
      end
    end
    return M / N * d
  end

  function birth(M)
    if M == 0 
      return 0 
    end
    if M == N - 1
      B1 = binom(1, 0)
    else
      B1 = binom(N - M - 1, p * eta / N)
    end
    B2 = binom(M, (1 - p) * eta / N)
    p2s = reverse(cumsum(pmf(B2,M : -1 : 0)))
    ds = pmf(B1, 0 : N - M - 1)
    b = 0
    for l in 0 : N - M - 1
        if l < M 
            b += ds[l + 1] * p2s[l + 2]
        end
    end
    return (N - M) / N * b
  end

  deaths = [death(i) for i in 1:N]

  for i in 1:N
      L[i, i + 1] = deaths[i]
      # L[i + 1, i] = birth(i - 1)
      L[i + 1, i] = deaths[N - i + 1]
      if i > 1 
          L[i, i] = - (L[i + 1, i] + L[i - 1, i])
      end
  end
   return L
end

function minev(L)
   return min(abs(eigvals(L[2:end-1,2:end-1])))
end

function lifetime(p, n, eta)
    return 1/minev(timeev(p, n, eta))
end

### some tests
# ps = linspace(0.5,0.7,640)
# N = 20
# eta = 10
# ts = float([lifetime(p, N, eta) for p in ps])

# load("plot.jl")
# using Plot

# fname = "test.pdf"
# pl = semilogy(ps, ts)
# file(pl, fname)
# system(strcat("evince ", fname))

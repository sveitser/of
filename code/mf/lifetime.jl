#!/usr/bin/julia
load("extras/distributions.jl")
binom = Distributions.Binomial
pmf = Distributions.pmf

function lifetime(p, N, eta)
  L = zeros(N + 1, N + 1)
  
  function death(M)
    if M == N        # probably wrong
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
    for k in 1 : M 
      t = if k < N - M + 1 p2[k + 1] else 0 end
      d += ds[k] * t
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
    p2 = reverse(cumsum(pmf(B2,M - 1 : -1 : 0)))
    ds = pmf(B1, 0 : N - M - 1)
    b = 0
    for l in 1 : N - M
        t = if l < M p2[l + 1] else 0 end
        b += ds[l] * t
    end
    return (N - M) / M * b
  end

  for i in 1:N
      L[i, i + 1] = death(i)
      L[i + 1, i] = birth(i - 1)
      if i > 1 
          L[i, i] = - (L[i + 1, i] + L[i - 1, i])
      end
  end

  return L


end

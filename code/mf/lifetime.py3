#!/usr/bin/python
#   TODO:
#   project onto row space, find largest eigenvalue of inv(A)
#   then invert to get back smallest nonzero eigenvalue of L
#

import numpy as np
from scipy.stats import binom
from numpy.linalg import eigvals, inv
from scipy.sparse.linalg import eigs

def timeev(p, N, eta):
  L = np.zeros([N + 1, N + 1])
  ms = range(0, N)

  def death(M):
    if M == N:
      return 0
    B1 = binom(M - 1, p * eta / N)
    B2 = binom(N - M, (1 - p) * eta / N)
    pmf1, pmf2 = B1.pmf, B2.pmf
    p2 = [pmf2(l) for l in range(N - M + 1)]
    p2.reverse()
    d = 0.0
    p2s = list(np.cumsum(p2))
    p2s.reverse()
    for k in range(M):
      t = p2s[k + 1] if k + 1 < N - M + 1 else 0
      d += pmf1(k) * t
      print(M, pmf1(k), k, t, d)
    return M / N * d

  def birth(M):
    if M == 0:
      return 0
    B1 = binom(N - M - 1, p * eta / N)
    B2 = binom(M, (1 - p) * eta / N)
    pmf1, pmf2 = B1.pmf, B2.pmf
    p2 = [pmf2(m) for m in range(M)]
    p2.reverse()
    p2s = list(np.cumsum(p2))
    p2s.reverse()
    b = 0.0
    for l in range(N - M):
      t = p2s[l + 1] if l + 1 < M else 0
      b += t * pmf1(l)
    return (N - M) / N * b

  ds = [death(i) for i in range(1, N + 1)]
  for i in range(N):
    L[i, i + 1] = ds[i]
    L[i + 1, i] = ds[N - i - 1]
    if i > 0 and i < N:
      L[i, i] = -(ds[N - i - 1] + ds[i - 1])

  return L

def minev(L):
  # remove the first/last row/column
  L = L[1:-1,1:-1]
  val = min(abs(eigvals(L)))
  return val

def lifetime(p, n, eta):
  return 1.0 / minev(timeev(p, n, eta))

if __name__ == "__main__":
  p = 0.3
  N = 20
  eta = 10
  ps = np.linspace(0.01, 0.99, 100)
  ls = [lifetime(p, N, eta) for p in ps]
  print(ls)

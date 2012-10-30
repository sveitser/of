#!/usr/bin/python
#   TODO:
#   project onto row space, find largest eigenvalue of inv(A)
#   then invert to get back smallest nonzero eigenvalue of L
#
from __future__ import division
import numpy as np
from scipy.stats import binom
from numpy.linalg import eigvals, inv
from scipy.sparse.linalg import eigs

def lifetime(p, N, eta):
  L = np.zeros([N + 1, N + 1])
  ms = range(0, N)

  def death(M):
    if M == N:
      return 0
    B1 = binom(M - 1, p * eta / N)
    B2 = binom(N - M, (1 - p) * eta / N)
    pmf1, pmf2 = B1.pmf, B2.pmf
    d = 0.0
    for k in range(M):
      t = 0
      for l in range(k + 1, N - M + 1):
        t += pmf2(l)
      d += pmf1(k) * t
    return M / N * d

  def birth(M):
    if M == 0:
      return 0
    B1 = binom(N - M - 1, p * eta / N)
    B2 = binom(M, (1 - p) * eta / N)
    pmf1, pmf2 = B1.pmf, B2.pmf
    b = 0.0
    for l in range(N - M):
      t = 0
      for m in range(l + 1, M):
        t += pmf2(m)
      b += t * pmf1(l)
    return (N - M) / N * b

  for i in range(N):
    L[i, i + 1] = death(i + 1)
    L[i + 1, i] = birth(i)
    if i > 0 and i < N:
      L[i, i] = -(birth(i) + death(i))

  # remove the first/last row/column
  L = L[1:-1,1:-1]
  

  val = eigvals(inv(L))
  val = abs(val)
  val = max(val)
  #l = max(lambdas[lambdas > 0])
  l = val

  return l

if __name__ == "__main__":
  p = 0.3
  N = 20
  eta = 10
  ps = np.linspace(0.01, 0.99, 100)
  ls = [lifetime(p, N, eta) for p in ps]
  print(ls)

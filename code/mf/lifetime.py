#!/usr/bin/python

# TODO: use julia

from __future__ import division
import numpy as np
from scipy.stats import binom
from numpy.linalg import eig
# import sympy
# from sympy.matrices import Matrix

def lifetime(p, N):
  L = np.zeros([N + 1, N + 1])
  ms = range(0, N)
  rv = binom(N - 1, p)
  binos = np.cumsum([rv.pmf(x) for x in range(0,N)])

  def death(M):
    return  M / N * binos[N - M - 1] if M != N else 0

  def birth(M):
    return (N - M) / N * binos[M - 1] if M != 0 else 0

  for i in range(N):
    L[i, i + 1] = death(i + 1)
    L[i + 1, i] = birth(i)
    if i > 0 and i < N:
      L[i, i] = -(birth(i) + death(i))


  # L = Matrix(L).applyfunc(lambda x:sympy.N(x, 10)) # too slow

  lambdas, v  = eig(L)
  lambdas = abs(lambdas)
  l = min(lambdas[lambdas > 0])

  return l

if __name__ == "__main__":
  p = 0.3
  N = 80
  l = lifetime(p, N)
  print(l)

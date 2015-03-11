import numpy as np
from numpy import linalg

def conicToParametric(coef):
  A = 1
  B = coef[0]
  C = coef[1]
  D = coef[2]
  E = coef[3]
  F = coef[4]

  T = np.arctan(B / (A - C)) / 2

  M_0 = np.matrix([[F, D/2, E/2], [D/2, A, B/2], [E/2, B/2, C]])
  M = np.matrix([[A, B/2], [B/2, C]])
  lambdas = linalg.eigvals(M)

  lambda1 = lambdas[1]
  lambda2 = lambdas[0]
  if abs(lambda1 - A) > abs(lambda1 - C):
    temp = lambda1
    lambda1 = lambda2
    lambda2 = temp

  h = (B*E - 2*C*D)/(4*A*C - B**2)
  k = (B*D - 2*A*E)/(4*A*C - B**2)

  detRatio = -linalg.det(M_0)/linalg.det(M)
  a = np.sqrt(detRatio/lambda1)
  b = np.sqrt(detRatio/lambda2)

  if a < b:
    temp = a
    a = b
    b = temp
    T = T + np.pi/2

  return [h, k, a, b, T]

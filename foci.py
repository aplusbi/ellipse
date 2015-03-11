import numpy as np

def foci(e, p):
  x, y = p
  h, k, a, b, tau = e[:5]

  c = np.sqrt(a**2 - b**2)
  
  f1 = (h - c*np.cos(tau), k - c*np.sin(tau))
  f2 = (h + c*np.cos(tau), k + c*np.sin(tau))

  return (f1, f2)

def focalDistance(e, p):
  x, y = p
  (f1x, f1y), (f2x, f2y) = foci(e, p)

  dist_f1 = np.sqrt((f1x - x)**2 + (f1y - y)**2)
  dist_f2 = np.sqrt((f2x - x)**2 + (f2y - y)**2)

  return dist_f1 + dist_f2

def isInside(e, p):
  x, y = p
  h, k, a, b, tau = e[:5]

  dist = focalDistance(e, p)

  return dist <= 2*a

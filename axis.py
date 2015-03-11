import numpy as np

def getMajorAxis(e):
  h = e[0]
  k = e[1]
  a = e[2]
  b = e[3]
  tau = e[4]

  x0 = h + np.cos(tau) * a
  y0 = k + np.sin(tau) * a
  x1 = h - np.cos(tau) * a
  y1 = k - np.sin(tau) * a

  return (x0, y0, x1, y1)

def getMinorAxis(e):
  h = e[0]
  k = e[1]
  a = e[2]
  b = e[3]
  tau = e[4] + np.pi/2

  x0 = h + np.cos(tau) * b
  y0 = k + np.sin(tau) * b
  x1 = h - np.cos(tau) * b
  y1 = k - np.sin(tau) * b

  return (x0, y0, x1, y1)

def getLine(xy):
  x0, y0, x1, y1 = xy
  deltax = x1 - x0
  deltay = y1 - y0
  m = deltay / deltax
  b = y0 - m*x0

  return (m, b)

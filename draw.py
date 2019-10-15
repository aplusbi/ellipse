from PIL import Image
import numpy as np

def draw(im, points, color):
  width, height = im.size
  for x, y in points:
    if x >= 0 and x < width and y >= 0 and y < height:
      im.putpixel((int(x), int(y)), color)

def drawEllipse(im, e, color):
  h = e[0]
  k = e[1]
  a = e[2]
  b = e[3]
  tau = e[4]

  # get a bunch of points between 0 and 2pi
  t = np.linspace(0, 2*np.pi, min(a*b, 500))

  # rotation matrix
  rMat = np.matrix([[np.cos(tau), -np.sin(tau)], [np.sin(tau), np.cos(tau)]])
  pMat = np.matrix([a*np.cos(t), b*np.sin(t)])
  p = (rMat * pMat).transpose()

  # add the center
  p[:,0] += h
  p[:,1] += k

  points = []
  for i in range(0, len(p)):
    points.append((p[i,0], p[i,1]))

  draw(im, points, color)


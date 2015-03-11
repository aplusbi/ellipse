from scipy.spatial import ConvexHull
from scipy.optimize import minimize
import numpy as np
from conicToParametric import conicToParametric
from radiansToDegreesFromNorth import radiansToDegreesNorth

def ellipsesFromImage(im, bg):
  dim = im.size

  ellipses = []

  for x in range(0, dim[0]):
    for y in range(0, dim[1]):
      points = getPoints(im, bg, x, y)

      if len(points) <= 2:
        continue

      points = np.array(points)
      hull = ConvexHull(points)
      pixels = points[hull.vertices]

      (offset, coef) = fitEllipse(pixels)

      # if this constraint is not met, it's hyperbolic
      if coef[0] ** 2 / 4 >= coef[1]:
          continue

      # convert from conic representation to parametric
      ellipse = conicToParametric(coef)
      ellipse[0] += offset[0]
      ellipse[1] += offset[1]
      ellipse[4] = normalizeAngle(ellipse[4])

      # convert radians to geologic degrees
      ellipse.append(radiansToDegreesNorth(ellipse[4]))

      # calculate the error of the ellipse
      ellipse.append(errorRate(points, offset, coef))

      ellipses.append(ellipse)

  return ellipses

def getTrueAngle(x, y):
  if x == 0:
    if y > 0:
      return np.pi / 2
    else:
      return 3 * np.pi / 2

  angle = np.arctan(y / x)
  if x < 0:
    angle += np.pi
  else:
    if y < 0:
      angle += 2*np.pi

  return angle

def normalizeAngle(tau):
  while tau < 0:
    tau += 2*np.pi

  if tau > np.pi:
    tau -= np.pi

  return tau

def getPoints(im, bg, startx, starty):
  ret = []

  # keep looping as long as we have pixels to look at
  toVisit = [(startx, starty)]
  while len(toVisit) > 0:
    x, y = toVisit.pop()
    pixel = getPixel(im, bg, x, y)

    if pixel == bg:
      continue

    im.putpixel((x, y), bg)
    ret.append((x, y))
    for i in range(x-1, x+2):
      for j in range(y-1, y+2):
        if getPixel(im, bg, i, j) != bg:
          toVisit.append((i, j))

  return ret

def getPixel(im, bg, x, y):
  pixel = bg
  try:
    pixel = im.getpixel((x, y))
  except IndexError:
    pixel = bg

  return pixel

def fitEllipse(points):
  offset = points[0]
  p = points - offset
  M = getDataMatrix(p[:,0], p[:,1])
  coef = np.zeros(5)

  cons = {}
  cons['type'] = 'ineq'
  cons['fun'] = lambda coef: (coef[0] ** 2 / 4 < coef[1]) and coef[2]**2 / 4 + coef[3] ** 2 / (4*coef[1]) > coef[4]

  opt = minimize(lambda c: costFunction(M, p[:,0], c), coef, constraints=cons, jac=lambda c: gradFunction(M, p[:,0], c))

  return (offset, opt.x)

def costFunction(M, x, coef):
  coef = np.matrix(coef).transpose()
  distances = (M * coef) + np.matrix(np.multiply(x, x)).transpose()
  return sum(np.multiply(distances, distances))

def gradFunction(M, x, coef):
  coef = np.matrix(coef).transpose()
  grad = M.transpose() * ((M*coef) + np.matrix((np.multiply(x, x))).transpose())
  return np.asarray(grad)

def getDataMatrix(x, y):
  M = np.ones((len(x),5))
  M[:, 0] = np.multiply(x,  y)
  M[:, 1] = np.multiply(y, y)
  M[:, 2] = x
  M[:, 3] = y

  return np.matrix(M)

def errorRate(points, offset, coef):
  p = points - offset
  M = getDataMatrix(p[:,0], p[:,1])
  return costFunction(M, p[:,0], coef)

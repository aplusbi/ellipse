#!/usr/bin/python
import sys
import os
import axis
import csv
from foci import isInside
from PIL import Image
from PIL import ImageDraw
from ellipsesFromImage import ellipsesFromImage
from draw import drawEllipse
import numpy as np

def main():
  efile = sys.argv[1]

  im = Image.open(efile).convert('RGBA').transpose(Image.FLIP_TOP_BOTTOM)
  bg = im.getpixel((0,0))
  size = im.size

  ellipses = ellipsesFromImage(im, bg)

  im = 0

  filename, extension = os.path.splitext(efile)
  
  #ellipses = ellipsesFromCsv(filename + '_ellipses.csv')

  writeEllipseCsv(filename + '_ellipses.csv', ellipses)
  drawEllipseFile(filename + '_ellipses.png', size, ellipses)
  drawNumberFile(filename + '_numbers.png', size, ellipses)

def ellipsesFromCsv(csvFile):
  ellipses = []
  with open(csvFile, 'r') as efile:
    reader = csv.DictReader(efile)
    for row in reader:
      ellipses.append([float(row['h']), float(row['k']), float(row['a']), float(row['b']), float(row['tau']), float(row['azimuth']), float(row['error'])])
  return ellipses


def drawEllipseFile(filename, size, ellipses):
  eOutput = Image.new('RGBA', size, (255, 255, 255, 0))
  drawer = ImageDraw.Draw(eOutput)
  for e in ellipses:
    drawEllipse(eOutput, e, (0, 0, 0, 255))
    major = axis.getMajorAxis(e)
    minor = axis.getMinorAxis(e)
    drawer.line(major, (255, 0, 0, 255), width=1)
    drawer.line(minor, (0, 0, 255, 255), width=1)

  eOutput.transpose(Image.FLIP_TOP_BOTTOM).save(filename)

def drawNumberFile(filename, size, ellipses):
  nOutput = Image.new('RGBA', size, (255, 255, 255, 0))
  drawer = ImageDraw.Draw(nOutput)
  for n, e in enumerate(ellipses):
    x = e[0]
    y = size[1] - e[1]
    drawer.text((x, y), str(n), (0, 0, 0, 255))

  nOutput.save(filename)

def writeEllipseCsv(filename, ellipses):
  indices = range(0, len(ellipses))
  parents = getParents(ellipses)

  #insert the indices and parents into the output rows
  rows = np.matrix(ellipses)
  rows = np.insert(rows, 0, parents, axis=1)
  rows = np.insert(rows, 0, indices, axis=1)

  with open(filename, 'wb') as output:
    writer = csv.writer(output, delimiter=',')
    writer.writerow(['index', 'parent', 'h', 'k', 'a', 'b', 'tau', 'azimuth', 'error'])
    writer.writerows(rows.tolist())

def getParents(ellipses):
  parents = []
  for n, e in enumerate(ellipses):
    candidates = ellipses
    del candidates[n]
    parent = findParent(e, candidates)
    parents.append(parent)
    candidates.insert(n, e)

  return parents

def findParent(e, candidates):
  p = e[:2]
  child_a = e[3]

  for n, candidate in enumerate(candidates):
    # the child major axis should be shorter than the parent
    if child_a > candidate[3]:
      continue

    if isInside(candidate, p):
      return n

  return -1

if __name__=='__main__':
  main()


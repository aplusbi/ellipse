#!/usr/bin/python

import csv
import axis
import sys
from scipy.cluster.vq import kmeans2

def main():
  csvfile = sys.argv[1]
  csvhandle = open(csvfile)
  reader = csv.reader(csvhandle)
  ellipses = [e for e in reader]
  ellipses = ellipses[1:]
  ellipses = [ [float(x) for x in e] for e in ellipses]
  cones = filter(lambda e: len(e) == 5, ellipses)
  craters = filter(lambda e: len(e) > 5, ellipses)

  cones_major = [axis.getLine(axis.getMajorAxis(e)) for e in cones]
  craters_major = [axis.getLine(axis.getMajorAxis(e)) for e in craters]
  print cones_major
  print craters_major

if __name__=='__main__':
  main()

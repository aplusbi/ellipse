#!/usr/bin/python
import csv
import sys
import os
import numpy as np

def main():
  efile = sys.argv[1]
  filename, extension = os.path.splitext(efile)
  outname = filename + '_degreesNorth.csv'

  with open(outname, 'w') as csvout:
    csvwriter = csv.DictWriter(csvout, fieldnames=['h','k','a','b','tau'], delimiter=',', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writeheader()

    with open(efile, 'r') as csvin:
      csvreader = csv.DictReader(csvin, delimiter=',')
      for row in csvreader:
        tau = float(row['tau'])
        row['tau'] = radiansToDegreesNorth(tau)

        csvwriter.writerow(row)

def radiansToDegreesNorth(tau):
  tau = tau * 180.0 / np.pi
  tau = 90 - tau
  if tau < 0:
    tau = tau + 180
  return tau

if __name__=='__main__':
  main()

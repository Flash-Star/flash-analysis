# Browse the directory tree, locate each integrals file, and extract information
# Don: 12/11/2015: just fixed re expression for dir_re to permit finding amplitude 6 files
# bringing the total number of integral files to the correct number of 35.

import os
import re
import csv
from collections import OrderedDict


## Custom imports
from IntegralFlashData import IntegralFlashData

## Setup
dir_re = re.compile('\A.*/ignMPoleA-([0-9]{1,2})e5\Z')
fil_re = re.compile('\Aprofile75_mpole-([0-9]{1,2})_r-35e6_a-([0-9]{1,2})e5_ordered.dat\Z')
ifd = IntegralFlashData()

data = [] # data_entry={}

def getData(f,ifd=ifd):
  ifd.readInts(f)
  ifd.GramsToMsun()
  dat = ifd.getArrayData()
  ifd.clrArrayData()
  return dat

# Collect integrals from each file
for root, dirs, files in os.walk(os.getcwd()):
  print 'in directory: ' + root
  if dir_re.match(root):
    for f in files:
      m = fil_re.match(f)
      if m:
        mpole_num = m.group(1)
        amp_num   = m.group(2)
        print 'got file: mpole-' + mpole_num + ', amp-' + amp_num
        data_entry = {'mpole': mpole_num,
                      'amp': amp_num,
                      'dat': getData(os.path.join(root,f))}
        data.append(data_entry)

# Process integrals
print 'Length of data structure: ' + str(len(data))

## Sort integrals by final estimated Ni56 mass
data.sort(key=lambda entry: entry['dat']['estimated Ni56 mass'][-1])

## Output results
with open('ni56-prod-sorted_integrals_ini.csv','wb') as csvfile:
  cwriter = csv.writer(csvfile, delimiter=',')
  row = ['amp','mpole'] + data[0]['dat'].keys()
  cwriter.writerow(row)
  for entry in data:
    row = [entry['amp'],entry['mpole']] + [v[0] for k,v in entry['dat'].iteritems()]
    cwriter.writerow(row)

with open('ni56-prod-sorted_integrals_fin.csv','wb') as csvfile:
  cwriter = csv.writer(csvfile, delimiter=',')
  row = ['amp','mpole'] + data[0]['dat'].keys()
  cwriter.writerow(row)
  for entry in data:
    row = [entry['amp'],entry['mpole']] + [v[-1] for k,v in entry['dat'].iteritems()]
    cwriter.writerow(row)



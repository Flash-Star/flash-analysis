from IntegralFlashData import IntegralFlashData
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict
import sys
import bisect
import glob as glob

ifd = IntegralFlashData()

if len(sys.argv)==1:
	print 'Please supply a list of input files to process!'
	exit()
ifnames = sys.argv[1:]

N = len(ifnames)
min_time = 0.25

# Make a dictionary for the data
ifdata = OrderedDict([])
dettimes = OrderedDict([])
headers = []
shortheaders = []
for i in xrange(0,N):
    iname = ifnames[i]
    inum = iname.split('-')[1].split('.')[0]
    intdatname = glob.glob('profile75_mpole-'+inum+'*_ordered.dat')
    ifd.readInts(intdatname[0])
    ifdata[inum] = ifd.getArrayData()
    if i==0:
	headers = ifdata[inum].keys()
	shortheaders = [hj.replace(' > ','>').replace(' ','_') for hj in headers]
    ifd.clrArrayData()
    detp_file = open(iname,'r')
    ddt_times = []
    for l in detp_file:
	ls = l.split()
	ddt_times.append(float(ls[0]))
    detp_file.close()
    dettimes[inum] = np.array(ddt_times)

# find all the time indices
ddt_time_indices = OrderedDict([])
for k,d in ifdata.iteritems():
	ddt_ti = []
	for ti in xrange(len(dettimes[k])):
		tib = bisect.bisect(d['time'],dettimes[k][ti])
		if (dettimes[k][ti]-d['time'][tib-1])<=(d['time'][tib]-dettimes[k][ti]):
			tib = tib-1
		ddt_ti.append(tib)
	ddt_time_indices[k] = np.array(ddt_ti)

ofk = open('ddt_time_detp_firsts.dat','w')
ofk.write('# ')
for hi in headers:
	ofk.write(hi + '  ')
ofk.write('\n')
for k,d in ifdata.iteritems():
	time_indx = ddt_time_indices[k] 
	for ti in time_indx:
		if d['time'][ti] >= min_time:
			for hi in headers:
				ofk.write('{:1.14e}'.format(d[hi][ti]) + '  ')
			ofk.write('\n')	
			break
ofk.close()

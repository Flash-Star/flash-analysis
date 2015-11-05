from IntegralFlashData import IntegralFlashData
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from collections import OrderedDict
import sys
import glob as glob

pref = 'profile75_'
suff = '_ordered.dat'
ifd = IntegralFlashData()
ifnames = glob.glob(pref+'*'+suff)

N = len(ifnames)
pbi = xrange(0,N)

# Make a dictionary for the data
ifdata = OrderedDict([])
headers = []
shortheaders = []
for i in xrange(0,N):
    p = pbi[i]
    iname = ifnames[i]
    ifd.readInts(iname)
#    ifd.orderData()
    ifdata[p] = ifd.getArrayData()
    if i==0:
	headers = ifdata[p].keys()
	shortheaders = [hj.replace(' > ','>').replace(' ','_') for hj in headers]
    ifd.clrArrayData()

## Calculate and write the ints_mean
# Get the range of time points for each dataset and interpolate only on the datasets where we have information
t_min_vec = [d['time'][0] for k,d in ifdata.iteritems()]
t_max_vec = [d['time'][-1] for k,d in ifdata.iteritems()]
print 't_min_vec: '
print t_min_vec
print 't_max_vec: '
print t_max_vec

print 'Number of integral files: ' + str(N)
print 'Number processed: ' + str(len(t_min_vec)) + ' = ' + str(len(t_max_vec))

# Construct interpolation function for each dataset
data_interps = OrderedDict([])
for dk in ifdata.keys():
	data_interps[dk] = OrderedDict([])
	for h in headers:
		if h!='time':
			data_interps[dk][h] = interpolate.interp1d(ifdata[dk]['time'],ifdata[dk][h],kind='linear') 
print 'Finished constructing interpolation functions!'

# Construct the time vector to use for the interpolation
t_interp_vec_npts = max([len(d['time']) for k,d in ifdata.iteritems()])
t_interp_vec_max = max(t_max_vec)
t_interp_vec_min = min(t_min_vec)

t_interp_vec = np.linspace(t_interp_vec_min,t_interp_vec_max,num=t_interp_vec_npts)

ints_stats = OrderedDict([])
which_ints_stats = ['min','max','mean','median']
for wis in which_ints_stats:
	ints_stats[wis] = OrderedDict([])
	for h in headers:
		ints_stats[wis][h] = np.empty(t_interp_vec_npts) # Defaults to float datatype

def vector_min(v):
	return min(v)
def vector_max(v):
	return max(v)
def vector_mean(v):
	return np.mean(v)
def vector_median(v):
	return 0.5*(vector_min(v)+vector_max(v))

vector_stats = {'min': vector_min,
		'max': vector_max,
		'mean': vector_mean,
		'median': vector_median}

for k,v in ints_stats.iteritems():
	v['time'] = t_interp_vec

for tn in xrange(0,t_interp_vec_npts):
	for h in headers:
		if h!='time':
			h_vec = []
			for k,dint in data_interps.iteritems():
				try:
					h_vec.append(dint[h](t_interp_vec[tn]))
				except ValueError:
					continue
			h_vec = np.array(h_vec)
			for k,v in ints_stats.iteritems():
				v[h][tn] = vector_stats[k](h_vec)

print 'Finished constructing stats dataset!'

# Write the ints_stats out to files
for k,v in ints_stats.iteritems():
	ofile = open(pref+k+'.dat','w')
	ofile.write('#')
	for h in headers:
		ofile.write(h + '  ')
	ofile.write('\n')
	for n in xrange(0,t_interp_vec_npts):
		for h in headers:
			ofile.write('{:1.14e}'.format(v[h][n]) + '  ')
		ofile.write('\n')
	ofile.close()

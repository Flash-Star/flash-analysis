from IntegralFlashData import IntegralFlashData
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from collections import OrderedDict
import sys

pbi = range(1,31)
N = len(pbi)
pref = 'Realization_'
suff = '_ordered.dat'
ifd = IntegralFlashData()

# Make a dictionary for the data
ifdata = OrderedDict([])
headers = []
shortheaders = []
for i in xrange(0,N):
    p = pbi[i]
    iname = pref + '{0:03}'.format(p) + suff
    ifd.readInts(iname)
#    ifd.orderData()
    ifdata[p] = ifd.getArrayData()
    if i==0:
	headers = ifdata[p].keys()
	shortheaders = [hj.replace(' > ','>').replace(' ','_') for hj in headers]
    ifd.clrArrayData()

## Calculate and write the mean
# Get the range of time points for each dataset and interpolate only on the datasets where we have information
t_min_vec = [d['time'][0] for k,d in ifdata.iteritems()]
t_max_vec = [d['time'][-1] for k,d in ifdata.iteritems()]
print 't_min_vec: '
print t_min_vec
print 't_max_vec: '
print t_max_vec

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

mean = OrderedDict([])
for h in headers:
	mean[h] = []

#for h in headers:
#	if h!='time':
#		mean[h] = [0.5*(max([dint[h](t_interp)])+min([dint[h](t_interp)])) for k,dint in data_interps.iteritems() for t_interp in t_interp_vec]

mean['time'] = t_interp_vec
for t_i in t_interp_vec:
	for h in headers:
		if h!='time':
			h_vec = []
			for k,dint in data_interps.iteritems():
				try:
					h_vec.append(dint[h](t_i))
				except ValueError:
					continue
			mean[h].append(np.mean(h_vec))

for h in headers:
	mean[h] = np.array(mean[h])

print 'Finished constructing mean dataset!'

# Write the mean out to a file
ofile = open(pref+'mean.dat','w')
ofile.write('#')
for h in headers:
	ofile.write(h + '  ')
ofile.write('\n')
for n in xrange(0,len(t_interp_vec)):
	for h in headers:
		if h=='time':
			ofile.write('{:1.14e}'.format(t_interp_vec[n]) + '  ')
		else:
			ofile.write('{:1.14e}'.format(mean[h][n]) + '  ')
	ofile.write('\n')
ofile.close()

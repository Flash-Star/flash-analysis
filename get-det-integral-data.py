import os
import sys
from bisect import bisect
import numpy as np
from collections import OrderedDict

if len(sys.argv)==1:
	print 'Please supply an integral file to process.'
ifiles = sys.argv[1:]

loc = os.getcwd()
outname = 'det_integrals.dat'

intsdata = OrderedDict([])
intsdata['mpoles'] = []
intsini['ign_rad'] = []
intsini['ign_amp'] = []
gotCols = False
ncols = 0
cols = []

for (path,dirs,files) in os.walk(loc):
	for f in files:
		if (f[0:9]=='profile75' and f[-4:]=='.dat'):
			# Read the data from this integral file
			fint = open(path + '/' + f,'r')
			# get data from file name
			fs = f.split('_')
			mpole_num = fs[1].lstrip('mpole-')
			
			# Open the detonation points file
			fdet = open(path + '/detpoints_mpole-'+mpole_num+'.dat','r')
			# get the detonation points
			detp = OrderedDict([])
			detp['time'] = []
			detp['x1'] = [] # 2D-cyl: corresponds to polar r
			detp['x2'] = [] # 2D-cyl: corresponds to z
			detp['x3'] = [] # 2D-cyl: should always be 0
			for dl in fdet:
				dlsf = [float(dlsi) for dlsi in dl.split()]
				detp_entry = zip(detp.keys(),dlsf)
				for k,v in detp_entry:
					detp[k].append(v)
				
			intsini['mpoles'].append(mpole_num)
			intsini['ign_rad'].append(fs[2].lstrip('r-'))
			intsini['ign_amp'].append(fs[3].lstrip('a-').rstrip('.dat'))
			# get headers
			h = fint.readline()
			if (not gotCols):
				ncols = 0
				hs = h.lstrip('  #').rstrip('\n').split('  ')
				for hi in hs:
					if (hi != ''):
						hi = hi.lstrip(' ')
						cols.append(hi)	
						ncols = ncols + 1
				# prepare column data structures
				for c in cols:
					intsini[c] = []
				gotCols = True
			# read all data points
			data = {}
			print path + '/' + f
			for c in cols:
				data[c] = []
			for l in fint:
				srow = l.split()
				for i in range(0,ncols):
					data[cols[i]].append(float(srow[i]))
			npdata = {}
			for k,v in data.iteritems():
				npdata[k] = np.array(v)
			# get index of first detonation time or right after.
			#ddt1_index = bisect(npdata['time'],ddt1)	
			#for i in range(0,ncols):
			#	intsini[cols[i]].append(npdata[cols[i]][ddt1_index])
			fint.close()
			
# Output to a file ...
fout = open(outname,'w')
for i in range(0,len(intsini['mpoles'])):
	fout.write('----------\n') # 10 -'s
	for k,v in intsini.iteritems():
		fout.write(k + '  ')
	fout.write('\n')
	for k,v in intsini.iteritems():
		fout.write(v[i] + '  ')
	fout.write('\n')
fout.close()

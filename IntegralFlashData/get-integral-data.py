import os
from collections import OrderedDict

loc = os.getcwd()
outname = 'ini_fin_integrals.dat'

intsini = OrderedDict([])
intsini['mpoles'] = []
intsini['ign_rad'] = []
intsini['ign_amp'] = []
intsfin = OrderedDict([])
intsfin['mpoles'] = []
intsfin['ign_rad'] = []
intsfin['ign_amp'] = []
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
			intsini['mpoles'].append(fs[1].lstrip('mpole-'))
			intsini['ign_rad'].append(fs[2].lstrip('r-'))
			intsini['ign_amp'].append(fs[3].lstrip('a-').rstrip('.dat'))
			intsfin['mpoles'].append(fs[1].lstrip('mpole-'))
			intsfin['ign_rad'].append(fs[2].lstrip('r-'))
			intsfin['ign_amp'].append(fs[3].lstrip('a-').rstrip('.dat'))
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
					intsfin[c] = []
				gotCols = True
			# read first and last data point
			row = fint.readline()
			srow = row.split()
			print ncols
			print srow
			print path + '/' + f
			for i in range(0,ncols):
				intsini[cols[i]].append(srow[i])
			for l in fint:
				row = l
			srow = row.split()
			print srow
			for i in range(0,ncols):
				intsfin[cols[i]].append(srow[i])
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
	for k,v in intsfin.iteritems():
		fout.write(v[i] + '  ')
	fout.write('\n')
fout.close()

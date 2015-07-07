from collections import OrderedDict

intdataname = 'ini_fin_integrals.dat'

intsini = OrderedDict([])
intsfin = OrderedDict([])
gotCols = False
ncols = 0
cols = []
nentries = 0

# Read the data from this integral file
fint = open(intdataname,'r')
# get headers
while (True):
	l = fint.readline()
	if not l:
		break
	if (l=='----------\n'):
		h = fint.readline()
		if (not gotCols):
			ncols = 0
			hs = h.rstrip('\n').split('  ')
			for hi in hs:
				if (hi != ''):
					cols.append(hi)	
					ncols = ncols + 1
			# prepare column data structures
			for c in cols:
				print c
				intsini[c] = []
				intsfin[c] = []
			gotCols = True
		# read first and last data point
		row = fint.readline()
		srow = row.split()
		for i in range(0,ncols):
			intsini[cols[i]].append(srow[i])
		row = fint.readline()
		srow = row.split()
		for i in range(0,ncols):
			intsfin[cols[i]].append(srow[i])
		nentries = nentries + 1
fint.close()
	
# Note: diffed testing.txt and original file, no difference!
#fout = open('testing.txt','w')
#for i in range(0,nentries):
#	fout.write('----------\n') # 10 -'s
#	for k,v in intsini.iteritems():
#		fout.write(k + '  ')
#	fout.write('\n')
#	for k,v in intsini.iteritems():
#		fout.write(v[i] + '  ')
#	fout.write('\n')
#	for k,v in intsfin.iteritems():
#		fout.write(v[i] + '  ')
#	fout.write('\n')
#fout.close()


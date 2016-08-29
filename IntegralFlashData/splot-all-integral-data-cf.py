from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from CustomScatterplot import CustomScatterplot
from matplotlib import rc

rc('text', usetex=False)

intdataname_brendan = 'ini_fin_integrals_brendan.dat'
intdataname_cone = 'ini_fin_integrals_cone.dat'

intsini = OrderedDict([])
intsfin = OrderedDict([])

# get headers
def readintfile(f,intsini,intsfin):
	ncols = 0
	cols = []
	gotCols = False
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
					if not c in intsini:
						intsini[c] = []
					if not c in intsfin:
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

# Read the data from the integral files
fint = open(intdataname_brendan,'r')
readintfile(fint,intsini,intsfin)
fint.close()
nentries_brendan = len(intsini['mass burned'])
print 'N_brendan: ' + str(nentries_brendan)
fint = open(intdataname_cone,'r')
readintfile(fint,intsini,intsfin)
fint.close()
nentries_cone = len(intsini['mass burned']) - nentries_brendan
print 'N_cone: ' + str(nentries_cone)

# Reorganize the data into a single dictionary for plotting ease
# Convert strings to numbers
data_ini = OrderedDict([])
data_fin = OrderedDict([])
headers = intsini.keys()
headers.remove('Realization')
headers.remove('mpoles')
headers.remove('ign_rad')
headers.remove('ign_amp')
for h in headers:
	print 'h: ' + str(h) + ', leni: ' + str(len(intsini[h])) + ', lenf: ' + str(len(intsfin[h]))

for h in headers:
	data_ini[h] = np.array([float(s) for s in intsini[h]])
	data_fin[h] = np.array([float(s) for s in intsfin[h]])

# Put masses in units of Msun
gpermsun = 1.988435e33 # grams/Msun
for h in headers:
	if h.find('mass') != -1:
		data_ini[h] = data_ini[h]/gpermsun
		data_fin[h] = data_fin[h]/gpermsun
		
# Enforce the above in a plot format dictionary corresponding to data
pltfmt = OrderedDict([])
pltfmt['color'] = ['red' for i in xrange(0,nentries_brendan)]+['blue' for i in xrange(0,nentries_cone)]
pltfmt['marker'] = ['*' for i in xrange(0,nentries_brendan)]+['D' for i in xrange(0,nentries_cone)]
pltfmt['linestyle'] = ['None' for i in xrange(0,nentries_brendan+nentries_cone)]

# Plot final variables vs. initial burned mass for all cases
for h in headers:
	data = OrderedDict([])
	plt.figure(1)
	fig = plt.gcf()
	csp = CustomScatterplot(fig)
	data['y'] = data_fin[h]
	data['x'] = data_ini['mass burned']
	csp.splot(data,'x','y',pltfmt)
	fig = csp.getfig()
	mlco = mlines.Line2D([], [], color='red', marker='*', markersize=5, label='CO (Brendan)')
	mlcone = mlines.Line2D([],[],color='blue',marker='D', markersize=5, label='CONe Hybrid')
	plt.legend(handles=[mlco,mlcone],bbox_to_anchor=(1.0,1.0),bbox_transform=plt.gcf().transFigure,prop={'size':7})
	plt.xlabel('Initial Mass Burned ($M_\\odot$)')
	plt.ylabel(h + ' at 4s')
	plt.title('CO vs. CONe Models')
	plt.savefig(h.replace(' ','_') + '.eps')
	plt.clf()

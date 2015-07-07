from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
from CustomScatterplot import CustomScatterplot

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

# Reorganize the data into a single dictionary for plotting ease
# Convert strings to numbers
data = OrderedDict([])
data['iniMassBurned'] = np.array([float(s) for s in intsini['mass burned']])
data['finMassNi56'] = np.array([float(s) for s in intsfin['estimated Ni56 mass']])
data['finMassNSE'] = np.array([float(s) for s in intsfin['mass burned to NSE']])
data['finEkinetic'] = np.array([float(s) for s in intsfin['E_kinetic (from vel)']])
data['mpoles'] = intsini['mpoles']
data['ign_rad'] = intsini['ign_rad']
data['ign_amp'] = intsini['ign_amp']

# Put masses in units of Msun
gpermsun = 1.988435e33 # grams/Msun
data['iniMassBurned'] = data['iniMassBurned']/gpermsun
data['finMassNi56'] = data['finMassNi56']/gpermsun
data['finMassNSE'] = data['finMassNSE']/gpermsun

# Do some plotting....
## I want marker shapes specifying mpole, colors specifying amplitude 
## So set up the color palette and marker shapes.
## The amplitudes are: 3, 6, 12, 24, 36, 48, 60, 72, 84, 100 (x1e5)
## Mpoles are: 2, 4, 6, 8
ampColors = OrderedDict([])
ampColors['100'] = 'black'
ampColors['84'] = 'gray'
ampColors['72'] = 'purple'
ampColors['60'] = 'magenta'
ampColors['48'] = 'green'
ampColors['36'] = 'lightgreen'
ampColors['24'] = 'darkorange'
ampColors['12'] = 'gold'
ampColors['6'] = 'red'
ampColors['3'] = 'salmon'

mpoleColors = OrderedDict([])
mpoleColors['20'] = 'black'
mpoleColors['18'] = 'gray'
mpoleColors['16'] = 'purple'
mpoleColors['14'] = 'magenta'
mpoleColors['12'] = 'green'
mpoleColors['10'] = 'lightgreen'
mpoleColors['8'] = 'darkorange'
mpoleColors['6'] = 'gold'
mpoleColors['4'] = 'red'
mpoleColors['2'] = 'salmon'

mpoleMarkers = OrderedDict([])
mpoleMarkers['2'] = 's' # squares
mpoleMarkers['4'] = 'D' # diamonds
mpoleMarkers['6'] = '*' # stars
mpoleMarkers['8'] = 'o' # circles
mpoleMarkers['12'] = '.' # points

ampMarkers = OrderedDict([])
ampMarkers['6'] = 's' # squares
ampMarkers['12'] = 'D' # diamonds
ampMarkers['24'] = '*' # stars
ampMarkers['36'] = 'o' # circles
ampMarkers['48'] = '.' # points

# Enforce the above in a plot format dictionary corresponding to data
pltfmt = OrderedDict([])
pltfmt['color'] = [mpoleColors[a.split('e')[0]] for a in data['mpoles']]
pltfmt['marker'] = [ampMarkers[m.split('e')[0]] for m in data['ign_amp']]
pltfmt['linestyle'] = ['None' for i in xrange(0,nentries)]

### Note, I don't know whether the above or below is more or less efficient
#for i in xrange(0,nentries):
#	for k,v in ampColors.iteritems():
#		if data['ign_amp']==k:
#			pltfmt['color'].append(v)
#	for k,v in mpoleMarkers.iteritems():
#		if data['mpoles']==k:
#			pltfmt['marker'].append(v)
#	pltfmt['linestyle'].append('None')

# Plot final NSE mass vs. initial burned mass for all cases
plt.figure(1)
fig = plt.gcf()
csp = CustomScatterplot(fig)
csp.splot(data,'iniMassBurned','finMassNSE',pltfmt)
fig = csp.getfig()
plt.xlabel('Initial Mass Burned ($M_\\odot$)')
plt.ylabel('Final Mass Burned to NSE ($M_\\odot$)')
plt.title('Final NSE Mass Trend')


plt.figure(2)
fig = plt.gcf()
csp = CustomScatterplot(fig)
csp.splot(data,'iniMassBurned','finMassNi56',pltfmt)
fig = csp.getfig()
plt.xlabel('Initial Mass Burned ($M_\\odot$)')
plt.ylabel('Estimated Ni56 Yield ($M_\\odot$)')
plt.title('Ni56 Yield')

plt.figure(3)
fig = plt.gcf()
csp = CustomScatterplot(fig)
csp.splot(data,'finMassNSE','finMassNi56',pltfmt)
fig = csp.getfig()
plt.xlabel('Final Mass Burned to NSE ($M_\\odot$)')
plt.ylabel('Estimated Ni56 Yield ($M_\\odot$)')
plt.title('Final Ni56 and NSE Mass Trends')

plt.figure(4)
fig = plt.gcf()
csp = CustomScatterplot(fig)
csp.splot(data,'iniMassBurned','finEkinetic',pltfmt)
fig = csp.getfig()
plt.xlabel('Initial Mass Burned ($M_\\odot$)')
plt.ylabel('Final Kinetic Energy')
plt.title('Final Kinetic Energy Trends')

plt.figure(5)
fig = plt.gcf()
csp = CustomScatterplot(fig)
csp.splot(data,'finEkinetic','finMassNi56',pltfmt)
fig = csp.getfig()
plt.xlabel('Final Kinetic Energy (erg)')
plt.ylabel('Estimated Ni56 Yield ($M_\\odot$)')
plt.title('Kinetic Energy and Ni56 Trends')

plt.show()

from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str, help='Name of input integral file to plot.')
args = parser.parse_args()

intdataname = args.infile

ints = OrderedDict([])
ncols = 0
cols = []
nentries = 0

# Read the data from this integral file
fint = open(intdataname,'r')
# get headers
h = fint.readline().lstrip().lstrip('#')
ncols = 0
hs = h.rstrip('\n').split('  ')
for hi in hs:
	if (hi != ''):
		cols.append(hi.strip())	
		ncols = ncols + 1
                # prepare column data structures
for c in cols:
	ints[c] = []
        # read data points
for l in fint:
	if l=='# simulation restarted\n':
		continue
	srow = l.split()
	for i in range(0,ncols):
		ints[cols[i]].append(srow[i])

fint.close()

# Convert strings to numbers
data = OrderedDict([])
for k in ints.keys():
        v = ints[k]
        data[k] = np.array([float(s) for s in v])

# Reorganize so leg N data overwrite data from leg N-1
data_o = OrderedDict([])
for k in ints.keys():
	data_o[k] = []

for i in range(0,len(data['time'])-1):
	# determine if this time is later than any future time, if so, ignore
	later = False
	for t in data['time'][i+1:]:
		if data['time'][i] > t:
			later = True
			break
	if not later:
		for k in data.keys():
			data_o[k].append(data[k][i])

for k in data.keys():
	data_o[k].append(data[k][-1]) 

for k in data_o.keys():
        v = data_o[k]
        data[k] = np.array(v) # now data contains the reorganized integral qtys

# Put masses in units of Msun
gpermsun = 1.988435e33 # grams/Msun
for k in data.keys():
        v = data[k]
        if k.find('mass')!=-1:
	        data[k] = v/gpermsun


# Plot all variables vs. time
nplot = 1
for k in data.keys():
        v = data[k]
        if k!='time':
                plt.figure(nplot)
                fig = plt.gcf()
                ax = fig.add_axes([0.1,0.1,0.8,0.8])
                ax.plot(data['time'],data[k])
                plt.xlabel('time (s)')
                plt.ylabel('$\mathrm{' + k + '}$')
                plt.title(k + ' vs. Time')
                # plt.tight_layout()
                # plt.save(k + '.png')
                # plt.clf()
                pp = PdfPages(k.replace(' > ','>').replace(' < ','<').replace(' ','_') + '.pdf')
                pp.savefig()
                pp.close()
                nplot += 1

#plt.figure(1)
#fig = plt.gcf()
#csp = CustomScatterplot(fig)
#csp.splot(data,'iniMassBurned','finMassNSE',pltfmt)
#fig = csp.getfig()
#plt.xlabel('Initial Mass Burned ($M_\\odot$)')
#plt.ylabel('Final Mass Burned to NSE ($M_\\odot$)')
#plt.title('Final NSE Mass Trend')

#plt.show()

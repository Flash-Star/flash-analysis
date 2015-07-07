from IntegralFlashData import IntegralFlashData
from CustomPlot import CustomPlot
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict
import sys

av = sys.argv
impa = '24'
if len(av)==2:
	impa = str(int(av[1]))

pbi = [2, 4, 6, 8, 12, 16, 20]
pbir = [str(p) for p in pbi]
colors = ['purple','magenta','green','lightgreen','darkorange','gold','red']
pref = 'profile75_mpole-'
suff = '_r-35e6_a-' + impa + 'e5_ordered.dat'
ifd = IntegralFlashData()

# Make a dictionary for the data
ifdata = OrderedDict([])
pfmt = OrderedDict([])
headers = []
shortheaders = []
for i in xrange(0,len(pbir)):
    p = pbir[i]
    iname = pref + p + suff
    ifd.readInts(iname)
#    ifd.orderData()
    ifd.GramsToMsun()
    ifdata[p] = ifd.getArrayData()
    if i==0:
	headers = ifdata[p].keys()
	shortheaders = [hj.replace(' > ','>').replace(' ','_') for hj in headers]
    pfmt[p] = {'color': colors[i],
               'marker': None,
               'linestyle': '-',
		'label':p}
    ifd.clrArrayData()

# Plot relevant data
for j in xrange(0,len(headers)):
	hj = headers[j]
	hs = shortheaders[j]
	if hs!='time':
		plt.figure(1)
		fig = plt.gcf()
		cp = CustomPlot(fig)
		h = cp.splot(ifdata,'time',hj,pfmt)
		fig = cp.getfig()
		plt.legend(handles=h,bbox_to_anchor=(1.0,0.7),bbox_transform=plt.gcf().transFigure,prop={'size':10})
		plt.xlabel('time (s)')
		if hj.find('mass')!=-1:
			yl = hj + ' ($M_\\odot$)'
		else:
			yl = hj
		plt.ylabel(yl)
		plt.title(hj + ' For ignMpoleA=' + impa + 'e5, pbIgnRho=10^7.2')
		plt.savefig(hs + '_mp-2' + suff.rstrip('_ordered.dat') + '.eps')
		plt.clf()

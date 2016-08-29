from IntegralFlashData import IntegralFlashData
from CustomPlot import CustomPlot
from ColorPicker import ColorPicker
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib as mpl
from collections import OrderedDict
import sys
import os
import glob as glob

# matplotlib rc parameters
mpl.rcParams['font.size'] = 14.0

# Define some data structures
ifdata = OrderedDict([])
pfmt = OrderedDict([])

# Store the current directory
this_dir = os.getcwd()

## Read in the CO integrals
#realz_dir = '/home/dwillcox/400k/analysis/cf_brendan' # absolute path
realz_dir = '/home/eugene/simulations/flash_runs/hybrid-cone/hddt/v3/profile75/ign_true/400k/analysis/cf_brendan_pbIgnRho-7.2'
#pref = 'Realization_'
pref = '400k_Tc7e8_co_wd_R'
suff = '_ordered.dat'
os.chdir(realz_dir)

# Make a dictionary for the data
ifd = IntegralFlashData()
headers = []
shortheaders = []
rflist = glob.glob(pref + '*' + suff)
N = len(rflist)
print 'Found this many CO files: ' + str(N)

cpick = ColorPicker()
colors = cpick.pickColors(N)
first = True
for fn in rflist:
    print fn
    ni = int(fn.replace(pref,'').replace(suff,''))
    ifd.readInts(fn)
    ifd.GramsToMsun()
    ifdk = 'co_' + str(ni)
    ifdata[ifdk] = ifd.getArrayData()
    if first:
	headers = ifdata[ifdk].keys()
	shortheaders = [hj.replace(' > ','>').replace(' ','_') for hj in headers]
    pfmt[ifdk] = {'color': 'blue',
               'alpha': 0.75,
               'marker': None,
               'linestyle': '-',
               'linewidth': 0.5,
               'label': None}
    ifd.clrArrayData()

co_r_keys = ifdata.keys()

# Read the mean now
ifd.readInts('mean.dat')
ifd.GramsToMsun()
ifdata['co_mean'] = ifd.getArrayData()
pfmt['co_mean'] = {'color': 'orange',
                  'marker': None,
                  'linestyle': '-',
                  'linewidth': 2.0,
                  'label': None}
ifd.clrArrayData()

os.chdir(this_dir)

## Read in the CONE integrals
#cone_dir = '/home/dwillcox/400k/analysis/new-pbIgnRho-7.2/cone_integrals' #absolute path
cone_dir = '/home/eugene/simulations/flash_runs/hybrid-cone/hddt/v3/profile75/ign_true/400k/analysis/new-pbIgnRho-7.2/cone_integrals'
os.chdir(cone_dir)
glob_pattern = 'profile75*_ordered.dat'
cone_files = glob.glob(glob_pattern)
print 'Found this many CONE files: ' + str(len(cone_files))

n = 0
cone_r_keys = []
for cf in cone_files:
    print cf
    ifd_n = 'cone_' + str(n)
    n += 1
    ifd.clrArrayData()
    ifd.readInts(cf)
    ifd.GramsToMsun()
    cone_r_keys.append(ifd_n)
    ifdata[ifd_n] = ifd.getArrayData()
    pfmt[ifd_n] = {'color': 'green',
                   'marker': None,
                   'alpha':0.75,
                   'linestyle': '-',
                   'linewidth': 0.5,
                   'label': None}

# Read the mean file
ifd.clrArrayData()
ifd.readInts('mean.dat')
ifd.GramsToMsun()
ifdata['cone_mean'] = ifd.getArrayData()
pfmt['cone_mean'] = {'color': 'red',
                       'marker': None,
                       'linestyle': '-',
                       'linewidth': 2.0,
                       'label': None}

os.chdir(this_dir)

plot_order = co_r_keys + cone_r_keys + ['co_mean','cone_mean']
ifdata_po = OrderedDict((k,ifdata[k]) for k in plot_order)
pfmt_po = OrderedDict((k,pfmt[k]) for k in plot_order)

# Plot relevant data
for j in xrange(0,len(headers)):
	hj = headers[j]
	hs = shortheaders[j]
	if hs!='time':
		print 'plotting: hj=' + str(hj)
		plt.figure(1)
		fig = plt.gcf()
		cp = CustomPlot(fig)
		h = cp.splot(ifdata_po,'time',hj,pfmt_po)
		fig = cp.getfig()
                handles_rzs = mlines.Line2D([],[],color='blue',alpha=0.75,
                                            linestyle='-',linewidth=2.0,
                                            label='CO WD Realizations')
                handles_rzm = mlines.Line2D([],[],color='orange',linestyle='-',linewidth=2.0,
                                            label='CO WD Mean Values')
                handles_cones = mlines.Line2D([],[],color='green',alpha=0.75,
                                            linestyle='-',linewidth=2.0,
                                            label='CONe WD Realizations')
                handles_conem = mlines.Line2D([],[],color='red',linestyle='-',linewidth=2.0,
                                            label='CONe WD Mean Values')
                h = [handles_rzs,handles_rzm,handles_cones,handles_conem]

                loc_legend_plots = {'E_internal':1,
					'E_nuc' :1,
					'E_internal+kinetic' :1,
					'maximum density': 1,
					'mass with dens > 1e6': 1,
					'mass': 3,
					'y-momentum': 3}
		try:
			plt.legend(handles=h,loc=loc_legend_plots[hj],prop={'size':10})
		except KeyError:
			plt.legend(handles=h,loc=4,prop={'size':10})

#		plt.legend(handles=h,bbox_to_anchor=(1.0,1.0),bbox_transform=plt.gcf().transFigure,prop={'size':7})
		plt.xlabel('Time (s)')

                hjs = hj.split(' ')
		hj = ''
		for hjsi in hjs:
                        if hjsi != 'NSQE' and hjsi != 'NSE':
                            hj = hj + hjsi.capitalize() + ' '
                        else:
                            hj = hj + hjsi + ' '
		hj = hj.rstrip()
                hj = hj.replace('+','$+$')
		hj = hj.replace('>','$>$')
		hj = hj.replace('_',' ')
		if hj.find('Mass')!=-1:
			yl = hj + ' ($M_\\odot$)'
		else:
			yl = hj
		plt.ylabel(yl)
		#plt.title(hj + ' (DDT Density = 10^7.2 g/cc)')
                plt.title(hj)
		plt.savefig(hs + '.pdf')
		plt.clf()

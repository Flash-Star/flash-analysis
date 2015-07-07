from IntegralFlashData import IntegralFlashData
from CustomPlot import CustomPlot
from ColorPicker import ColorPicker
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib as mpl
from collections import OrderedDict
import re
import sys
import os
import glob as glob

# matplotlib rc parameters
#mpl.rcParams['font.size'] = 14.0

# Common objects 
ifd = IntegralFlashData()
headers = []
shortheaders = []
stats_co = OrderedDict([])
stats_cone = OrderedDict([])
which_stats = ['mean','median','min','max','std']

# Store the current directory
this_dir = os.getcwd()

## Read in the CO integral stats
realz_dir = '/home/dwillcox/400k/analysis/cf_brendan' # absolute path
prefix = ''
suffix = '.dat'
os.chdir(realz_dir)

for ws in which_stats:
	ifd.readInts(prefix + ws + suffix,convert_g_to_msun=True)
	stats_co[ws] = ifd.getArrayData()

## Read in the CONE integral stats
cone_dir = '/home/dwillcox/400k/analysis/new-pbIgnRho-7.2/cone_integrals' #absolute path
os.chdir(cone_dir)
prefix = ''
suffix = '.dat'

for ws in which_stats:
	ifd.readInts(prefix + ws + suffix,convert_g_to_msun=True)
	stats_cone[ws] = ifd.getArrayData()

# Get headers
headers = stats_co[which_stats[0]].keys()
shortheaders = [hj.replace(' > ','>').replace(' ','_') for hj in headers]

os.chdir(this_dir)

# Get labels and titles for the plots
header_labels = {}
header_titles = {}
flab = open('axes_labels.txt','r')
# eat header
flab.readline()
for l in flab:
	ls = l.split(':')
	flab_h = ls[0].strip()
	flab_l = ls[1].strip()
	flab_t = ls[2].strip()
	header_labels[flab_h] = flab_l
	header_titles[flab_h] = flab_t
flab.close()

# Plot relevant data
for j in xrange(0,len(headers)):
	hj = headers[j]
	hs = shortheaders[j]
	if hs!='time':
		plt.figure(1)
		fig = plt.gcf()
                ax = fig.add_axes([0.1,0.1,0.8,0.8])

                # Plot CO Range (Shaded)
                y1 = stats_co['min'][hj]
                y2 = stats_co['max'][hj]
		#y1 = stats_co['mean'][hj]-stats_co['std'][hj]
		#y2 = stats_co['mean'][hj]+stats_co['std'][hj]
                print y1
		print y2
		print 'y1 shape: '
		print len(y1)
                print 'y2 shape: '
		print len(y2)
		print len(stats_co['mean']['time'])
                ax.fill_between(stats_co['mean']['time'],y1,y2,
                                where=y2>y1,interpolate=True,facecolor='blue',
				linewidth=0.0,alpha=0.5)
                # Plot CONE Range (Shaded)
                y1 = stats_cone['min'][hj]
                y2 = stats_cone['max'][hj]
#		y1 = stats_cone['mean'][hj]-stats_cone['std'][hj]
#		y2 = stats_cone['mean'][hj]+stats_cone['std'][hj]
                ax.fill_between(stats_cone['mean']['time'],y1,y2,
                                where=y2>y1,interpolate=True,facecolor='green',
				linewidth=0.0,alpha=0.5)
                # Plot CO Mean
                ax.plot(stats_co['mean']['time'],stats_co['mean'][hj],color='orange',linestyle='-',linewidth=2.0)
                # Plot CONE Mean
                ax.plot(stats_cone['mean']['time'],stats_cone['mean'][hj],color='red',linestyle='-',linewidth=2.0)


#                handles_rzs = mlines.Line2D([],[],color='blue',alpha=0.5,
#                                            linestyle='-',linewidth=2.0,
#                                            label='CO ' + r'$\pm 1 \sigma$')
#                handles_rzm = mlines.Line2D([],[],color='orange',linestyle='-',linewidth=2.0,
#                                            label='CO Average')
#                handles_cones = mlines.Line2D([],[],color='green',alpha=0.5,
#                                            linestyle='-',linewidth=2.0,
#                                            label='CONe '+r'$\pm 1 \sigma$')
#                handles_conem = mlines.Line2D([],[],color='red',linestyle='-',linewidth=2.0,
#                                            label='CONe Average')
                
		handles_rzs = mlines.Line2D([],[],color='blue',alpha=0.5,
                                            linestyle='-',linewidth=2.0,
                                            label='CO Range')
                handles_rzm = mlines.Line2D([],[],color='orange',linestyle='-',linewidth=2.0,
                                            label='CO Average')
                handles_cones = mlines.Line2D([],[],color='green',alpha=0.5,
                                            linestyle='-',linewidth=2.0,
                                            label='CONe Range')
                handles_conem = mlines.Line2D([],[],color='red',linestyle='-',linewidth=2.0,
                                            label='CONe Average')
                
		h = [handles_rzs,handles_rzm,handles_cones,handles_conem]
		loc_legend_plots = {'\AE[_]internal\Z':1,
					'\AE[_]nuc\Z' :1,
					'\AE[_]internal[+]kinetic\Z' :1,
					'\Amaximum density\Z': 1,
					'\Amass with dens [>] .*': 1,
#					'mass with dens > 1e6': 1,
					'\Amass\Z': 3,
					'\Aminimum flame density\Z': 1,
					'\Ay[-]momentum\Z': 3}
#		try:
#			plt.legend(handles=h,loc=loc_legend_plots[hj],prop={'size':10})
#		except KeyError:
#			plt.legend(handles=h,loc=4,prop={'size':10})
#		plt.legend(handles=h,bbox_to_anchor=(1.0,1.0),bbox_transform=plt.gcf().transFigure,prop={'size':7},loc=2)
		for loc_legend_k,loc_legend_v in loc_legend_plots.iteritems():
			llre = re.compile(loc_legend_k)
			llm = llre.search(hj)
			print 're: ' + loc_legend_k
			print 'key: ' + hj
			print 'match: ' + str(llm)
			if llm:
				plt.legend(handles=h,loc=loc_legend_v,prop={'size':16})
				#plt.legend(handles=h,loc=loc_legend_v)
				break
			else:
				plt.legend(handles=h,loc=4,prop={'size':16})
				#plt.legend(handles=h,loc=4)
		h_xlabel = 'time'
		h_ylabel = hj
		h_title = hj
	#	plt.xlabel('Time (s)')
		plt.xlabel(header_labels[h_xlabel])
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
	#	plt.ylabel(yl)
		plt.ylabel(header_labels[h_ylabel])
		#plt.title(hj + r' (DDT Density = $10^{7.2}$ $g/cc$)')
	#	plt.title(hj)
		plt.title(header_titles[h_title])
		plt.savefig(hs + '.pdf',bbox_inches='tight',pad_inches=0.05)
		plt.clf()

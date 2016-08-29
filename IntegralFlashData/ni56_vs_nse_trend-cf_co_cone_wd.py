from collections import OrderedDict
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from CustomScatterplot import CustomScatterplot

intdataname_brendan = 'ini_fin_integrals_co_rhoddt-7.2.dat'
intdataname_cone = 'ini_fin_integrals_cone.dat'

intsini = OrderedDict([])
intsfin = OrderedDict([])

annotation_font_size = 18

# get headers
def readintfile(fint,intsini,intsfin,which_file):
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
			t_indx = cols.index('time')
			t_fin = float(srow[t_indx])
			if abs(t_fin-4.0)>0.1:
                                if which_file == 'co':
				        print 'Omitting horked, tfin='+str(t_fin)
				        for i in range(0,ncols):
					        intsini[cols[i]].pop()
                                elif which_file == 'cone':
                                        print 'Including horked, tfin='+str(t_fin)
                                        for i in range(0,ncols):
					        intsfin[cols[i]].append(srow[i])

                                else:
                                        print 'Unknown which_file!'
                                        exit()
			else:
				for i in range(0,ncols):
					intsfin[cols[i]].append(srow[i])
                        
                        print 'ini len: ' + str(len(intsini['mass burned']))
                        print 'fin len: ' + str(len(intsfin['mass burned']))
#			for i in range(0,ncols):
#				intsfin[cols[i]].append(srow[i])

# Read the data from the integral files
fint = open(intdataname_brendan,'r')
readintfile(fint,intsini,intsfin,'co')
fint.close()
nentries_brendan = len(intsini['mass burned'])
print 'N_brendan: ' + str(nentries_brendan)
fint = open(intdataname_cone,'r')
readintfile(fint,intsini,intsfin,'cone')
fint.close()
nentries_cone = len(intsini['mass burned']) - nentries_brendan
print 'N_cone: ' + str(nentries_cone)

# Reorganize the data into a single dictionary for plotting ease
# Convert strings to numbers
data = OrderedDict([])
data['iniMassBurned'] = np.array([float(s) for s in intsini['mass burned']])
data['finMassNi56'] = np.array([float(s) for s in intsfin['estimated Ni56 mass']])
data['finMassNSE'] = np.array([float(s) for s in intsfin['mass burned to NSE']])
data['finEkinetic'] = np.array([float(s) for s in intsfin['E_kinetic (from vel)']])

# Put masses in units of Msun
gpermsun = 1.988435e33 # grams/Msun
data['iniMassBurned'] = data['iniMassBurned']/gpermsun
data['finMassNi56'] = data['finMassNi56']/gpermsun
data['finMassNSE'] = data['finMassNSE']/gpermsun

# Enforce the above in a plot format dictionary corresponding to data
pltfmt = OrderedDict([])
pltfmt['color'] = ['red' for i in xrange(0,nentries_brendan)]+['green' for i in xrange(0,nentries_cone)]
pltfmt['marker'] = ['o' for i in xrange(0,nentries_brendan)]+['D' for i in xrange(0,nentries_cone)]
pltfmt['linestyle'] = ['None' for i in xrange(0,nentries_brendan+nentries_cone)]

# Fit lines through final kinetic energy and Ni-56 for all cases
def linearfun(x,m,b):
	return m*x+b

# to do the fits properly, I have to order the data points...
ntotal = len(data['finEkinetic'])
co_nse_ni = [(data['finMassNSE'][i],data['finMassNi56'][i]) for i in xrange(0,nentries_brendan)]
cone_nse_ni = [(data['finMassNSE'][i],data['finMassNi56'][i]) for i in xrange(nentries_brendan,ntotal)]

co_nse_ni_s = sorted(co_nse_ni,key=lambda x: x[0])
cone_nse_ni_s = sorted(cone_nse_ni,key=lambda x: x[0])

co_nse = np.array([x[0] for x in co_nse_ni_s])
co_ni = np.array([x[1] for x in co_nse_ni_s])
cone_nse = np.array([x[0] for x in cone_nse_ni_s])
cone_ni = np.array([x[1] for x in cone_nse_ni_s])

lopt_co, lcov_co = curve_fit(linearfun,co_nse,co_ni)
lerr_co = np.sqrt(np.diag(lcov_co))
lopt_cone, lcov_cone = curve_fit(linearfun,cone_nse,cone_ni)
lerr_cone = np.sqrt(np.diag(lcov_cone))

co_fit_nse = np.linspace(min(co_nse),max(co_nse),100)
co_fit_ni = co_fit_nse*lopt_co[0]+lopt_co[1]
cone_fit_nse = np.linspace(min(cone_nse),max(cone_nse),100)
cone_fit_ni = cone_fit_nse*lopt_cone[0]+lopt_cone[1]


print '____________________________'
print 'Final Ni-56 = M_NSE*m + b: '
print '* CO: m = ' + str(lopt_co[0]) + ', b = ' + str(lopt_co[1])
print '* CONe: m = ' + str(lopt_cone[0]) + ', b = ' + str(lopt_cone[1])

# Plot final NSE mass vs. initial burned mass for all cases
#plt.figure(1)
#fig = plt.gcf()
#csp = CustomScatterplot(fig)
#csp.splot(data,'iniMassBurned','finMassNSE',pltfmt)
#fig = csp.getfig()
#plt.xlabel('Initial Mass Burned ($M_\\odot$)')
#plt.ylabel('Final Mass Burned to NSE ($M_\\odot$)')
#plt.title('Final NSE Mass Trend')
#
#
#plt.figure(2)
#fig = plt.gcf()
#csp = CustomScatterplot(fig)
#csp.splot(data,'iniMassBurned','finMassNi56',pltfmt)
#fig = csp.getfig()
#plt.xlabel('Initial Mass Burned ($M_\\odot$)')
#plt.ylabel('Estimated Ni56 Yield ($M_\\odot$)')
#plt.title('Ni56 Yield')

plt.figure(1)
fig = plt.gcf()
csp = CustomScatterplot(fig)
csp.splot(data,'finMassNSE','finMassNi56',pltfmt)
fig = csp.getfig()
ax=plt.gca()
ax.plot(co_fit_nse,co_fit_ni,linestyle='-',color='orange',alpha=0.9,linewidth=2.0)
ax.plot(cone_fit_nse,cone_fit_ni,linestyle='-',color='blue',alpha=0.9,linewidth=2.0)
mlco = mlines.Line2D([], [], color='red', marker='o', markersize=5, linestyle='None', label='CO Realizations')
mlcone = mlines.Line2D([],[],color='green',marker='D', markersize=5, linestyle='None', label='CONe Realizations')
mlco_fit = mlines.Line2D([],[],color='orange',linestyle='-',linewidth=2.0,label='CO Linear Fit\n' + 
			'Slope: ' + '{0:0.4f}'.format(lopt_co[0]) + r'$\pm$' + '{0:0.4f}'.format(lerr_co[0]) + '\n' + 
			'Intercept: ' + '{0:0.4f}'.format(lopt_co[1]) + r'$\pm$' + '{0:0.4f}'.format(lerr_co[1]))
mlcone_fit = mlines.Line2D([],[],color='blue',linestyle='-',linewidth=2.0,label='CONe Linear Fit\n' + 
			'Slope: ' + '{0:0.4f}'.format(lopt_cone[0]) + r'$\pm$' + '{0:0.4f}'.format(lerr_cone[0]) + '\n' + 
			'Intercept: ' + '{0:0.4f}'.format(lopt_cone[1]) + r'$\pm$' + '{0:0.4f}'.format(lerr_cone[1]))
#mlcone_fit = mlines.Line2D([],[],color='red',linestyle='-',linewidth=2.0,label='CONE Linear Fit')
plt.legend(handles=[mlco,mlco_fit,mlcone,mlcone_fit],loc=2,borderpad=0.2, borderaxespad=0.0, handletextpad=0.0, prop={'size':annotation_font_size})
plt.xlabel('Final Mass Burned to IGE ($\\mathrm{M_\\odot}$)')
plt.ylabel('Estimated $^{56}$Ni Yield ($\\mathrm{M_\\odot}$)')
#plt.title('Final $^{56}$Ni and NSE Mass Trends')

plt.savefig('ni56_vs_nse_mass.pdf',bbox_inches='tight',pad_inches=0.05)

#plt.figure(4)
#fig = plt.gcf()
#csp = CustomScatterplot(fig)
#csp.splot(data,'iniMassBurned','finEkinetic',pltfmt)
#fig = csp.getfig()
#plt.xlabel('Initial Mass Burned ($M_\\odot$)')
#plt.ylabel('Final Kinetic Energy')
#plt.title('Final Kinetic Energy Trends')
#
#plt.figure(5)
#fig = plt.gcf()
#csp = CustomScatterplot(fig)
#csp.splot(data,'finEkinetic','finMassNi56',pltfmt)
#fig = csp.getfig()
#plt.xlabel('Final Kinetic Energy')
#plt.ylabel('Estimated Ni56 Yield ($M_\\odot$)')
#plt.title('Kinetic Energy and Ni56 Trends')
#
#plt.show()

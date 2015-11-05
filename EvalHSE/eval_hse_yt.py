from yt.mods import *
import numpy as np
import pylab as P
import os

filePrefix = 'preSNIa_co_wd_m6.3_uniform_Dr-1k_hdf5_plt_cnt_'
fileSuffix = ['0000','0050','0100','0150','0200','0240']
fileNames = [filePrefix+fS for fS in fileSuffix]

# Lists to hold profiles, labels, and plot specifications.
profiles = []
labels = []

#pf = load(fileNames)
# Loop over each dataset in the time-series.
# Create a data container to hold the whole dataset.
#ad = pf.h.sphere([0.0,0.0,0.0],(2.5e8,"cm"))
# Create a 1d profile of density vs. radius.
#profiles.append(create_profile(ad, ["Radius"],
#                                   fields=["dens"],n=512,
#                                   weight_field=None,
#                                   accumulation=False))
# Add labels
#labels.append("t = %.2f" % pf.current_time)

# Create the profile plot from the list of profiles.
#plot = ProfilePlot.from_profiles(profiles, labels=labels)

# Save the image.
#plot.save()

fig,pax = P.subplots(2)
for fN in fileNames:
	pf = load(fN)
	axcut = 0 # take a line cut along the x axis
	loccut = (0.0,0.0) # place cut ray at origin
	ray = pf.h.ortho_ray(axcut, loccut)
	pax[0].plot(ray['x'], ray['Density'],
		label='t = %.2f' % pf.current_time)
	pax[1].semilogy(ray['x'], ray['Density'],
                label='t = %.2f' % pf.current_time)
pax[0].set_ylabel('Density')
pax[0].set_xlabel('X')
pax[0].set_xlim([0,0.5e8])
pax[0].set_ylim([1e9,4e9])
#pax[0].legend(loc = 'upper right')
pax[1].set_ylabel('Density')
pax[1].set_xlabel('X')
pax[1].set_xlim([0,1e9])
pax[1].legend(loc = 'upper right')
titobj = pax[0].set_title('Density Lineout along x-axis for preSNIa (Dr=1e3, level 11 ref)')
P.tight_layout()
titobj.set_y(1.09)
fig.subplots_adjust(top=0.86) 
P.savefig("preSNIa_mass-ave_Dr-1e3_R11_xsweep_ts_dens.png")


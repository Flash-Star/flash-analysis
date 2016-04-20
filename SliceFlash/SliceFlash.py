#!/usr/bin/env python
import yt # Uses yt-3
import matplotlib
import numpy as np
from matplotlib import pyplot as plt
import argparse

###############################################################################
######### Sample use: the below command takes the given hdf5 file as an input, 
#########               and plots a rectangular region defined by the intervals
#########               from r=[0,10^4 km], z=[-10^4 km, 10^4 km]
######### It guesses the axis scaling to use and produces a 300dpi EPS file.
########### >python SliceFlashComposition.py profile75_mpole-16_r-35e6_a-12e5_hdf5_plt_cnt_0190 -o cone_400k_m16_a12_0190.eps -rd=0.0 -ru=1.0e4 -zd=-1.0e4 -zu=1.0e4


parser = argparse.ArgumentParser()
parser.add_argument("dataset", type=str, 
                    help="Name of the input dataset.")
parser.add_argument("-field", "--field", type=str, default='rgbcomp',
                    help="Name of the dataset field or derived field to plot. To plot a RGB representation of the composition as in the hybrid paper, set this argument to 'rgbcomp'. Default is 'rgbcomp'.")
parser.add_argument("-cmap", "--colormap", type=str, default='jet',
                    help="Name of the matplotlib colormap to use. (If not plotting the composition). For a list of names and examples, see: http://matplotlib.org/examples/color/colormaps_reference.html")
parser.add_argument("-cbar", "--colorbar", type=bool, default=True, help="True/False sets whether or not a colorbar is plotted (if not plotting the composition). Default is True.")
parser.add_argument("-log", "--takelog", type=bool, default=False, help="True/False sets whether or not to plot the base-10 log of the field specified in --field (if not plotting the composition). Default is False.")
parser.add_argument("-rd", "--r_down", type=float, 
                    help="Lower bound of radial (r) coordinate in kilometers.")
parser.add_argument("-ru", "--r_up", type=float, 
                    help="Upper bound of radial (r) coordinate in kilometers.")
parser.add_argument("-zd", "--z_down", type=float, 
                    help="Lower bound of axial (z) coordinate in kilometers.")
parser.add_argument("-zu", "--z_up", type=float, 
                    help="Upper bound of axial (z) coordinate in kilometers.")
parser.add_argument("-dpi", "--dpi", type=int, default=300, 
                    help="DPI at which to produce the output plot.")
parser.add_argument("-rts", "--r_tick_step", type=float, default=0.5, 
                    help="Radial (r) tick step scaled in units of km/f, where scale f is 10^[min(log10(rd), log10(ru))] for nonzero ru and rd. Tick step should be of order ~1 due to auto-scaled axes.")
parser.add_argument("-zts", "--z_tick_step", type=float, default=0.5, 
                    help="Axial (z) tick step scaled in units of km/f, where scale f is 10^[min(log10(zd), log10(zu))] for nonzero zu and zd. Tick step should be of order ~1 due to auto-scaled axes.")
parser.add_argument("-o", "--output", type=str, default="composition.eps", 
                    help="Name of the output EPS file to write.")

args = parser.parse_args()

ds = yt.load(args.dataset)
## Below are the dimensions from the hybrid and CO FLASH runs ... (in cm)
## domain_left_edge = [  0.00000000e+00  -6.55360000e+09   0.00000000e+00]
## domain_right_edge = [  6.55360000e+09   6.55360000e+09   6.28318531e+00]
## The runs were done in cylindrical polar coord (r,z) and the coordinates
## yt will read are (r,z,theta)
slc = ds.slice('theta',0.0) # Get a slice through theta=0.0 rad

## Now setup domain size for making a fixed-resolution buffer (FRB)
#width_km = 65536.0 # Width of slice in km

#### Make a FRB enclosing the rectangle from (r_down, z_down) to (r_up, z_up)
#### Units are in km
r_down = args.r_down
r_up   = args.r_up
z_down = args.z_down
z_up   = args.z_up

#### For setting the axes labels
## Get the axis scaling so tick labels will be numbers of order ~1.
def get_log_km_factor(c_down, c_up):
  tt = []
  for c in [c_down, c_up]:
    if abs(c) > 0.0:
      tt.append(abs(c))
  tt = np.amin(np.log10(np.array(tt)))
  if int(tt) > 1:
    return int(tt)
  else:
    return 0

z_log_km_factor = get_log_km_factor(z_down, z_up)
r_log_km_factor = get_log_km_factor(r_down, r_up)

z_km_factor = 10.0**z_log_km_factor
r_km_factor = 10.0**r_log_km_factor

z_limits = [z_down/z_km_factor, z_up/z_km_factor]
r_limits = [r_down/r_km_factor, r_up/r_km_factor]

r_tick_locations = np.arange(r_limits[0],r_limits[1]+args.r_tick_step,args.r_tick_step)
r_tick_labels = ['$' + '{0:0.1f}'.format(rt) + '$' for rt in r_tick_locations]
z_tick_locations = np.arange(z_limits[0],z_limits[1]+args.z_tick_step,args.z_tick_step)
z_tick_labels = ['$' + '{0:0.1f}'.format(zt) + '$' for zt in z_tick_locations]

#### For setting the resolution and figure size in inches
aspect_z_div_r = (z_up - z_down)/(r_up - r_down)
dpi = args.dpi # Figure resolution desired (in both dimensions)
inches_r = 2.5 # Width of the resulting desired image
inches_z = inches_r*aspect_z_div_r
npix_r = int(dpi*inches_r) # Number of FRB pixels to use in the radial direction 
npix_z = int(dpi*inches_z)
res = (npix_z, npix_r)

## Create a fixed-resolution buffer object with the above parameters
#### Given the geometry, center the plot so the z-axis is the left edge
#### r_down, r_up, z_down, z_up multiplied by 1e5 to convert (km) to data units (cm)
frb = yt.FixedResolutionBuffer(slc,(r_down*1e5, r_up*1e5, z_down*1e5, z_up*1e5),res)

if args.field == 'rgbcomp':
  ## Get a numpy array of shape res for each progress variable
  phfa = np.array(frb['phfa'])
  phaq = np.array(frb['phaq'])
  phqn = np.array(frb['phqn'])

  ## Create an array of shape (npix_z, npix_r, 3) with the RGB values
  ## WHITE: Fuel
  ## RED:   Ash
  ## GREEN: QNSE
  ## BLACK: NSE
  rgb = np.empty((npix_z, npix_r, 3), dtype=float)
  rgb[:,:,0] = 1.0 - phaq[:,:] # Red 
  rgb[:,:,1] = 1.0 - phfa[:,:] + phaq[:,:] - phqn[:,:] # Green 
  rgb[:,:,2] = 1.0 - phfa[:,:] # Blue
else:
  rgb = np.array(frb[args.field]) 
  if args.takelog:
    rgb = np.log10(rgb)
  
## Write the plot
#fig = plt.figure(figsize=(inches_r, inches_z), dpi=dpi)
fig = plt.figure()
#### The following block of commands turns off all axes & labels
#ax = fig.gca()
#ax.set_frame_on(False)
#ax.axes.get_xaxis().set_visible(False)
#ax.axes.get_yaxis().set_visible(False)

#### Set proper axes and labels
ax = fig.gca()
ax.set_ylim(z_limits)
ax.set_xlim(r_limits)
ax.tick_params(axis='both', which='major', pad=5)
ax.tick_params(direction='out')
plt.xticks(r_tick_locations,r_tick_labels)
plt.yticks(z_tick_locations,z_tick_labels)
#Use km_factor to display the axis scale...
ax.set_xlabel('r $\\mathrm{(\\times 10^{' + str(r_log_km_factor) + '} ~ km)}$')
ax.set_ylabel('z $\\mathrm{(\\times 10^{' + str(z_log_km_factor) + '} ~ km)}$', labelpad=-5)

#### Flip the FRB vertically because plt.imshow() puts pixel (0,0) at the 
#### top left corner of the plot instead of the lower left corner.
rgbud = np.flipud(rgb)
#### Plot RGB FRB
imgplot = plt.imshow(rgbud,extent=(r_limits[0], r_limits[1], z_limits[0], z_limits[1]))
if args.field != 'rgbcomp':
  imgplot.set_cmap(args.colormap)
  plt.colorbar()
  
#### Save image
plt.savefig(args.output, bbox_inches='tight',pad_inches=0.06,dpi=dpi)
#plt.savefig(args.output, dpi=dpi)

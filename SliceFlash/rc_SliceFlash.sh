#!/usr/bin/env bash

# For explanations of what other options are available and what they mean, run 'python SliceFlash.py --help'
# First argument to this script is the name of a Flash plotfile to plot
# Second argument to this script is the value of a density contour to plot, e.g. 1.0e7

# Plot the density using the 'jet' colormap
SliceFlash.py $1 -o oflash_dens.eps -rd=0.0 -ru=1.5e4 -zd=-2.0e4 -zu=1.0e4 -field='dens' -cmap='jet'

# Plot the log10(temperature) using the 'hot' colormap
SliceFlash.py $1 -o oflash_logtemp.eps -rd=0.0 -ru=1.5e4 -zd=-2.0e4 -zu=1.0e4 -field='temp' -cmap='hot' -log=True

# Plot the log10(pressure) using the 'Blues' colormap without showing the colorbar
SliceFlash.py $1 -o oflash_logpres.eps -rd=0.0 -ru=1.5e4 -zd=-2.0e4 -zu=1.0e4 -field='pres' -cmap='Blues' -cbar=False -log=True

# Plot the composition 
SliceFlash.py $1 -o oflash_composition.eps -rd=0.0 -ru=1.5e4 -zd=-2.0e4 -zu=1.0e4

# Plot the composition with density contour at $2 g/cm**3
SliceFlash.py $1 -o oflash_composition_dens.eps -rd=0.0 -ru=1.5e4 -zd=-2.0e4 -zu=1.0e4 --densitycontour=1.0e7

# Nice demonstration of density contour. Plot density with a density contour.
SliceFlash.py $1 -o oflash_dens_contour.eps -rd=0.0 -ru=1.5e4 -zd=-2.0e4 -zu=1.0e4 -field='dens' -cmap='spring' --densitycontour=5.0e7 --densitycontourwidth=0.5

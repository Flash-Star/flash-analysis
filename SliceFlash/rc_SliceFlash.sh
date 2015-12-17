# For explanations of what other options are available and what they mean, run 'python SliceFlash.py --help'

# Plot the density using the 'jet' colormap
python SliceFlash.py hse_profile75_4km_hdf5_plt_cnt_0250 -o oflash_dens.eps -rd=0.0 -ru=1.5e4 -zd=-2.0e4 -zu=1.0e4 -field='dens' -cmap='jet'

# Plot the log10(temperature) using the 'hot' colormap
python SliceFlash.py hse_profile75_4km_hdf5_plt_cnt_0250 -o oflash_logtemp.eps -rd=0.0 -ru=1.5e4 -zd=-2.0e4 -zu=1.0e4 -field='temp' -cmap='hot' -log=True

# Plot the log10(pressure) using the 'Blues' colormap without showing the colorbar
python SliceFlash.py hse_profile75_4km_hdf5_plt_cnt_0250 -o oflash_logpres.eps -rd=0.0 -ru=1.5e4 -zd=-2.0e4 -zu=1.0e4 -field='pres' -cmap='Blues' -cbar=False -log=True

# Plot the composition 
python SliceFlash.py hse_profile75_4km_hdf5_plt_cnt_0250 -o oflash_composition.eps -rd=0.0 -ru=1.5e4 -zd=-2.0e4 -zu=1.0e4

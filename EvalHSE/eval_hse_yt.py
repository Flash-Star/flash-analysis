import yt
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from InterpolateDatasets import InterpolateDatasets
from InterpolateDatasets import ElementwiseStats
from scipy.integrate import quadrature
import argparse

########################################################
### This script reads a flash plot file and returns a
### lineout of all or a particular field along the axis specified.
### For a FLASH plt_cnt file with cylindrical (r,z,theta) coordinates:
### ## Axis 0: radial axis
### ## Axis 1: z axis (cyl. axis of symmetry)
### ## Axis 2: theta axis (not useful)

parser = argparse.ArgumentParser()
parser.add_argument('refdataset', type=str, help='Name of the reference dataset.')
parser.add_argument('-cfds','--cfdataset', nargs='*', type=str, help='Name(s) of the datasets to be compared to the reference dataset.', required=False)
parser.add_argument('-axis','--axis',type=int, help='Axis along which to cast the ray. For Cartesian coordinates, (0=x, 1=y, 2=z). For cylindrical coordinates, (0=r, 1=z, 2=theta). Enter 0, 1, or 2.', required=True)
parser.add_argument('-coord','--coordinates',type=int,help='Coordinate system to use. (0=Cartesian, 1=Cylindrical)', required=True)
args = parser.parse_args()

if (args.axis != 0 and args.axis != 1 and args.axis != 2):
        print 'Error: --axis argument must be 0, 1, or 2.'
        exit()
        
dcrt_lu = {'0':'dx','1':'dy','2':'dz'}
dcyl_lu = {'0':'dr','1':'dz','2':'dtheta'}
        
if (args.coordinates == 0):
        interp_daxis = dcrt_lu[str(args.axis)]
elif (args.coordinates == 1):
        interp_daxis = dcyl_lu[str(args.axis)]
else:
        print 'Error: --coordinates argument must be 0 or 1.'
        exit()
interp_axis = interp_daxis[1:]
        
def get_np_ray(ray_ortho,flist):
        global interp_daxis, interp_axis
        dray = {}
        for f in flist:
                #print f
                dray[f] = np.array(ray_ortho[f])
        np_interp_daxis = np.array(ray_ortho[interp_daxis])
        dray[interp_axis] = np.cumsum(np_interp_daxis)-0.5*np_interp_daxis
        return dray
        
ds_ref = yt.load(args.refdataset)
fields = ds_ref.field_list
dray_ref = get_np_ray(ds_ref.ortho_ray(args.axis, (0.0,0.0)),fields)
dict_ref = {interp_axis:np.array(dray_ref[interp_axis])}

################ Setup Plot
plt.figure()
fig = plt.gcf()
ax = fig.add_axes([0.1,0.1,0.8,0.8])
################ End Setup Plot

integrated_residuals = dict([(f,0.0) for f in fields])
        
if args.cfdataset:
        dray_cf_list = []
        for cfds in args.cfdataset:
                ds_cf = yt.load(cfds)
                dray_cf_list.append(get_np_ray(ds_cf.ortho_ray(args.axis, (0.0,0.0)),
                                               fields))
        interpolator = InterpolateDatasets(dray_cf_list,dict_ref)
        dray_interp_list = interpolator.get_interp_list()
        dray_interp_list.append(dray_ref)
        #print dray_interp_list
        estats = ElementwiseStats()
        dray_cf_max = estats.cf_dicts_op(np.maximum, dray_interp_list)
        dray_cf_min = estats.cf_dicts_op(np.minimum, dray_interp_list)
        #print dray_cf_max
        #print dray_cf_min

        ############# Plot max and min
        ax.plot(dray_cf_max[interp_axis],dray_cf_max[('flash', u'dens')],color='red',
                label='max')
        ax.plot(dray_cf_min[interp_axis],dray_cf_min[('flash', u'dens')],color='green',
                label='min')
        ############# End Plot max and min
        
        # Get the sum of the magnitudes of upper residual and the lower residual
        dray_residual_upper = estats.dicts_subtract(dray_cf_max, dray_ref)
        #print dray_residual_upper
        dray_residual_lower = estats.dicts_subtract(dray_ref, dray_cf_min)
        #print dray_residual_lower
        dray_residual_total = estats.dicts_add([dray_residual_upper, dray_residual_lower])

        # Integrate the residual in all fields to estimate the amount of fluctuation
        integrated_residuals = {}
        for k in fields:
                integrated_residuals[k] = np.trapz(dray_residual_total[k],
                                                   dict_ref[interp_axis])
for k in fields:
        print '-----------------------'
        print k
        print integrated_residuals[k]

################ Plot Reference Data
ax.plot(dray_ref[interp_axis],dray_ref[('flash', u'dens')],color='blue',label='ref')
plt.legend()
plt.xlabel('Log10 ' + interp_axis)
plt.ylabel('Log10 ' + 'dens')
ax.set_xscale('log')
ax.set_yscale('log')
plt.savefig('dens_max_min.eps')
################ End Plot Reference Data

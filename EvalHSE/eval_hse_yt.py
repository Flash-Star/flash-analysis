import yt
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from InterpolateDatasets import InterpolateDatasets
from InterpolateDatasets import ElementwiseStats
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
parser.add_argument('-cfdataset','--cfdataset', nargs='*', type=str, help='Name(s) of the datasets to be compared to the reference dataset.', required=False)
parser.add_argument('-axis','--axis',type=int, help='Axis along which to cast the ray. For Cartesian coordinates, (0=x, 1=y, 2=z). For cylindrical coordinates, (0=r, 1=z, 2=theta). Enter 0, 1, or 2.', required=True)
parser.add_argument('-coord','--coordinates',type=int,help='Coordinate system to use. (0=Cartesian, 1=Polar)', required=True)
args = parser.parse_args()

if (args.axis != 0 and args.axis != 1 and args.axis != 2):
        print 'Error: --axis argument must be 0, 1, or 2.'
        exit()
        
crt_lu = {'0':'x','1':'y','2':'z'}
cyl_lu = {'0':'r','1':'z','2':'theta'}
        
if (args.coordinates == 0):
        interp_axis = crt_lu[str(args.axis)]
elif (args.coordinates == 1):
        interp_axis = cyl_lu[str(args.axis)]
else:
        print 'Error: --coordinates argument must be 0 or 1.'
        exit()

ds_ref = yt.load(args.refdataset)
ray_ref = ds_ref.ortho_ray(args.axis, (0.0,0.0))
dict_ref = {interp_axis:ray_ref[interp_axis]}

if args.cfdataset:
        ray_cf_list = []
        for cfds in args.cfdataset:
                ds_cf = yt.load(cfds)
                ray_cf_list.append(ds_cf.ortho_ray(args.axis, (0.0,0.0)))
        interpolator = InterpolateDatasets(ray_cf_list,dict_ref)
        ray_interp_list = interpolator.get_interp_list()
        ray_interp_list.append(ray_ref)
        estats = ElementwiseStats()
        ray_cf_max = estats.cf_dicts_stat(np.maximum, ray_interp_list)
        ray_cf_min = estats.cf_dicts_stat(np.maximum, ray_interp_list)
        # Get the sum of the magnitudes of upper residual and the lower residual
        ## TODO




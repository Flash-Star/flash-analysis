import numpy as np
from scipy import interpolate

class InterpolateDatasets:
    def __init__(self):
        self.dataset_list = []
        self.interp_list = []
        self.dataset_ref = None
        
    def __init__(self,ds_list,ds_ref):
        # ds_list should be a list of dictionaries ds
        # all ds contain the same keys, pointing to 1-D numpy arrays
        # each ds contains one or more dependent variable keys
        # each ds contains only one independent variable key
        # ds_ref is a dictionary containing the independent variable key ikey
        # ds_ref[ikey] is a 1-D numpy array containing the values of ikey.
        self.dataset_list = ds_list
        self.dataset_ref  = ds_ref
        self.interpolate_all()

    def set_dataset_list(self,ds_list):
        self.dataset_list = ds_list

    def set_dataset_ref(self,ds_ref):
        self.dataset_ref = ds_ref

    def get_interp_list(self):
        return self.interp_list

    def interpolate_ds(self,ds_cf,ds_ref):
        ds_interp = {}
        ikey = ds_ref.keys()[0]
        ds_interp[ikey] = ds_ref[ikey]
        for k,v in ds_cf.iteritems():
            if k != ikey:
                ifunc = interpolate.interp1d(ds_cf[ikey],ds_cf[k],kind='linear')
                ds_interp[k] = ifunc(ds_interp[ikey])
        return ds_interp
        
    def interpolate_all(self):
        if not self.dataset_ref:
            print 'No reference dataset.'
            exit()
        else:
            self.interp_list = [self.interpolate_ds(ds_cf) for ds_cf in self.dataset_list]
            

class ElementwiseStats:
    def cf_array_stat(stat_fun, array_list):
        # Takes a list of same-shape numpy arrays and returns the element-wise operation.
        # stat_fun should be a 2-argument numpy element-wise associative comparison function
        # stat_fun could be, e.g. numpy.minimum, numpy.maximum, etc.n
        a_max = array_list[0]
        for a in array_list:
            a_max = stat_fun(a_max,a)
        
    def cf_dicts_stat(stat_fun, dict_list):
        # Takes a list of dictionaries dict_list
        # All dictionaries d in dict_list have the same keys pointing to
        ## numpy arrays of the same shape.
        # Returns a single dictionary with the keys of d containing the element-wise op.
        # stat_fun should be a 2-argument numpy element-wise associative comparison function
        # stat_fun could be, e.g. numpy.minimum, numpy.maximum, etc.
        d_max = {}
        keys = dict_list[0].keys()
        for k in keys:
            d_max[k] = self.cf_array_stat(stat_fun, [d[k] for d in dict_list])

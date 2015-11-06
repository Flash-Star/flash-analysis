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
            self.interp_list = [self.interpolate_ds(ds_cf,self.dataset_ref) for ds_cf in self.dataset_list]
            

class ElementwiseStats:
    def cf_arrays_op(self,stat_fun, array_list):
        # Takes a list of same-shape numpy arrays and returns the element-wise operation.
        # stat_fun should be a 2-argument numpy element-wise associative comparison function
        # stat_fun could be, e.g. numpy.minimum, numpy.maximum, etc. (But NOT, eg. subtract)
        a_stat = array_list[0] # stat_fun must be a function where this makes sense!!!!!!
        for a in array_list:
            a_stat = stat_fun(a_stat,a)
        return a_stat
        
    def cf_dicts_op(self,stat_fun, dict_list):
        # Takes a list of dictionaries dict_list
        # All dictionaries d in dict_list have the same keys pointing to
        ## numpy arrays of the same shape.
        # Returns a single dictionary with the keys of d containing the element-wise op.
        # stat_fun should be a 2-argument numpy element-wise associative comparison function
        # stat_fun could be, e.g. numpy.minimum, numpy.maximum, etc.
        # It must be possible to initialize stat_fun with one of the list elements.
        d_stat = {}
        keys = dict_list[0].keys()
        for k in keys:
            d_stat[k] = self.cf_arrays_op(stat_fun, [d[k] for d in dict_list])
        return d_stat

    def dicts_subtract(self,A,B):
        # Given dictionaries A and B, returns the key-wise A-B.
        d_sub = {}
        keys = A.keys()
        for k in keys:
            d_sub[k] = np.subtract(A[k],B[k])
        return d_sub

    def dicts_add(self,dict_list):
        # Given a list of dictionaries, returns their key-wise sum.
        d_add = dict([(k,np.zeros_like(v)) for k,v in dict_list[0].iteritems()])
        keys = dict_list[0].keys()
        for d in dict_list:
            for k in keys:
                d_add[k] = np.add(d_add[k],d[k])
        return d_add

from IntegralFlashData import IntegralFlashData
import numpy as np
from collections import OrderedDict
import sys

av = sys.argv
impa = '24'
if len(av)==2:
	impa = str(int(av[1]))

pbi = [2, 4, 6, 8, 12, 16, 20]
pbir = [str(p) for p in pbi]
pref = 'profile75_mpole-'
suff = '_r-35e6_a-' + impa + 'e5.dat'
ifd = IntegralFlashData()

# Make a dictionary for the data
ifdata = OrderedDict([])
pfmt = OrderedDict([])
for i in xrange(0,len(pbir)):
    p = pbir[i]
    iname = pref + p + suff
    ifd.readInts(iname)
    ifd.orderData()
    # Compute the binding energy and add it to the integrals
    data = ifd.getArrayData()
    data['E_binding'] = data['E_internal+kinetic'] + data['E_grav']
    ifd.data = data
    ifd.saveOrderedData()
    ifd.clrArrayData()

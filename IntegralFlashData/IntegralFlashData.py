from collections import OrderedDict
import numpy as np

class IntegralFlashData:
        def __init__(self):
                ifilename = ''
                data = OrderedDict([])
	
        def readInts(self,ifname,convert_g_to_msun = False):
                self.clrArrayData()
                self.data = OrderedDict([])
                self.ifilename = ifname
                self.ifile = open(self.ifilename,'r')

                data_str = OrderedDict([])

		# Read the data from this integral file
                # get headers
                cols = []
                h = self.ifile.readline().strip().lstrip('#')
                ncols = 0
                hs = h.split('  ')
                for hi in hs:
                        if (hi != ''):
                                cols.append(hi.strip())	
                                ncols = ncols + 1
                # prepare column data structures
                for c in cols:
                        data_str[c] = []
                # read data points
                for l in self.ifile:
                        if l=='# simulation restarted\n':
                                continue
                        srow = l.split()
                        for i in range(0,ncols):
                                data_str[cols[i]].append(srow[i])
                # close integrals file
                self.ifile.close()

                # Convert strings to numbers
                self.data = OrderedDict([])
                for k,v in data_str.items():
                        self.data[k] = np.array([float(s) for s in v])
		
		# Convert grams to Msun if needed
                if convert_g_to_msun:
                        self.GramsToMsun()
                        
        def orderData(self):
                # Reorganize so leg N data overwrite data from leg N-1
                data_o = OrderedDict([])
                for k in self.data.keys():
                        data_o[k] = []

                for i in xrange(0,len(self.data['time'])-1):
                        # determine if this time is later than any future time
                        later = False
                        for t in self.data['time'][i+1:]:
                                if self.data['time'][i] > t:
                                        later = True
                                        break
                        if not later:
                                for k in self.data.keys():
                                        data_o[k].append(self.data[k][i])

                for k in self.data.keys():
                        data_o[k].append(self.data[k][-1])
                        
                for k,v in data_o.items():
                        self.data[k] = np.array(v) # now data contains the ordered values

        def saveOrderedData(self,ofname=''):
                # By default, just append _ordered to the base integral file name
                if (ofname==''):
                        #basel = self.ifilename.split('.')
                        #base = ''
                        #if len(basel) > 1:
                        #        for b in basel[:-1]:
                        #                base + b + '.'
                        #        base = base.rstrip('.')
                        #else:
                        #        base = basel[0]
                        base = self.ifilename.rstrip('.dat')
                        ofname = base + '_ordered.dat'
                # Now open the output file and write the ordered data
                of = open(ofname,'w')
                for k in self.data.keys():
                        of.write(k + '  ')
                of.write('\n')
                nentries = 0
                for k in self.data.keys():
                        nentries = len(self.data[k])
                        break
                for i in xrange(0,nentries):
                        for k in self.data.keys():
                                of.write('{:1.14e}'.format(self.data[k][i]) + '  ')
                        of.write('\n')
                of.close()

        def GramsToMsun(self):
                self.data = self.getArrayData()
                gpermsun = 1.988435e33 # grams/Msun
                for k,v in self.data.items():
                        if (k.find('mass')!=-1):
                                self.data[k] = v/gpermsun

        def getArrayData(self):
                a = OrderedDict([])
                for k,v in self.data.items():
                        a[k] = np.array(v)
                return a

        def clrArrayData(self):
                self.data = OrderedDict([])

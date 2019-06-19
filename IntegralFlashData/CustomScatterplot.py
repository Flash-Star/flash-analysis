from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt

class CustomScatterplot:
	# Given a figure and an OrderedDict containing a set of 1D numpy arrays 
	# corresponding to data fields, a pair of dictionary keys 
	# specifying the x and y-axes, and an OrderedDict containing plot 
	# formatting commands for each point, 
	# return a pyplot figure object with the plot.
	def __init__(self,f):
		self.fig = f
		self.ax1 = self.fig.add_axes([0.1,0.1,0.8,0.8])
	def clear(self):
		self.fig.clf()
	def splot(self,data,xaxis,yaxis,pfmt):
		# Expect color and marker specifications for each point
		# in pfmt['color'], pfmt['marker'], and pfmt['linestyle'], etc.
		## Get the number of points to use
		npts = 0
		for k,v in data.items():
			npts = len(v)
			break
		for i in range(0,npts):
			fargs = {}
			for k,v in pfmt.items():
				fargs[k] = v[i]
			self.ax1.plot(data[xaxis][i],data[yaxis][i],**fargs)
	def getfig(self):
		return self.fig
				

		

'''Plots historgams of adversity fields by ER status'''

from collections import OrderedDict
from datetime import datetime
from getTotals import Counter
from manifest import *
from matplotlib import pyplot
import os
from windowspath import *

class Field():

	def __init__(self, name):
		# Stores data for single histogram
		self.name = name
		self.pos = []
		self.neg = []
		self.none = []
		self.bins = -1
		self.set = set()

	def add(self, er, val):
		# Adds value to approriate list
		if er == "P":
			self.pos.append(val)
		elif er == "N":
			self.neg.append(val)
		else:
			self.none.append(val)
		self.set.add(val)

	def setBins(self):
		# Sets number of bins for plot and returns
		self.bins = len(self.set)
		self.set = None




#-----------------------------------------------------------------------------

class Histograms():

	def __init__(self):
		self.label = ["ER+", "ER-", "None"]
		self.style = "seaborn-deep"
		self.outdir = setPath + os.path.sep + "histograms"
		self.data = {}
		self.__setData__()
		self.__plotHistograms__()

	def __plot__(self, ax, name, d):
		# Adds histogram to figure pane
		ax.set_title(name)
		ax.bar([self.pos, self.neg, self.none], self.bins, label = self.label)
		ax.legend(loc='upper right')

	def __plotHistograms__(self):
		# Plots histograms and saves to svg
		row = 0
		col = 0
		pyplot.style.use(self.style)
		fig, axes = pyplot.subplots(nrows = 5, ncol = 3, sharex=True, sharey=True)
		for k in self.data.keys():
			self.data[k].plot(axes[row, col], count)
			col += 1
			if col == 3:
				# Move to new row
				row += 1
				col = 0
		fig.savefig(self.outfile)

	def __setData__(self):
		# Gets data from Counter class
		c = Counter()
		self.data = c.getPercents()		

def main():
	# Read csv with blanks as NAs
	h = Histograms()

if __name__ == "__main__":
	main()

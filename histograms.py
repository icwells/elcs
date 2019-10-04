'''Plots historgams of adversity fields by ER status'''

from collections import OrderedDict
from datetime import datetime
from getTotals import Counter
from manifest import *
from matplotlib import pyplot
from math import ceil
import os
from windowspath import *

class Histograms():

	def __init__(self):
		self.label = ["ER+", "ER-", "None"]
		self.style = "seaborn-deep"
		self.legend = "upper right"
		self.outdir = checkDir(setPath + "histograms", True)
		self.data = Counter()
		self.__plotHistograms__()

	def __setBins__(self, t):
		# Returns number of bins for hist
		keys = t.setKeys()
		return(min(100, len(keys)))

	def __plot__(self, ax, name, t):
		# Adds histogram to figure pane
		bins = self.__setBins__(t)
		ax.set_title(name)
		ax.bar([t.pos, t.neg, t.control], bins, label = self.label)
		ax.legend(loc=self.legend)

	def __plotFile__(self, filename, keys, columns=1):
		# Plots related fields to single svg
		row = 0
		col = 0
		pyplot.style.use(self.style)
		fig, axes = pyplot.subplots(nrows = ceil(len(keys)/columns), ncol = columns, sharex=True, sharey=True)
		for k in keys:
			self.__plot__(axes[row, col], k, self.data[k])
			col += 1
			if col == columns:
				# Move to new row
				row += 1
				col = 0
		fig.savefig(("{}{}.{}.svg").format(self.outdir, filename, datetime.now().strftime("%Y-%m-%d")))			

	def __plotHistograms__(self):
		# Plots histograms by related fields
		self.__plotFile__("ages", self.data.columns[:5])
		'''self.__plotFile__("sei", self.data.columns[5:9], 2)
		self.__plotFile__("income", self.data.columns[9:11])
		self.__plotFile__("homeValues", self.data.columns[11:])'''

def main():
	# Read csv with blanks as NAs
	h = Histograms()

if __name__ == "__main__":
	main()

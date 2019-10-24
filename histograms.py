'''Plots historgams of adversity fields by ER status'''

from collections import OrderedDict
from datetime import datetime
from getTotals import Counter
from manifest import *
from matplotlib import pyplot, ticker
from numpy import ones_like
import os
from windowspath import *

class PlotAttributes():

	def __init__(self, label, xmin=0, xmax=None, ymin=0, ymax=None):
		# Stores attributes for specific plots
		self.label = label
		self.xmin = xmin
		self.xmax = xmax
		self.ymin = ymin
		self.ymax = ymax		

class Histograms():

	def __init__(self, counter):
		pyplot.style.use("seaborn-deep")
		self.label = ["ER+", "ER-", "Control"]
		self.legend = "upper right"
		self.outdir = checkDir(setPath() + "histograms", True)
		self.axes = {}
		self.data = counter
		self.__setAxes__()
		self.__plotHistograms__()

	def __setAxes__(self):
		# Store unique axes data for each field in dict
		a = "Age (years)"
		np = "Nam Powers Score"
		sei = "Socio-Economic Index"
		i = "Income (US dollars)"
		self.axes["AgeMaD"] = PlotAttributes(a, xmax=85)
		self.axes["MaAgeBr"] = PlotAttributes(a, xmin=10, xmax=55)
		self.axes["AgePaD"] = PlotAttributes(a, xmax=85)
		self.axes["PaAgeBr"] = PlotAttributes(a, xmin=10, xmax=70)
		self.axes["NumSibsDieChildhood"] = PlotAttributes("Number of Siblings", xmax=13)
		self.axes["MergedSEI"] = PlotAttributes(sei, xmax=100)
		self.axes["MergedNP"] = PlotAttributes(np, xmax=1000)
		self.axes["EgoCenIncome"] = PlotAttributes(i)
		self.axes["MaCenIncome_New"] = PlotAttributes(i)
		self.axes["PaCenIncome_New"] = PlotAttributes(i)
		self.axes["HomeValue_Head1940"] = PlotAttributes("1940 Home Value (US dollars)")
		self.axes["RENT_ToHEAD"] = PlotAttributes("Rent (US dollars)", xmin=1)

	def __setWeights__(self, k):
		# Returns list of weights to plot by percent
		t =  self.data.totals[k]
		p = 100 * ones_like(t.pos)/len(t.pos)
		n = 100 * ones_like(t.neg)/len(t.neg)
		c = 100 * ones_like(t.control)/len(t.control)
		return [p, n, c]

	def __trimList__(self, k, l):
		# Trims given list an returns
		l.sort()
		if self.axes[k].xmin != 0:
			for i in range(len(l)):
				if l[i] >= self.axes[k].xmin:
					l = l[i:]
					break
		if self.axes[k].xmax is not None:
			for i in range(len(l)-1, 0, -1):
				if l[i] <= self.axes[k].xmax:
					l = l[:i]
					break
		return l

	def __trimLists__(self, k):
		# Removes values greater than xlim from control list
		self.data.totals[k].control = self.__trimList__(k, self.data.totals[k].control)
		self.data.totals[k].pos = self.__trimList__(k, self.data.totals[k].pos)
		self.data.totals[k].neg = self.__trimList__(k, self.data.totals[k].neg)

	def __setBins__(self, k):
		# Returns number of bins and stores xmax for hist
		keys = self.data.totals[k].setKeys()
		if self.axes[k].xmax is None:
			self.axes[k].xmax = max(keys)
		return min(100, len(keys))

	def __plot__(self, k):
		# Adds histogram to figure pane
		print(("\tPlotting {}...").format(k))
		fig, ax = pyplot.subplots(nrows = 1, ncols = 1)
		ax.hist([self.data.totals[k].pos, self.data.totals[k].neg, self.data.totals[k].control], 
				self.__setBins__(k), weights = self.__setWeights__(k), label = self.label)
		ax.set(title = k, ylabel = "Percent Frequency", xlabel = self.axes[k].label)
		ax.set_xlim(0, self.axes[k].xmax)
		ax.yaxis.set_major_formatter(ticker.PercentFormatter())
		#if self.axes[k].ymin != 0 or self.axes[k].ymax is not None:
		#	ax.set_ylim(self.axes[k].ymin, self.axes[k].ymax)
		ax.legend(loc=self.legend)
		fig.savefig(("{}{}.{}.svg").format(self.outdir, k, datetime.now().strftime("%Y-%m-%d")))

	def __plotHistograms__(self):
		# Plots histograms by related fields
		for k in self.data.columns:
			self.data.totals[k].trim(self.axes[k].xmax, self.axes[k].xmin)
			self.__plot__(k)

def main():
	start = datetime.now()
	Histograms(Counter())
	print(("\tTotal runtime: {}\n").format(datetime.now() - start))

if __name__ == "__main__":
	main()

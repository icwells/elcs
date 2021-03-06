'''Plots historgams of adversity fields by ER status'''

from collections import OrderedDict
from datetime import datetime
from getTotals import Counter
from manifest import *
from matplotlib import pyplot, ticker
from numpy import ones_like, arange
import os
from windowspath import *

class PlotAttributes():

	def __init__(self, label, xmin=0, xmax=None, bins=1):
		# Stores attributes for specific plots
		self.label = label
		self.xmin = xmin
		self.xmax = xmax
		# Number to multiply len of data points by
		self.bins = bins

def setAxes(allLabels=True):
	# Store unique axes data for each field in dict
	ret = {}
	a = "Age (years)"
	np = "Nam Powers Score"
	sei = "Socio-Economic Index"
	i = "Income (US dollars)"
	ret["AgeMaD"] = PlotAttributes(a, xmin=1, xmax=85)
	ret["MaAgeBr"] = PlotAttributes(a, xmin=10, xmax=55)
	ret["AgePaD"] = PlotAttributes(a, xmin=1, xmax=85)
	ret["PaAgeBr"] = PlotAttributes(a, xmin=10, xmax=70)
	ret["NumSibs"] = PlotAttributes("Number of Siblings", xmax=28)
	ret["SibsDieKnown"] = PlotAttributes("Number of Siblings Died", xmax=13)
	ret["MergedSEI"] = PlotAttributes(sei, xmax=100)
	ret["MergedNP"] = PlotAttributes(np, xmax=1000)
	if allLabels:
		ret["EgoCenIncome"] = PlotAttributes(i)
		ret["MaCenIncome_New"] = PlotAttributes(i)
		ret["PaCenIncome_New"] = PlotAttributes(i)
		ret["HomeValue_Head1940"] = PlotAttributes("1940 Home Value (US dollars)")
		ret["RENT_ToHEAD"] = PlotAttributes("Rent (US dollars)")
		ret["byrBin"] = PlotAttributes("Birth Year Decade Bin (1888-1994)")
		ret["Complete"] = PlotAttributes("Number of Complete Records")
		ret["AgeFirstBirth"] = PlotAttributes("Age at First Birth", bins=1.15)
		ret["AgeLastBirth"] = PlotAttributes("Age at Last Birth", bins=1.15)
		ret["MaxParity"] = PlotAttributes("Max Parity")
	return ret	

class Histograms():

	def __init__(self, counter):
		pyplot.style.use("seaborn-deep")
		self.label = ["ER+", "ER-", "Control"]
		self.legend = "upper right"
		self.outdir = checkDir(setPath() + "histograms", True)
		self.axes = setAxes(True)
		self.data = counter
		self.na = {"p": [], "n": [], "c": []}
		self.__plotHistograms__()

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
		if self.axes[k].xmin is not None:
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
		return min(100, int(len(keys)*self.axes[k].bins))

	def __plot__(self, k):
		# Adds histogram to figure pane
		print(("\tPlotting {}...").format(k))
		fig, ax = pyplot.subplots(nrows = 1, ncols = 1)
		ax.hist([self.data.totals[k].pos, self.data.totals[k].neg, self.data.totals[k].control], 
				self.__setBins__(k), weights = self.__setWeights__(k), label = self.label)
		ax.set(title = k, ylabel = "Percent Frequency", xlabel = self.axes[k].label)
		ax.set_xlim(0, self.axes[k].xmax)
		ax.yaxis.set_major_formatter(ticker.PercentFormatter())
		ax.legend(loc=self.legend)
		fig.savefig(("{}{}.{}.svg").format(self.outdir, k, datetime.now().strftime("%Y-%m-%d")))

	def __plotNA__(self):
		# Plots barplot of NA values by field and NA Status
		print("\tPlotting NAs...")
		width = 0.3
		ticks = arange(len(self.data.columns))
		fig, ax = pyplot.subplots(nrows = 1, ncols = 1)
		# Plot each field
		ax.bar(ticks-width, self.na["p"], width, label = self.label[0])
		ax.bar(ticks, self.na["n"], width, label = self.label[1])
		ax.bar(ticks+width, self.na["c"], width, label = self.label[2])
		# Add labels and tick marks
		ax.set(title = "Percent NAs", ylabel = "Percent Frequency")
		ax.set_xticks(ticks)
		ax.set_xticklabels(self.data.columns, rotation='vertical')
		ax.yaxis.set_major_formatter(ticker.PercentFormatter())
		ax.legend(loc = "upper left")
		fig.subplots_adjust(bottom=0.4)
		fig.savefig(("{}NApercents.{}.svg").format(self.outdir, datetime.now().strftime("%Y-%m-%d")))

	def __plotHistograms__(self):
		# Plots histograms by related fields
		for k in self.data.columns:
			nas = self.data.totals[k].getNA()
			self.na["p"].append(nas[0])
			self.na["n"].append(nas[1])
			self.na["c"].append(nas[2])
			if k != "TeenMa":
				self.__trimLists__(k)
				self.__plot__(k)
		self.__plotNA__()

def main():
	start = datetime.now()
	Histograms(Counter())
	print(("\tTotal runtime: {}\n").format(datetime.now() - start))

if __name__ == "__main__":
	main()

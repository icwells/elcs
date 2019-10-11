'''Plots historgams of adversity fields by ER status'''

from collections import OrderedDict
from datetime import datetime
from getTotals import Counter
from manifest import *
from matplotlib import pyplot, ticker
from numpy import ones_like
import os
from windowspath import *

class Histograms():

	def __init__(self):
		pyplot.style.use("seaborn-deep")
		self.label = ["ER+", "ER-", "Control"]
		self.legend = "upper right"
		self.outdir = checkDir(setPath() + "histograms", True)
		self.axes = {}
		self.data = Counter()
		self.__setAxes__()
		self.__plotHistograms__()

	def __setAxes__(self):
		# Store unique axes data for each field in dict
		a = "Age (years)"
		np = "Nam Powers Score"
		sei = "Socio-Economic Index"
		i = "Income (US dollars)"
		v = "1940 Home Value (US dollars)"
		self.axes["AgeMaD"] = [a, 85]
		self.axes["MaAgeBr"] = [a, 55]
		self.axes["AgePaD"] = [a, 85]
		self.axes["PaAgeBr"] = [a, 55]
		self.axes["NumSibsDieChildhood"] = ["Number of Siblings", 13]
		self.axes["MaCenNamPow"] = [np, 1000]
		self.axes["MaCenSEI"] = [sei, 100]
		self.axes["PaCenNamPow"] = [np, 1000]
		self.axes["PaCenSEI"] = [sei, 100]
		self.axes["EgoCenIncome"] = [i, None]
		self.axes["MaCenIncome_New"] = [i, None]
		self.axes["PaCenIncome_New"] = [i, None]
		self.axes["HomeValue1940_New"] = [v, None]
		self.axes["PaHomeValue1940_New"] = [v, None]
		self.axes["MaHomeValue1940_New"] = [v, None]

	def __setWeights__(self, k):
		# Returns list of weights to plot by percent
		t =  self.data.totals[k]
		p = 100 * ones_like(t.pos)/len(t.pos)
		n = 100 * ones_like(t.neg)/len(t.neg)
		c = 100 * ones_like(t.control)/len(t.control)
		return [p, n, c]

	def __trimList__(self, k, l):
		# Trims given list an returns
		idx = -1
		l.sort()
		for i in range(len(l)-1, 0, -1):
			if l[i] <= self.axes[k][1]:
				break
			idx = i
		if idx > 0:
			l = l[:idx]
		return l

	def __trimLists__(self, k):
		# Removes values greater than xlim from control list
		self.data.totals[k].control = self.__trimList__(k, self.data.totals[k].control)
		self.data.totals[k].pos = self.__trimList__(k, self.data.totals[k].pos)
		self.data.totals[k].neg = self.__trimList__(k, self.data.totals[k].neg)

	def __setBins__(self, k):
		# Returns number of bins and xlim for hist
		keys = self.data.totals[k].setKeys()
		return min(100, len(keys)), max(keys)

	def __plot__(self, k):
		# Adds histogram to figure pane
		print(("\tPlotting {}...").format(k))
		bins, xl = self.__setBins__(k)
		if self.axes[k][1] is not None:
			if xl > self.axes[k][1]:
				self.__trimLists__(k)
			xl = self.axes[k][1]
		w = self.__setWeights__(k)
		fig, ax = pyplot.subplots(nrows = 1, ncols = 1)
		ax.hist([self.data.totals[k].pos, self.data.totals[k].neg, self.data.totals[k].control], bins, weights = w, label = self.label)
		ax.set_xlim(0, xl)
		ax.set(title = k, ylabel = "Percent Frequency", xlabel = self.axes[k][0])
		ax.yaxis.set_major_formatter(ticker.PercentFormatter())
		ax.legend(loc=self.legend)
		fig.savefig(("{}{}.{}.svg").format(self.outdir, k, datetime.now().strftime("%Y-%m-%d")))

	def __plotHistograms__(self):
		# Plots histograms by related fields
		for k in self.data.columns:
			self.__plot__(k)

def main():
	start = datetime.now()
	Histograms()
	print(("\tTotal runtime: {}\n").format(datetime.now() - start))

if __name__ == "__main__":
	main()

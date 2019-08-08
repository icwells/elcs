'''Plots historgams of adversity fields by ER status'''

from collections import OrderedDict
from datetime import datetime
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

	def plot(self, ax, count):
		# Adds histogram to figure pane
		ax.set_title(self.name)
		ax.hist([self.pos, self.neg, self.none], self.bins, label = ["ER+", "ER-", "None"])
		ax.legend(loc='upper right')


#-----------------------------------------------------------------------------

class Histograms():

	def __init__(self):
		self.infile = getMergedFile()
		self.outfile = os.path.join(os.path.split(self.infile)[0], "adversityHistograms.svg")
		self.case = -1
		self.er = -1
		self.head = {}
		self.data = OrderedDict()
		self.__setData__()
		self.__plotHistograms__()

	def __plotHistograms__(self):
		# Plots histograms and saves to svg
		row = 0
		col = 0
		pyplot.style.use("seaborn-deep")
		fig, axes = pyplot.subplots(nrows = 5, ncol = 3, sharex=True, sharey=True)
		for k in self.data.keys():
			self.data[k].plot(axes[row, col], count)
			col += 1
			if col == 3:
				# Move to new row
				row += 1
				col = 0
		fig.savefig(self.outfile)

	def __setHead__(self, row):
		# Sets relevant header indeces
		columns = ["AgeMaD", "MaAgeBr", "AgePaD", "PaAgeBr", "NumSibsDieChildhood", "MaCenNamPow",
				 "MaCenSEI", "PaCenNamPow", "PaCenSEI", "EgoCenIncome", "MaCenIncome_New", 
				"PaCenIncome_New", "HomeValue1940_New", "PaHomeValue1940_New", "MaHomeValue1940_New"]
		for idx, i in enumerate(row):
			if i in columns:
				self.head[i] = idx
			elif i == "Case":
				self.case = idx
			elif i == "ER":
				self.er = idx
		for i in columns:
			# Initialize data dict keys
			self.data[i] = Field(i)

	def __setData__(self):
		# Reads appropriate info from input file
		first = True
		print("\n\tReading input file...")
		with open(self.infile, "r") as f:
			for line in f:
				if first == False:
						row = line.split(d)
						if len(row) > self.case and row[self.case] == "1":
							# Case is last column
							er = row[self.er].strip()
							if er:
								for k in self.data.keys():
									self.data[k].add(er, row[self.head[k]].strip())
				else:
					d = getDelim(line)
					self.__setHead__(line.split(d))
					first = False

def main():
	# Read csv with blanks as NAs
	h = Histograms()

if __name__ == "__main__":
	main()

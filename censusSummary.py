'''Calculates summary statistics for census 1940 variables'''

from argparse import ArgumentParser
from collections import OrderedDict
from datetime import datetime
from manifest import getCensusFiles, setPath
import os
from pandas import DataFrame, ExcelWriter
from statistics import mean, stdev
from windowspath import *

class Variable():

	def __init__(self):
		self.missing = 0
		self.vals = []

	def add(self, val):
		# Adds value to struct
		val = val.strip()
		try:
			self.vals.append(float(val))			
		except ValueError:
			self.missing += 1

	def toList(self, name, total):
		# Returns measures as formatted list
		ret = [name]
		if len(self.vals) != 0:
			ret.append(mean(self.vals))
			if len(self.vals) > 1:
				for i in [stdev(self.vals), min(self.vals), max(self.vals)]:
					ret.append(str(i))
			else:
				ret.extend(["0", str(self.vals[0]), str(self.vals[0])])
			ret.append("{0:.2%}".format(self.missing/total))
		else:
			ret.extend(["0", "0", "0", "0", "100%"])
		return ret

class Summary():

	def __init__(self):
		self.columns = ["HIGRADE_1940", "FAMSIZE_1940", "INCNONWG_1940", "BPLSTR_1940", "HRSWORK1_1940", "HRSWORK2_1940", "OWNERSHP_1940", "VALUEH_1940", "FARM_1940"]
		self.delim = ","
		self.header = ["Variable", "Mean", "StdDev", "Min", "Max", "Missing"]
		self.infiles = getCensusFiles()
		self.labels = ["case", "control"]
		self.outfile = "{}Census_1940Summary.xlsx".format(setPath())
		self.total = 0
		self.variables = {}
		self.__setVariables__()

	def __setVariables__(self):
		# Adds variables to dict
		print("\n\tInitializing variable structs...")
		for l in self.labels:
			self.variables[l] = OrderedDict()
			for i in ["", "Pa", "Ma"]:
				for k in self.columns:
					self.variables[l]["{}{}".format(i, k)] = Variable()

	def getSummary(self):
		# Calculates summary statistics for case/control input files
		print("\tSummarizing target variables...")
		for l in self.labels:
			first = True
			for line in readFile(self.infiles[l], True, self.delim):
				if not first:
					self.total += 1
					for k in self.variables[l].keys():
						self.variables[l][k].add(line[header[k]])
				else:
					header = line
					first = False

	def getDFs(self):
		# Converts variable classes to lists in-place
		ret = {}
		for l in self.labels:
			rows = []
			for k in self.variables[l]:
				rows.append(self.variables[l][k].toList(k, self.total))
			ret[l] = DataFrame(rows, columns = self.header)
		return ret

	def write(self):
		# Writes values to excel file
		print("\tWriting to file...")
		dfs = self.getDFs()
		with ExcelWriter(self.outfile, mode = "w") as writer:
			for l in self.labels:
				dfs[l].to_excel(writer, sheet_name = l)

def main():
	start = datetime.now()
	parser = ArgumentParser("Calculates summary statistics for census 1940 variables.")
	args = parser.parse_args()
	s = Summary()
	s.getSummary()
	s.write()
	print(("\tTotal runtime: {}\n").format(datetime.now() - start))

if __name__ == "__main__":
	main()

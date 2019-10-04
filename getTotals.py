'''Prints frequencies of adversity measures to csv'''

import os
from collections import OrderedDict
from datetime import datetime
from manifest import *
from numpy import zeros
from pandas import DataFrame, ExcelWriter
from windowspath import *

class Total():

	def __init__(self):
		self.pos = []
		self.neg = []
		self.control = []

	def add(self, status, val):
		# Adds value to appropriate dict
		if status == "P":
			self.pos.append(val)
		elif status == "N":
			self.neg.append(val)
		else:
			self.control.append(val)

	def setKeys(self):
		# Get sorted list of all keys
		l = ["Totals"].extend(self.pos)
		l.extend(self.neg)
		keys = set(l.extend(self.control))
		keys = list(keys)	
		keys.sort()
		return keys

	'''def __calculatePercent__(self, n, d):
		# Calculates percentage
		ret = 0
		if d > 0 and n > 0:
			ret = n/d
		return ret

	def setPercents(self):
		# Returns dict of percents
		ret = OrderedDict()
		keys = self.__setKeys__()
		for k in keys:
			ret[k] = [0, 0, 0]
			if k in self.pos.keys():
				ret[k][0] = self.__calculatePercent__(self.pos[k], self.poscount)
			if k in self.neg.keys():
				ret[k][1] = self.__calculatePercent__(self.neg[k], self.negcount)
			if k in self.control.keys():
				ret[k][2] = self.__calculatePercent__(self.control[k], self.concount)'''

	def getDF(self):
		# Converts to data frame
		col = ["ER+", "ER-", "Control"]
		keys = self.setKeys()
		ret = DataFrame(zeros((len(keys), len(col)), dtype = int), columns = col, index = keys)
		ret.loc["Totals", "ER+"] = len(self.pos)
		ret.loc["Totals", "ER-"] = len(self.neg)
		ret.loc["Totals", "Control"] = len(self.control)
		for k in keys:
			ret.loc[k, "ER+"] = self.pos.count(k)
			ret.loc[k, "ER-"] = self.neg.count(k)
			ret.loc[k, "Control"] = (self.control.count(k)
		return ret

class Counter():

	def __init__(self):
		self.infile = getMergedFile()
		self.outfile = ("{}adversityTotals.{}.xlsx").format(setPath(), datetime.now().strftime("%Y-%m-%d"))
		self.header = {}
		self.totals = {}
		self.columns = ["AgeMaD", "MaAgeBr", "AgePaD", "PaAgeBr", "NumSibsDieChildhood", "MaCenNamPow", "MaCenSEI", "PaCenNamPow", "PaCenSEI", "EgoCenIncome", 
	             "MaCenIncome_New", "PaCenIncome_New", "HomeValue1940_New", "PaHomeValue1940_New", "MaHomeValue1940_New"]
		self.__setFields__()
		self.__getTotals__()

	def __setFields__(self):
		# Sets new dict for each field in self.totals
		for i in self.columns:
			self.totals[i] = Total(self.outdir, i)

	def __parseRow__(self, status, row):
		# Extracts relevant data from row
		for k in self.totals.keys():
			try:
				val = int(row[self.header[k]])
				self.totals[k].add(status, val)
			except:
				pass

	def __getStatus__(self, row):
		# Returns ER status from line
		ret = None
		if len(row) > self.header["Case"]:
			if row[self.header["Case"]].strip() == "1":
				ret = row[self.header["ER"]].strip()
			else:
				ret = "C"
		return ret

	def __getTotals__(self):
		# Counts total occurances for each field by ER status
		first = True
		print("\n\tReading input file...")
		with open(self.infile, "r") as f:
			for line in f:
				line = line.strip()
				if first == False:
					row = line.split(d)
					status = self.__getStatus__(row)
					if status is not None:
						self.__parseRow__(status, row)
				else:
					d = getDelim(line)
					self.header = setHeader(line.split(d))
					first = False

	'''def getPercents(self):
		# Returns dict of percents
		ret = {}
		# column: {value:[p,n,c]}
		for k in self.totals.keys():
			ret[k] = self.totals.setPercents()
		return ret'''

	def writeXLSX(self):
		# Writes each dict to csv
		print("\tWriting table to file...")
		with ExcelWriter(self.outfile) as writer:
			for k in self.totals.keys():
				df = self.totals[k].getDF()
				df.to_excel(writer, sheet_name = k)

def main():
	start = datetime.now()
	c = Counter()
	c.writeXLSX()
	print(("\tTotal runtime: {}\n").format(datetime.now() - start))

if __name__ == "__main__":
	main()

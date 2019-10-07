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
		l = []
		l.extend(self.pos)
		l.extend(self.neg)
		l.extend(self.control)
		keys = set(l)
		keys = list(keys)	
		keys.sort()
		return keys

	def getDF(self):
		# Converts to data frame
		col = ["ER+", "ER-", "Control"]
		keys = self.setKeys()
		keys.insert(0, "Total")
		ret = DataFrame(zeros((len(keys), len(col)), dtype = int), columns = col, index = keys)
		for k in keys:
			ret.loc[k, "ER+"] = self.pos.count(k)
			ret.loc[k, "ER-"] = self.neg.count(k)
			ret.loc[k, "Control"] = self.control.count(k)
		ret.loc["Total"] = ret.sum()
		return ret

class Counter():

	def __init__(self):
		self.infile = getMergedFile()
		self.outfile = ("{}adversityTotals.{}.xlsx").format(setPath(), datetime.now().strftime("%Y-%m-%d"))
		self.header = {}
		self.totals = {}
		self.complete = {"P":0, "N":0, "C":0}
		self.columns = ["AgeMaD", "MaAgeBr", "AgePaD", "PaAgeBr", "NumSibsDieChildhood", "MaCenNamPow", "MaCenSEI", "PaCenNamPow", "PaCenSEI", "EgoCenIncome", 
	             "MaCenIncome_New", "PaCenIncome_New", "HomeValue1940_New", "PaHomeValue1940_New", "MaHomeValue1940_New"]
		self.__setFields__()
		self.__getTotals__()

	def __setFields__(self):
		# Sets new dict for each field in self.totals
		for i in self.columns:
			self.totals[i] = Total()

	def __parseRow__(self, status, row):
		# Extracts relevant data from row
		complete = True
		for idx, k in enumerate(self.columns):
			try:
				val = int(row[self.header[k]])
				self.totals[k].add(status, val)
				if idx < 9 and val < 0:
					complete = False
			except:
				if idx < 9:
					complete = False
		if complete == True:
			self.complete[status] += 1

	def __getStatus__(self, row):
		# Returns ER status from line
		ret = None
		if len(row) > self.header["Case"]:
			if row[self.header["Case"]].strip() == "1":
				s = row[self.header["ER"]].strip()
				if s == "P" or s == "N":
					ret = s
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

	def writeXLSX(self):
		# Writes each dict to csv
		print("\tWriting tables to file...")
		with ExcelWriter(self.outfile) as writer:
			for k in self.totals.keys():
				df = self.totals[k].getDF()
				df.to_excel(writer, sheet_name = k)

	def printComplete(self):
		# Prints number of complete records to the screen
		print("\n\tNumber of complete records:")
		print(("\t\tER+\t{}").format(self.complete["P"]))
		print(("\t\tER-\t{}").format(self.complete["N"]))
		print(("\t\tControl\t{}\n").format(self.complete["C"]))

def main():
	start = datetime.now()
	c = Counter()
	c.writeXLSX()
	c.printComplete()
	print(("\tTotal runtime: {}\n").format(datetime.now() - start))

if __name__ == "__main__":
	main()

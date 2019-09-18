'''Prints frequencies of adversity measures to csv'''

import os
from collections import OrderedDict
from datetime import datetime
from manifest import *
from windowspath import *

class Total():

	def __init__(self, outdir, name):
		self.outfile = os.path.join(outdir, ("{}.csv").format(name))
		self.pos = {}
		self.neg = {}
		self.control = {}
		self.poscount = 0
		self.negcount = 0
		self.concount = 0

	def add(self, status, val):
		# Adds value to appropriate dict
		if status == "P":
			if val not in self.pos.keys():
				self.pos[val] = 0
			self.pos[val] += 1
			self.poscount += 1
		elif status == "N":
			if val not in self.neg.keys():
				self.neg[val] = 0
			self.neg[val] += 1
			self.negcount += 1
		else:
			if val not in self.control.keys():
				self.control[val] = 0
			self.control[val] += 1
			self.concount += 1

	def __setKeys__(self):
		# Get sorted list of all keys
		keys = set()
		for d in [self.pos, self.neg, self.control]:
			for k in d.keys():
				keys.add(k)
		keys = list(keys)	
		keys.sort()
		return keys

	def __calculatePercent__(self, n, d):
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
				ret[k][2] = self.__calculatePercent__(self.control[k], self.concount)

	def writeCSV(self):
		# Writes data to csv
		keys = self.__setKeys__()
		with open(self.outfile, "w") as out:
			out.write("Value,ER+,ER-,Conttol\n")
			out.write(("Totals,{},{},{}\n").format(self.poscount, self.negcount, self.concount))
			for k in keys:
				out.write(("{},{},{},{}\n").format(k, self.pos[k], self.neg[k], self.control[k]))

class Counter():

	def __init__(self):
		self.infile = getMergedFile()
		self.header = {}
		self.totals = {}
		self.outdir = checkDir(os.path.join(setPath(), "totals"), True)
		self.__getTotals__()

	def __setFields__(self):
		# Sets new dict for each field in self.totals
		columns = ["AgeMaD", "MaAgeBr", "AgePaD", "PaAgeBr", "NumSibsDieChildhood", "MaCenNamPow", "MaCenSEI", "PaCenNamPow", "PaCenSEI", "EgoCenIncome", 
	             "MaCenIncome_New", "PaCenIncome_New", "HomeValue1940_New", "PaHomeValue1940_New", "MaHomeValue1940_New"]
		for i in columns:
			self.totals[i] = Total(self.outdir, i)

	def __parseRow__(self, status, row):
		# Extracts relevant data from row
		for k in self.totals.keys:
			try:
				val = int(row[self.header[k]])
				self.totals[k].add(status, val)
			except:
				pass

	def __getStatus__(self, row):
		# Returns ER status from line
		ret = None
		if len(row) > self.header["Case"]:
			if row[self.header["Case"]] == "1":
				ret = row[self.header["ER"]] == "P"
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

	def writeCSVs(self):
		# Writes each dict to csv
		for k in self.totals.keys():
			self.totals[k].writeCSV()

def main():
	start = datetime.now()
	c = Counter()
	c.writeCSVs()
	print(("\tTotal runtime: {}\n").format(datetime.now() - start))

if __name__ == "__main__":
	main()

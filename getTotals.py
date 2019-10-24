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

	def getNA(self):
		# Returns number of NAs by ER status
		ret = []
		ret.append(self.pos.count(-1))
		ret.append(self.neg.count(-1))
		ret.append(self.control.count(-1))
		return ret 

	def add(self, status, val):
		# Adds value to appropriate dict
		if status == "P":
			self.pos.append(val)
		elif status == "N":
			self.neg.append(val)
		else:
			self.control.append(val)

	def __trimList__(self, l, less, greater):
		# Trims given list
		l.sort()
		if less is not None:
			for i in range(len(l)):
				if l[i] >= less:
					l = l[i:]
					break
		if greater is not None:
			for i in range(len(l)-1, 0, -1):
				if l[i] <= greater:
					l = l[:i+1]
					break
		return l

	def trim(self, less=None, greater=None):
		# Removes values greater than greater or less than less from lists
		self.pos = self.__trimList__(self.pos, less, greater)
		self.neg = self.__trimList__(self.neg, less, greater)
		self.control = self.__trimList__(self.control, less, greater)

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
		self.columns = ["AgeMaD", "MaAgeBr", "AgePaD", "PaAgeBr", "NumSibsDieChildhood", "MergedSEI", 
						"MergedNP", "HomeValue_Head1940", "RENT_ToHEAD", "EgoCenIncome", "MaCenIncome_New", "PaCenIncome_New"]
		self.__setFields__()
		self.__getTotals__()

	def __setFields__(self):
		# Sets new dict for each field in self.totals
		for i in self.columns:
			self.totals[i] = Total()

	def __parentAlive__(self, k, row):
		# Determines if given parent is still alive
		if k == "AgeMaD" and row[self.header["MAlive18"]] == "1":
			return True
		elif k == "AgePaD" and row[self.header["PAlive18"]] == "1":
			return True
		return False

	def __parseRow__(self, status, row):
		# Extracts relevant data from row
		complete = True
		end = 4
		for idx, k in enumerate(self.columns):
			try:
				val = int(row[self.header[k]])
			except ValueError:
				# Record NAs
				val = -1
			self.totals[k].add(status, val)
			if idx < end and val < 0 and not self.__parentAlive__(k, row):
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

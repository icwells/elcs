'''Counts number of records in file where Ma died before ego age 10.'''

from argparse import ArgumentParser
from datetime import datetime
import os
from windowspath import *

class MaDeath():

	def __init__(self, infile):
		self.h = {}
		self.infile = infile
		self.pa = 0
		self.ma = 0
		self.start = 1904
		self.total = 0
		checkFile(self.infile)

	def __getCol__(self, row, name):
		# Returns column value
		ret = 0
		idx = self.h[name]
		if idx < len(row):
			val = row[idx].strip()
			if val is not None:
				try:
					ret = int(val)
				except ValueError:
					pass
		return ret

	def __countMaDeath__(self, row):
		# Counts number of records where ma died before age 10
		birth = self.__getCol__(row, "byr")
		if birth > self.start:
			# Ignore records from before 1904
			md = self.__getCol__(row, "MaDyr")
			pd = self.__getCol__(row, "PaDyr")
			if 0 <= md - birth <= 10:
				self.ma += 1
			if 0 <= pd - birth <= 10:
				self.pa += 1

	def countCases(self):
		# Reads records from file
		first = True
		ret = []
		print(("\n\tReading {}...").format(self.infile))
		with open(self.infile, "r") as f:
			for line in f:
				self.total += 1
				line = line.strip()
				if first == False:
					row = line.split(d)
					self.__countMaDeath__(row)
				else:
					d = getDelim(line)
					self.h = setHeader(line.split(d))
					first = False

	def printCount(self):
		# Writes number of records found
		print(("\tFound {} total records.").format(self.total))
		print(("\tFound {} records where Ma died before age 10.").format(self.ma))
		print(("\tFound {} records where Pa died before age 10.").format(self.pa))

def main():
	start = datetime.now()
	parser = ArgumentParser("Counts number of records in file where Ma died before ego age 10.")
	parser.add_argument("i", help = "Path to input file.")
	args = parser.parse_args()
	m = MaDeath(args.i)
	m.countCases()
	m.printCount()
	print(("\tTotal runtime: {}\n").format(datetime.now() - start))

if __name__ == "__main__":
	main()

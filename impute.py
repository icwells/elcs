'''Replaces empty values with imputed values'''

from datetime import datetime
from manifest import *


class Impute():

	def __init__(self):
		self.infile = getMergedFile(True)
		self.header = {}
		self.columns = measureColumns()
		self.outfile = ("{}imputedUCRrecords.{}.csv").format(setPath(), datetime.now().strftime("%Y-%m-%d"))
		self.records = {}
		self.measures = {}
		self.totals = {}
		self.__setMeasures__()
		self.__setrecords__()
		self.__calculateMeasures__()

	def __setMeasures__(self):
		# Initializes measures and totals dicts
		for i in self.columns:
			self.measures[i] = []
			self.totals[i] = 0

	def __calculateMeasures__(self):
		# Calculates imputed values for each field

	def __getMeasures__(self, row):
		# Apeends value to list
		for i in self.columns:
			try:
				val = int(row[self.header[i]])
				if val >= 0:
					self.measures[i].append(val)
			except ValueError:
				pass

	def __setrecords__(self):
		# Reads data into dict
		first = True
		print(("\tReading {} file...").format(k))
		with open(self.infile, "r") as f:
			for line in f:
				line = line.strip()
				if first == False:
					s = line.split(d)
					self.records[s[self.header["personid"]]] = s
					self.__getMeasures__(s)
				else:
					d = getDelim(line)
					self.header = self.__correctPersonID__(setHeader(line.split(d)))
					first = False

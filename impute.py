'''Replaces empty values with imputed values'''

from collections import OrderedDict
from copy import deepcopy
from datetime import datetime
from manifest import *
from statistics import mean, stdev
from windowspath import *

class Impute():

	def __init__(self):
		self.header = {}
		self.columns = measureColumns()
		self.outfile = setOutfile("imputedUCRrecords")
		self.totalimputed = setOutfile("imputedTotals")
		self.measures = {}
		self.imputed = OrderedDict()
		self.totals = OrderedDict()
		self.__setMeasures__()
		self.__calculateMeasures__()

	def __setMeasures__(self):
		# Initializes measures and totals dicts
		for i in self.columns:
			self.measures[i] = []
			self.totals[i] = [0, 0]
			self.imputed[i] = "0"

	def __imputeMeasures__(self):
		# Calculates imputed values for each field
		for i in self.columns:
			m = mean(self.measures[i])
			sd = stdev(self.measures[i])
			self.measures[i] = str(m + sd)

	def __getMeasures__(self, row):
		# Appends value to list
		for i in self.columns:
			try:
				val = int(row[self.header[i]])
				if val >= 0:
					self.measures[i].append(val)
			except ValueError:
				pass

	def __calculateMeasures__(self):
		# Reads values from merged file to impute values
		first = True
		print("\tCalculating imputed values...")
		with open(getMergedFile(), "r") as f:
			for line in f:
				line = line.strip()
				if first == False:
					self.__getMeasures__(line.split(d))
				else:
					d = getDelim(line)
					self.header = setHeader(line.split(d))
					first = False
		self.__imputeMeasures__()

#-----------------------------------------------------------------------------

	def __writeTotals__(self):
		# Writes number of imputed records to file
		print("\tWriting total imputed records to file...")
		with open(self.totalimputed, "w") as out:
			out.write("Column,ImputedValue,#Imputed,Total,%\n")
			for k in self.totals.keys():
				p = self.totals[k][0]/self.totals[k][1]
				out.write(("{},{},{},{},{:.2%}\n").format(k, self.measures[k], self.totals[k][0], self.totals[k][1], p))

	def __replaceValues__(self, row):
		# Inserts imputed values where needed
		imp = deepcopy(self.imputed)
		for i in self.columns:
			self.totals[i][1] += 1
			if not row[self.header[i]].strip() or row[self.header[i]] == "-1":
				row[self.header[i]] = self.measures[i]
				imp[i] = "1"
				self.totals[i][0] += 1
		row.extend(list(imp.values()))
		return row

	def __outputHeader__(self, line, d):
		# Appends dummy variable columns to header
		row = line.strip().split(d)
		for i in self.columns:
			row.append("{}_imputed".format(i))
		return d.join(row) + "\n"

	def imputeRecords(self):
		# Replaces missing data with imputed measures
		first = True
		print("\tReplacing missing data with imputed values...")
		with open(self.outfile, "w") as out:
			with open(getMergedFile(True), "r") as f:
				for line in f:
					if first == False:
						line = line.strip()
						s = line.split(d)
						row = self.__replaceValues__(s)
						out.write(",".join(row) + "\n")						
					else:
						d = getDelim(line)
						out.write(self.__outputHeader__(line, d))
						first = False
		self.__writeTotals__()

def main():
	start = datetime.now()
	print("\n\tImputing missing data...")
	i = Impute()
	i.imputeRecords()
	print(("\tFinished. Run time: {}\n").format(datetime.now() - start))

if __name__ == "__main__":
	main()

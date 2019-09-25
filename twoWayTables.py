'''Makes csv of table of value A vs value B'''

from datetime import datetime
from manifest import *
from numpy import zeros
from pandas import DataFrame, ExcelWriter
from windowspath import *

class Tables():

	def __init__(self, x, y):
		self.infile = getMergedFile()
		self.outfile = ("{}adversityTables.{}.xlsx").format(setPath(), datetime.now().strftime("%Y-%m-%d"))
		self.x = x
		self.y = y
		self.d = ""
		self.head = {}
		self.df = None
		self.__setDataFrame__()
		self.__getTable__()
		self.__writeTable__()

	def __writeTable__(self):
		# Writes or appends table to file
		print("\tWriting table to file...")
		m = "w"
		if os.path.isfile(self.outfile):
			m = "a"
		with ExcelWriter(self.outfile, mode = m) as writer:
			self.df.to_excel(writer, sheet_name = self.x)

	def __getTable__(self):
		# Calculates table values
		first = True
		print("\tCalculating table values...")
		with open(self.infile, "r") as f:
			for line in f:
				line = line.strip()
				if first == False:
					s = line.split(self.d)
					if len(s) >= self.head["Case"]:
						try:
							x = str(int(s[self.head[self.x]]))
							y = str(int(s[self.head[self.y]]))
							self.df[x, y] += 1
						except TypeError:
							pass
				else:
					first = False

	def __setDataFrame__(self):
		# Stores columns and indeces for table
		first = True
		col, ind = set(), set()
		print("\tGetting table column and row names...")
		with open(self.infile, "r") as f:
			for line in f:
				line = line.strip()
				if first == False:
					s = line.split(self.d)
					if len(s) >= self.head["Case"]:
						try:
							x = int(s[self.head[self.x]])
							ind.add(str(x))
						except TypeError:
							pass
						try:
							y = int(s[self.head[self.y]])
							col.add(str(y))
						except TypeError:
							pass
				else:
					self.d = getDelim(line)
					self.head = setHeader(line.split(self.d))
					first = False
		col = list(col)
		col.sort()
		ind = list(ind)
		ind.sort()
		# Initialize empty data frame
		self.df = pandas.DataFrame(zeros((len(col), len(ind)), dtype = int), columns = col, rows = ind)

def main():
	start = datetime.now()
	print("\n\tCreating two-way tables...")
	t = Tables("NumSibsDieChildhood", "NumSibs")
	print(("\tTotal runtime: {}\n").format(datetime.now() - start))

if __name__ == "__main__":
	main()

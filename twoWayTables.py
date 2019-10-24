'''Makes csv of table of value A vs value B'''

from datetime import datetime
from manifest import *
from numpy import zeros
from pandas import DataFrame, ExcelWriter
from windowspath import *

class Tables():

	def __init__(self, x, y, mx):
		self.infile = getMergedFile()
		self.outfile = ("{}adversityTables.{}.xlsx").format(setPath(), datetime.now().strftime("%Y-%m-%d"))
		self.x = x
		self.y = y
		self.max = mx
		self.d = ""
		self.head = {}
		self.df = None
		self.illogical = []
		self.__setDataFrame__()
		self.__getTable__()
		self.__writeTable__()
		self.__writeIllogical__()

	def __writeIllogical__(self):
		# Writes list of illogical values to file
		if len(self.illogical) > 1:
			outfile = ("{}{}.Illogical.csv").format(setPath(), self.x)
			with open(outfile, "w") as out:
				for line in self.illogical:
					out.write(",".join(line) + "\n")

	def __writeTable__(self):
		# Writes or appends table to file
		print("\tWriting table to file...")
		m = "w"
		with ExcelWriter(self.outfile, mode = m) as writer:
			self.df.to_excel(writer, sheet_name = self.x)

	def __getValue__(self, v):
		# Returns integer value
		if v.strip() == "":
			ret = 0
		else:
			try:
				ret = int(v)
			except ValueError:
				ret = -1
		return ret

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
						x = self.__getValue__(s[self.head[self.x]])
						y = self.__getValue__(s[self.head[self.y]])
						if x >= 0 and y >= 0:
							if x > y or y > self.max:
								# Record illogical values
								self.illogical.append(s)
							else:
								self.df.loc[x, y] += 1
				else:
					first = False

	def __setDataFrame__(self):
		# Stores columns and indeces for table
		first = True
		col, ind = set(), set()
		col.add(0)
		ind.add(0)
		print("\tGetting table column and row names...")
		with open(self.infile, "r") as f:
			for line in f:
				line = line.strip()
				if first == False:
					s = line.split(self.d)
					if len(s) >= self.head["Case"]:
						try:
							ind.add(int(s[self.head[self.x]]))
						except ValueError:
							pass
						try:
							y = int(s[self.head[self.y]])
							if y <= self.max:
								col.add(y)
						except ValueError:
							pass
				else:
					self.d = getDelim(line)
					header = line.split(self.d)
					self.head = setHeader(header)
					self.illogical.append(header)
					first = False
		col = list(col)
		col.sort()
		ind = list(ind)
		ind.sort()
		# Initialize empty data frame
		self.df = DataFrame(zeros((len(ind), len(col)), dtype = int), columns = col, index = ind)

def main():
	start = datetime.now()
	print("\n\tCreating two-way tables...")
	t = Tables("SibsDieKnown", "NumSibs", 30)
	print(("\tTotal runtime: {}\n").format(datetime.now() - start))

if __name__ == "__main__":
	main()

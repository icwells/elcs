'''Adds UPDB columns for parental age at death and at birth of child'''

from datetime import datetime
from manifest import *
from windowspath import *

class Ages():

	def __init__(self):
		self.infiles = getInfiles()
		self.headers = {}
		self.caseout = ("{}updbCases.{}.csv").format(setPath(), datetime.now().strftime("%Y-%m-%d"))
		self.controlout = ("{}updbControl.{}.csv").format(setPath(), datetime.now().strftime("%Y-%m-%d"))
		self.case = self.__setCases__("case")
		self.control = self.__setCases__("control")

	def __setCases__(self, k):
		# Reads dict of case/control records
		first = True
		ret = []
		print(("\tReading {} file...").format(k))
		with open(self.infiles[k], "r") as f:
			for line in f:
				line = line.strip()
				if first == False:
					ret.append(line.split(d))
				else:
					d = getDelim(line)
					h = setHeader(line.split(d))
					# Store header for later
					self.headers[k] = h
					first = False
		return ret

	def __writeList__(self, outfile, l, header):
		# Writes list to csv
		print(("\tWriting {} records to {}...").format(len(l), getFileName(outfile)))
		with open(outfile, "w") as out:
			out.write(",".join(header) + ",AgeMaD,MaAgeBr,MaD<10,AgePaD,PaAgeBr,PaD<10\n")
			for i in l:
				out.write(",".join(i) + "\n")

#-----------------------------------------------------------------------------

	def __lessThanTen__(self, v):
		# Returns Y if <= 10 when parent died
		if int(v) <= 10:
			return "Y"
		else:
			return "N"

	def __setAge__(self, p, e):
		# Returns string of p-e
		return str(p-e)

	def __getCol__(self, k, c, line):
		# Returns column value/-1
		ret = -1
		val = line[self.headers[k][c]].strip()
		if val is not None and len(val.strip()) == 4:
			try:
				ret = int(val)
			except ValueError:
				pass
		return ret

	def __setAges__(self, l, k):
		# Returns list with parental dates added
		for idx, i in enumerate(l):
			ext = ["NA", "NA", "NA", "NA", "NA", "NA"]
			# Get self, mother's, and father's birth year
			eb = self.__getCol__(k, "byr", i)
			mb = self.__getCol__(k, "MaByr", i)
			pb = self.__getCol__(k, "PaByr", i)
			if eb > 0 and mb > 0 and pb > 0:
				# Get parent death years
				md = self.__getCol__(k, "MaDyr", i)
				if md > 0:
					ext[0] = self.__setAge__(md, eb)
					ext[1] = self.__setAge__(eb, mb)
					ext[2] = self.__lessThanTen__(ext[0])
				pd = self.__getCol__(k, "PaDyr", i)
				if pd > 0:
					ext[3] = self.__setAge__(pd, eb)
					ext[4] = self.__setAge__(eb, pb)	
					ext[5] = self.__lessThanTen__(ext[3])
			l[idx].extend(ext)
		return l

	def getParentalAges(self):
		# Adds parental age columns to output
		self.cases = self.__setAges__(self.case, "case")
		self.__writeList__(self.caseout, self.case, self.headers["case"].keys())
		self.control = self.__setAges__(self.control, "control")
		self.__writeList__(self.controlout, self.control, self.headers["control"].keys())

def main():
	start = datetime.now()
	print("\n\tCalculating parental age in UPDB records...")
	er = Ages()
	er.getParentalAges()
	print(("\tFinished. Run time: {}\n").format(datetime.now() - start))

if __name__ == "__main__":
	main()

'''Adds UPDB columns for measures of adversity'''

from datetime import datetime
from manifest import *
from windowspath import *

class Adversity():

	def __init__(self):
		self.infiles = getInfiles()
		self.headers = {}
		self.income = {}
		self.caseout = ("{}updbCases.{}.csv").format(setPath(), datetime.now().strftime("%Y-%m-%d"))
		self.controlout = ("{}updbControl.{}.csv").format(setPath(), datetime.now().strftime("%Y-%m-%d"))
		self.case = self.__setCases__("case")
		self.control = self.__setCases__("control")
		self.__setScores__()

	def __getTotals__(self, key, l, inc):
		# Totals target columns from given list
		for i in l:
			for k in inc.keys():
				# Isolate each target value
				val = i[self.headers[key][k]].strip()
				try:
					v = float(val)
					inc[k].append(v)
				except ValueError:
					pass
		return inc

	def __setScores__(self):
		# Determines 25% mark for income status measures
		p = 0.25
		inc = {"MaCenNamPow": [], "MaCenSEI": [], "PaCenNamPow": [], "PaCenSEI": [], "EgoCenIncome": [], 
				"MaCenIncome_New": [], "PaCenIncome_New": [], "HomeValue1940_New": [], "PaHomeValue1940_New": [], "MaHomeValue1940_New": []}
		inc = self.__getTotals__("case", self.case, inc)
		inc = self.__getTotals__("control", self.control, inc)
		for k in inc.keys():
			inc[k].sort()
			# Get index at 25% the length of list, set value in dict
			idx = int((len(inc[k])-1)*p)
			self.income[k] = inc[k][idx]

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
		tail = ",AgeMaD,MaAgeBr,MaD<10,AgePaD,PaAgeBr,PaD<10,TeenMa,SibDeath,LowMaSEI,LowMaNP,LowPaSEI,LowPaNP"
		tail += ",LowEgoInc,LowMaInc,LowPaInc,LowEgoHomeVal,LowMaHomeVal,LowPaHomeVal,>5Sibs,AdversityScore\n"
		print(("\tWriting {} records to {}...").format(len(l), getFileName(outfile)))
		with open(outfile, "w") as out:
			out.write(",".join(header) + tail)
			for i in l:
				out.write(",".join(i) + "\n")

#-----------------------------------------------------------------------------

	def __lessThanTen__(self, v):
		# Returns Y if <= 10 when parent died
		if v != "NA" and int(v) <= 10:
			return "1"
		else:
			return "0"

	def __setAge__(self, p, e):
		# Returns string of p-e
		ret = p-e
		if ret >= 0:
			return str(ret)
		else:
			return "NA"

	def __getCol__(self, k, c, line):
		# Returns column value/-1
		ret = -1
		val = line[self.headers[k][c]].strip()
		if val is not None:
			try:
				ret = int(val)
			except ValueError:
				pass
		return ret

	def __getComparison__(self, k, c, line, less=None, greater=None):
		# Performs given comparison, appends to ext and returns adversity point
		ret = self.__getCol__(k, c, line)
		if ret >= 0:
			if less is not None and ret < less:
				ret = 1
			elif greater is not None and ret > greater:
				ret = 1
			else:
				ret = 0
		return ret

	def __getIncomeMeasures__(self, k, line):
		# Returns scores for mother/father income status and mumber of siblings controlling for income status
		ret = []
		n = 0
		manp = self.__getComparison__(k, "MaCenNamPow", line, less=self.income["MaCenNamPow"])
		masei = self.__getComparison__(k, "MaCenSEI", line, less=self.income["MaCenSEI"])
		panp = self.__getComparison__(k, "PaCenNamPow", line, less=self.income["PaCenNamPow"])
		pasei = self.__getComparison__(k, "PaCenSEI", line, less=self.income["PaCenSEI"])
		eci = self.__getComparison__(k, "EgoCenIncome", line, less=self.income["EgoCenIncome"])
		mci = self.__getComparison__(k, "MaCenIncome_New", line, less=self.income["MaCenIncome_New"])
		pci = self.__getComparison__(k, "PaCenIncome_New", line, less=self.income["PaCenIncome_New"])
		ehv = self.__getComparison__(k, "HomeValue1940_New", line, less=self.income["HomeValue1940_New"])
		mhv = self.__getComparison__(k, "MaHomeValue1940_New", line, less=self.income["MaHomeValue1940_New"])
		phv = self.__getComparison__(k, "PaHomeValue1940_New", line, less=self.income["PaHomeValue1940_New"])
		# Give max of one point for low income status per self/parent
		if eci == 1 or ehv == 1:
			n += 1
		if manp == 1 or masei == 1 or mci == 1 or mhv == 1:
			n += 1
		if panp == 1 or pasei == 1 or pci == 1 or phv == 1:
			n += 1
		sibs = self.__getComparison__(k, "NumSibs", line, greater=5)
		if n > 1 and sibs == 1:
			# Only consider large number of siblings adversity if low income
			n += 1
		for i in [manp, masei, panp, pasei, sibs, eci, mci, pci, ehv, mhv, phv]:
			ret.append(str(i))
		return ret, n		

	def __getAges__(self, k, line):
		# Returns age-based calculations
		ret = 0
		ext = ["NA", "NA", "NA", "NA", "NA", "NA", "0"] 
		# Get self, mother's, and father's birth year
		eb = self.__getCol__(k, "byr", line)
		mb = self.__getCol__(k, "MaByr", line)
		pb = self.__getCol__(k, "PaByr", line)
		if eb > 0 and mb > 0 and pb > 0:
			# Get parent death years
			md = self.__getCol__(k, "MaDyr", line)
			if md > 0:
				ext[0] = self.__setAge__(md, eb)
			ext[1] = self.__setAge__(eb, mb)
			ext[2] = self.__lessThanTen__(ext[0])
			if ext[2] == "1":
				ret += 1
			pd = self.__getCol__(k, "PaDyr", line)
			if pd > 0:
				ext[3] = self.__setAge__(pd, eb)
			ext[4] = self.__setAge__(eb, pb)	
			ext[5] = self.__lessThanTen__(ext[3])
			if ext[5] == "1":
				ret += 1
			if ext[1] != "NA" and int(ext[1]) <= 18:
				# Add 1 for teenage mother
				ext[6] = "1"
				ret += 1
		return ext, ret

	def __setMeasures__(self, l, k):
		# Returns list with parental dates added
		for idx, i in enumerate(l):
			ext, total = self.__getAges__(k, i)
			n = self.__getComparison__(k, "NumSibsDieChildhood", i, greater=1)
			ext.append(str(n))
			if n == 1:
				total += n
			lst, n = self.__getIncomeMeasures__(k, i)
			total += n
			ext.extend(lst)
			ext.append(str(total))
			l[idx].extend(ext)
		return l

	def getAdversityScores(self):
		# Adds parental age columns to output
		self.cases = self.__setMeasures__(self.case, "case")
		self.__writeList__(self.caseout, self.case, self.headers["case"].keys())
		self.control = self.__setMeasures__(self.control, "control")
		self.__writeList__(self.controlout, self.control, self.headers["control"].keys())

def main():
	start = datetime.now()
	print("\n\tCalculating parental age in UPDB records...")
	a = Adversity()
	a.getAdversityScores()
	print(("\tFinished. Run time: {}\n").format(datetime.now() - start))

if __name__ == "__main__":
	main()

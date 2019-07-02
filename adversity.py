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
		inc = {"MaCenNamPow": [], "MaCenSEI": [], "PaCenNamPow": [], "PaCenSEI": []}
		inc = self.__getTotals__("case", self.case, inc)
		inc = self.__getTotals__("control", self.control, inc)
		for k in inc.keys():
			inc[k].sort()
			# Get index at 25% the length of list, set value in dict
			idx = int(len(inc[k]-1)*p)
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
		tail = ",AgeMaD,MaAgeBr,MaD<10,AgePaD,PaAgeBr,PaD<10,TeenMa,SibDeath,LowMSEI,LowMNP,LowPSEI,LowPNP,>5Sibs,AdversityScore\n"
		print(("\tWriting {} records to {}...").format(len(l), getFileName(outfile)))
		with open(outfile, "w") as out:
			out.write(",".join(header) + tail)
			for i in l:
				out.write(",".join(i) + "\n")

#-----------------------------------------------------------------------------

	def __lessThanTen__(self, v):
		# Returns Y if <= 10 when parent died
		if int(v) <= 10:
			return "1"
		else:
			return "0"

	def __setAge__(self, p, e):
		# Returns string of p-e
		return str(p-e)

	def __getCol__(self, k, c, line):
		# Returns column value/-1
		ret = -1
		l = 1
		if "yr" in c:
			# Expect 4 digit year
			l = 4
		val = line[self.headers[k][c]].strip()
		if val is not None and len(val.strip()) == l:
			try:
				ret = int(val)
			except ValueError:
				pass
		return ret

	def __getComparison__(self, k, c, line, less=None, greater=None):
		# Performs given comparison, appends to ext and returns adversity point
		ret = self.__getCol__(k, c, line)
		if v >= 0:
			if less is not None and ret < less:
				ret = 1
			elif greater is not None and ret > greater:
				ret = 1
			else:
				ret = 0
		return ret

	def __getIncomeMeasures__(self, k, line):
		# Returns scores for mother/father income status and mumber of siblings controlling for income status
		n = 0
		manp = self.__getComparison__(k, "MaCenNamPow", line, less=self.income["MaCenNamPow"])
		masei = self.__getComparison__(k, "MaCenSEI", line, less=self.income["MaCenSEI"])
		panp = self.__getComparison__(k, "PaCenNamPow", line, less=self.income["PaCenNamPow"])
		pasei = self.__getComparison__(k, "PaCenSEI", line, less=self.income["PaCenSEI"])
		if manp == 1 or masei == 1:
			# Give max of one point for low income status per parent
			n += 1
		if panp == 1 or pasei == 1:
			n += 1
		sibs = self.__getComparison__(k, "NumSibs", line, greater=5)
		if n > 0 and sibs == 1:
			# Only consider large number of siblings adversity if low income
			n += 1
		ret = [str(manp), str(masei), str(panp), str(pasei), str(sibs)]
		return ret, n		

	def __getAges__(self, k, line):
		# Returns age-based calculations
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
			pd = self.__getCol__(k, "PaDyr", line)
			if pd > 0:
				ext[3] = self.__setAge__(pd, eb)
				ext[4] = self.__setAge__(eb, pb)	
				ext[5] = self.__lessThanTen__(ext[3])
			if int(ext[1]) <= 18:
				# Add 1 for teenage mother
				ext[6] = "1"
		return ext

	def __setMeasures__(self, l, k):
		# Returns list with parental dates added
		for idx, i in enumerate(l):
			ext = self.__getAges__(k, i)
			total = int(ext[2]) + int(ext[5]) + int(ext[6])
			total += self.__getComparison__(k, "NumSibsDieChildhood", i, greater=1)
			ext.append(str(n))
			l, n = self.__getIncomeMeasures__(k, i)
			total += n
			ext.extend(l)
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
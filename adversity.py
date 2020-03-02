'''Adds UPDB columns for measures of adversity'''

from datetime import datetime
from histograms import setAxes
from manifest import *
from record import *
from windowspath import *

class Adversity():

	def __init__(self):
		self.infiles = getInfiles()
		self.newcol = newColumns()[:-1]
		self.headers = {}
		self.income = {}
		self.bins = []
		self.limits = setAxes(False)
		self.caseout = setOutfile("updbCases")
		self.controlout = setOutfile("updbControl")
		self.case = self.__setCases__("case")
		self.control = self.__setCases__("control")
		self.diagdate = self.__setDiagnosisDates__()
		self.__setScores__()

	def __getTotals__(self, key, l, inc):
		# Totals target columns from given list
		for i in l:
			# Isolate each target value
			sei = getMax(self.headers[key]["MaCenSEI"], self.headers[key]["PaCenSEI"], i)
			if sei >= 0:
				inc["MergedSEI"].append(sei)
			np = getMax(self.headers[key]["MaCenNamPow"], self.headers[key]["PaCenNamPow"], i)
			if np >= 0:
				inc["MergedNP"].append(np)
			for k in ["EgoCenIncome", "MaCenIncome_New", "PaCenIncome_New", "HomeValue_Head1940"]:
				idx = self.headers[key][k]
				if idx < len(i):
					try:
						v = float(i[idx].strip())
						if v > 0.0:
							inc[k].append(v)
					except ValueError:
						pass
		return inc

	def __setBins__(self):
		# Stores list of birth year decades
		start = 1888
		# Add ten to highest birth year to avoid index error
		stop = 2004
		while start < stop:
			self.bins.append(start)
			start += 10

	def __setScores__(self):
		# Determines 25% mark for income status measures
		p = 0.25
		inc = {"MergedSEI": [], "MergedNP": [], "EgoCenIncome": [], "MaCenIncome_New": [], "PaCenIncome_New": [], "HomeValue_Head1940": []}
		inc = self.__getTotals__("case", self.case, inc)
		inc = self.__getTotals__("control", self.control, inc)
		for k in inc.keys():
			inc[k].sort()
			# Get index at 25% the length of list, set value in dict
			idx = int((len(inc[k])-1)*p)
			self.income[k] = inc[k][idx]
		self.__setBins__()

	def __formatDiagDate__(self, date):
		# Returns formatted year or -1
		ret = -1
		date = date.strip()
		try:
			d = int(date)
			if d > 0:
				ret = d
		except ValueError:
			pass
		return ret

	def __setDiagnosisDates__(self):
		# Stores date of diagnosis from ucr file
		ret = {}
		first = True
		print("\tReading dates from ucr file...")
		with open(self.infiles["ucr"], "r") as f:
			for line in f:
				line = line.strip()
				if first == False:
					s = line.split(d)
					k = s[h["personid"]].strip()
					ret[k] = self.__formatDiagDate__(s[h["DATE_OF_DIAGNOSIS_YYYY"]])
				else:
					d = getDelim(line)
					h = setHeader(line.split(d))
					first = False
		return ret

	def __setCases__(self, k):
		# Reads dict of case/control records
		first = True
		ret = []
		print(("\tReading {} file...").format(k))
		with open(self.infiles[k], "r") as f:
			for line in f:
				# Replace whitespace characters to retain spacing
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
			out.write(("{},{}\n").format(",".join(header), ",".join(self.newcol)))
			for i in l:
				out.write(",".join(i) + "\n")

#-----------------------------------------------------------------------------

	def __birthYearBin__(self, birth):
		# Determines which decade bin birth falls in
		if birth > 0:
			for idx, i in enumerate(self.bins):
				if i <= birth < self.bins[idx+1]:
					return str(idx + 1)
		return "-1"

	def __setMeasures__(self, l, k):
		# Returns list with parental dates added
		h = self.headers[k]
		for idx, i in enumerate(l):
			dd = -1
			pid = i[h["personid"]].strip()
			if pid in self.diagdate.keys():
				dd = self.diagdate[pid]
			rec = UPDBRecord(h, self.newcol, self.income, i, dd)
			l[idx].append(self.__birthYearBin__(rec.birth))
			l[idx].extend(rec.toList(self.limits))
		return l

	def getAdversityScores(self):
		# Adds parental age columns to output
		self.cases = self.__setMeasures__(self.case, "case")
		self.__writeList__(self.caseout, self.case, self.headers["case"].keys())
		self.control = self.__setMeasures__(self.control, "control")
		self.__writeList__(self.controlout, self.control, self.headers["control"].keys())

def main():
	start = datetime.now()
	print("\n\tCalculating adversity scores in UPDB records...")
	a = Adversity()
	a.getAdversityScores()
	print(("\tFinished. Run time: {}\n").format(datetime.now() - start))

if __name__ == "__main__":
	main()

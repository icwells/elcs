'''Adds UPDB columns for measures of adversity'''

from datetime import datetime
from manifest import *
from record import UPDBRecord
from windowspath import *

class Adversity():

	def __init__(self):
		self.infiles = getInfiles()
		self.newcol = ["AgeMaD", "MaAgeBr", "MaD<10", "MAlive18", "TeenMa", "AgePaD", "PaAgeBr", 
					"PaD<10", "PAlive18", "SibDeath", "LowMaSEI", "LowMaNP", "LowPaSEI", "LowPaNP", 
					"LowIncome", "LowHomeVal", ">5Sibs", "AdversityScore"]
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
				idx = self.headers[key][k]
				if idx < len(i):
					val = i[idx].strip()
					if k == "RENT_ToHEAD":
						rent = getRent(val)
						if rent >= 0:
							inc[k].append(rent)
					else:
						try:
							v = float(val)
							inc[k].append(v)
						except ValueError:
							pass
		return inc

	def __setScores__(self):
		# Determines 25% mark for income status measures
		p = 0.25
		inc = {"MaCenNamPow": [], "MaSEI1940": [], "PaCenNamPow": [], "PaSEI1940": [], "EgoCenIncome": [], 
				"MaCenIncome_New": [], "PaCenIncome_New": [], "HomeValue_Head1940": [], "RENT_ToHEAD": []}
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
				line = line.lstrip().replace("\n", "")
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
		length = len(header) + len(tail.split(","))
		print(("\tWriting {} records to {}...").format(len(l), getFileName(outfile)))
		with open(outfile, "w") as out:
			out.write(("{},{}\n").format(",".join(header), ",".join(self.newcol)))
			for i in l:
				if len(i) < length:
					# Ensure empty cells are still present
					for idx in range(length-len(i)-1):
						i.append("")
				out.write(",".join(i) + "\n")

#-----------------------------------------------------------------------------

	def __setMeasures__(self, l, k):
		# Returns list with parental dates added
		for idx, i in enumerate(l):
			rec = UPDBRecords(self.headers[k], self.income, i)
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
	print("\n\tCalculating adversity scores in UPDB records...")
	a = Adversity()
	a.getAdversityScores()
	print(("\tFinished. Run time: {}\n").format(datetime.now() - start))

if __name__ == "__main__":
	main()

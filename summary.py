'''Produces sumamry of total/complete entries per column'''

import os
from datetime import datetime
from argparse import ArgumentParser
from collections import OrderedDict
from windowspath import *

class Summary():

	def __init__(self, infile):
		self.infile = infile
		self.outfile = ""
		self.head = None
		self.header = "Field,Filled,Empty,%Filled,Total\n"
		self.casecontrol = False
		self.casetotal = 0
		self.controltotal = 0
		self.case = OrderedDict()
		self.control = OrderedDict()
		self.__setOutfile__()
		self.__setSummary__()
		self.__writeSummary__()

	def __setOutfile__(self):
		# Stores output file name
		ext = getExt(self.infile)
		path = self.infile[:self.infile.rfind(".")]
		self.outfile = ("{}_summary.{}").format(path, ext)
		if "mergedUCRrecords" in self.infile:
			self.casecontrol = True
			self.header = "Field,CaseFilled,CaseEmpty,Case%Filled,CaseTotal,ControlFilled,ControlEmpty,Control%Filled,ControlTotal\n"

	def __calculateTotal__(self, n, t):
		# Calculates full, empty, total
		return (",{},{},{:.2%},{}").format(n, t-n, n/t, t)

	def __writeSummary__(self):
		# Write complete dict to outfile
		with open(self.outfile, "w") as out:
			out.write(self.header)
			for k in self.case.keys():
				s = self.__calculateTotal__(self.case[k], self.casetotal)
				if self.casecontrol == True:
					s += self.__calculateTotal__(self.control[k], self.controltotal)
				out.write(("{}{}\n").format(k, s))

	def __setKeys__(self):
		# Copies keys from header to complete dict
		for k in self.head.keys():
			if k != "Case":
				self.case[k] = 0
				self.control[k] = 0

	def __countRow__(self, s):
		# Checks each column for entry
		l = len(s)
		if self.casecontrol == False or (l > self.head["Case"] and s[self.head["Case"]] == "1"):
			self.casetotal += 1
			for k in self.case.keys():
				i = s[self.head[k]].strip()
				if i:
					if i != "NA" and i != "-1":
						self.case[k] += 1
		else:
			self.controltotal += 1
			for k in self.control.keys():
				idx = self.head[k]
				if l > idx:
					i = s[idx].strip()
					if i:
						if i != "NA" and i != "-1":
							self.control[k] += 1

	def __setSummary__(self):
		# Counts entires per column in input file
		first = True
		with open(self.infile, "r") as f:
			for line in f:
				line = line.strip()
				if first == False:
					s = line.split(d)
					self.__countRow__(s)
				else:
					d = getDelim(line)
					self.head = setHeader(line.split(d))
					self.__setKeys__()
					first = False

def main():
	start = datetime.now()
	parser = ArgumentParser("")
	parser.add_argument("infile", help = "Path to input file.")
	args = parser.parse_args()
	checkFile(args.infile)
	print(("\n\tSummarizing {}...").format(os.path.split(args.infile)[1]))
	Summary(args.infile)
	print(("\tFinished. Run time: {}\n").format(datetime.now() - start))

if __name__ == "__main__":
	main()

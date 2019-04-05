'''Merges UPDB data with UCR data'''

import os
from datetime import datetime
from manifest import getInfiles
from windowspath import *

class DatabaseMerger():

	def __init__(self):
		self.infiles = getInfiles()
		self.headers = {}
		self.outdir = None
		self.ucr = {}
		self.case = {}
		#self.control = {}
		self.casecontrol = {}
		self.__setInfiles__()
		self.__setPath__()

	def __setPath__(self):
		# Sets path to and outdir
		wd = os.getcwd()
		# Remove possible trailing slash and drop last directory
		wd = wd[:-1]
		self.outdir = wd[:wd.rfind(os.path.sep)+1]

	def __checkInfiles__(self):
		# Makes sure files exist
		for i in self.infiles.keys():
			checkFile(self.infiles[i])

	def __setCases__(self, k):
		# Reads dict of case/control records
		first = True
		ret = {}
		print(("\tReading {} file...").format(k))
		with open(self.infiles[k], "r") as f:
			for line in f:
				if first == False:
					s = line.strip().split(d)
					self.casecontrol[s[h["personid"]]] = s
				else:
					first = True
					d = getDelim(line)
					h = setHeader(line.split(d))
					# Store header for later
					self.headers[k] = h
		return ret

	def __setCaseControl__(self):
		# Reads dict of case/control ids
		first = True
		k = "casecontrols"
		with open(self.infiles[k], "r") as f:
			for line in f:
				if first == False:
					s = line.strip().split(d)
					self.casecontrol[s[h["CaseID"]]] = s[h["controlId"]]
				else:
					first = True
					d = getDelim(line)
					h = setHeader(line.split(d))

#-----------------------------------------------------------------------------

	def __writeList__(self, outfile, l, header):
		# Writes list to csv
		print(("\tWriting {} records to {}...").format(len(l), getFileName(outfile))
		with open(outfile, "w") as out:
			out.write(",".join(header) + "\n")
			for i in l:
				out.write(",".join(i) + "\n")

	def __checkCaseRecords__(self):
		# Compares case eg and person IDs against case/control IDs
		misses = []
		outfile = self.outdir + "missingControl.csv"
		h = self.headers["case"]
		if len(self.casecontrol) != len(self.cases):
			print(("\n\t[Warning] Number of case records {} does not equal case controls: {}\n").format(len(self.casecontrol), len(self.cases))
		for k in self.case.keys():
			egid = self.case[k][h["egid"]]
			if egid not in self.casecontrol.keys() or self.casecontrol[egid] != k or k not in self.ucr.keys():
				misses.append(self.case[k])
				del self.case(k)
		self.__writeList__(outfile, misses, self.headers["case"].values)

	def __mergeCaseRecords__(self):
		# Merges ucr and case records
		outfile = self.outdir + "mergedUCRrecords.csv"
		# Merge headers
		tail = self.headers["ucr"].values
		del tail[self.headers["ucr"]["personid"]]
		header = self.headers["case"].values.extend(tail)
		for k in self.cases.keys():
			row = self.ucr[k]
			# Delete redundant column
			del row[self.headers["ucr"]["personid"]]
			self.cases[k].extend(row)
		self.__writeList__(outfile, self.cases.values, header)

	def merge(self):
		# Merges UCR and UPDB data
		self.__setCaseControl__()
		self.ucr = self.__setCases__("ucr")
		self.cases = self.__setCases__("case")
		self.__checkCaseRecords__()
		#self.control = self.__setCases__("control")

def main():
	start = datetime.now()
	print("\n\tMerging UPDB and UCR records...")
	merger = DatabaseMerger()
	merger.merge()

if __name__ == "__main__":
	main()

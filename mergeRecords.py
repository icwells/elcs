'''Merges UPDB data with UCR data'''

import os
from datetime import datetime
from manifest import getInfiles
from windowspath import *

class CaseID():
	def __init__(self, caseid):
		self.caseid = caseid
		self.total = 0
		self.controlids = set()

	def add(self, controlid):
		# Adds new control id and increments total
		self.total += 1
		self.controlids.add(controlid)

class DatabaseMerger():

	def __init__(self):
		self.infiles = getInfiles()
		self.headers = {}
		self.outdir = None
		self.ucr = {}
		self.case = {}
		self.caseids = {}
		self.__setPath__()

	def __setPath__(self):
		# Sets path to and outdir
		wd = os.getcwd()
		# Remove possible trailing slash and drop last directory
		wd = wd[:-1]
		self.outdir = wd[:wd.rfind(os.path.sep)+1]

	def __setCases__(self, k):
		# Reads dict of case/control records
		first = True
		ret = {}
		print(("\tReading {} file...").format(k))
		with open(self.infiles[k], "r") as f:
			for line in f:
				line = line.strip()
				if first == False:
					s = line.split(d)
					ret[s[h["personid"]]] = s
				else:
					d = getDelim(line)
					h = setHeader(line.split(d))
					# Store header for later
					self.headers[k] = h
					first = False
		return ret

	def __setCaseControl__(self):
		# Reads dict of case/control ids
		first = True
		k = "casecontrol"
		with open(self.infiles[k], "r") as f:
			for line in f:
				line = line.strip()
				if first == False:
					s = line.split(d)
					cid = s[h["CaseID"]]
					if cid not in self.caseids.keys():
						self.caseids[cid] = CaseID(cid)
					self.caseids[cid].add(s[h["controlId"]])
				else:
					d = getDelim(line)
					h = setHeader(line.split(d))
					first = False

#-----------------------------------------------------------------------------

	def __writeList__(self, outfile, l, header):
		# Writes list to csv
		print(("\tWriting {} records to {}...").format(len(l), getFileName(outfile)))
		with open(outfile, "w") as out:
			out.write(",".join(header) + "\n")
			for i in l:
				out.write(",".join(i) + "\n")

	def __checkCaseRecords__(self):
		# Compares case eg and person IDs against case/control IDs
		nocontrol = {}
		nocase = {}
		h = self.headers["case"]
		if len(self.caseids) != len(self.case):
			print(("\n\t[Warning] Number of case records {:,} does not equal case controls: {:,}\n").format(len(self.case), len(self.caseids)))
		for k in self.case.keys():
			if k not in self.caseids.keys() or k not in self.ucr.keys():
				nocontrol[k] = self.case[k]
		for k in nocontrol.keys():
			 # Delete in seperate loop
			del self.case[k]
		for k in self.ucr.keys():
			if k not in self.case.keys():
				nocase[k] = self.ucr[k]
		if len(nocontrol) > 0:
			self.__writeList__(self.outdir + "missingControl.csv", nocontrol.values(), self.headers["case"].keys())
		if len(nocase) > 0:
			self.__writeList__(self.outdir + "missingCase.csv", nocase.values(), self.headers["ucr"].keys())

	def __mergeCaseRecords__(self):
		# Merges ucr and case records
		outfile = self.outdir + "mergedUCRrecords.csv"
		# Merge headers
		header = list(self.headers["case"].keys())
		h = self.headers["ucr"]
		tail = list(h.keys())
		del tail[h["personid"]]
		header.extend(tail)
		for k in self.case.keys():
			row = self.ucr[k]
			# Delete redundant column
			del row[h["personid"]]
			self.case[k].extend(row)
		self.__writeList__(outfile, self.case.values(), header)

	def merge(self):
		# Merges UCR and UPDB data
		self.__setCaseControl__()
		self.ucr = self.__setCases__("ucr")
		self.case = self.__setCases__("case")
		self.__checkCaseRecords__()
		self.__mergeCaseRecords__()

def main():
	start = datetime.now()
	print("\n\tMerging UPDB and UCR records...")
	merger = DatabaseMerger()
	merger.merge()
	print(("\tFinished. Run time: {}\n").format(datetime.now() - start))

if __name__ == "__main__":
	main()

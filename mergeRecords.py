'''Merges UPDB data with UCR data'''

import os
from datetime import datetime
from manifest import *
from windowspath import *

class DatabaseMerger():

	def __init__(self):
		self.infiles = getInfiles(False)
		self.headers = {}
		self.outdir = setPath()
		self.outfile = ("{}mergedUCRrecords.{}.csv").format(setPath(), datetime.now().strftime("%Y-%m-%d"))
		self.ucr = {}
		self.case = {}
		self.control = {}
		self.caseids = set()
		self.controlids = set()

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
		# Reads sets of case/control ids
		first = True
		k = "casecontrol"
		with open(self.infiles[k], "r") as f:
			for line in f:
				line = line.strip()
				if first == False:
					s = line.split(d)
					self.caseids.add(s[h["CaseID"]])
					self.controlids.add(s[h["controlId"]])
				else:
					d = getDelim(line)
					h = setHeader(line.split(d))
					first = False

#-------------------------------ID Comparison---------------------------------

	def __checkIDs__(self, l, s, m1, m2, shared = False):
		# Identifies shared/exclusive ids between l and s and prints total
		count = 0
		for i in l:
			if shared == True and i in s:
				count += 1
			elif shared == False and i not in s:
				count += 1
		if count > 0:
			ins = ""
			if "ids" not in m1:
				ins = "records "
			if shared == False:
				ins += "not "
			print(("\t{:,} {} {}found in {}.").format(count, m1, ins, m2))	

	def __checkKeys__(self, header, outfile, d, s):
		# Identifies ids in d not in s, writes records to outfile, and returns list of ids
		misses = {}
		for k in d.keys():
			if k not in s:
				misses[k] = d[k]
		if len(misses) > 0:
			self.__writeList__(self.outdir + outfile, misses.values(), header)
		return misses.keys()

	def __checkCaseRecords__(self):
		# Compares case eg and person IDs against case/control IDs
		# Compare caseids to case file and control ids to control file
		self.__checkIDs__(self.caseids, set(self.case.keys()), "caseids", "case")
		self.__checkIDs__(self.controlids, set(self.control.keys()), "controlids", "control")
		# Make sure no caseids are in control file
		self.__checkIDs__(self.case.keys(), set(self.control.keys()), "case", "control", True)
		if len(self.caseids) != len(self.case):
			print(("\n\t[Warning] Number of case records {:,} does not equal case controls: {:,}\n").format(len(self.case), len(self.caseids)))
		# Compare case keys to case ids and vice versa
		ids = self.__checkKeys__(self.headers["case"].keys(), "missingControl.csv", self.case, self.caseids)
		for k in ids:
			 # Delete lines with missing data
			del self.case[k]
		# Comapre ucr personids to case file and compare misses to control
		ids = self.__checkKeys__(self.headers["ucr"].keys(), "missingCase.csv", self.ucr, set(self.case.keys()))
		self.__checkIDs__(ids, set(self.control.keys()), "ucr", "control", True)
		for k in ids:
			 # Delete lines with missing data
			del self.ucr[k]		

#-----------------------------------------------------------------------------

	def __writeList__(self, outfile, l, header):
		# Writes list to csv
		print(("\tWriting {} records to {}...").format(len(l), getFileName(outfile)))
		with open(outfile, "w") as out:
			out.write(",".join(header) + "\n")
			for i in l:
				out.write(",".join(i) + "\n")

	def __getHeader__(self):
		# Returns header for output file
		header = list(self.headers["case"].keys())
		h = self.headers["ucr"]
		tail = list(h.keys())
		del tail[h["personid"]]
		header.extend(tail)
		header.append("Case")
		return header

	def __mergeCaseRecords__(self):
		# Merges ucr and case records
		tag = "1"
		for k in self.case.keys():
			if k in self.ucr.keys():
				row = self.ucr[k]
				# Delete redundant column
				del row[self.headers["ucr"]["personid"]]
				self.case[k].extend(row)
				self.case[k].append(tag)

	def __addControls__(self):
		# Adds control records to output list and writes to file
		tag = "0"
		blank = []
		for i in range(len(self.headers["ucr"])-1):
			blank.append(".")
		blank.append(tag)
		res = list(self.case.values())
		for k in self.control.keys():
			row = self.control[k]
			# Add empty spaces to preserve case column placement
			row.extend(blank)
			res.append(row)
		self.__writeList__(self.outfile, res, self.__getHeader__())

	def merge(self):
		# Merges UCR and UPDB data
		self.__setCaseControl__()
		self.ucr = self.__setCases__("ucr")
		self.case = self.__setCases__("case")
		self.control = self.__setCases__("control")
		self.__checkCaseRecords__()
		self.__mergeCaseRecords__()
		self.__addControls__()

def main():
	start = datetime.now()
	print("\n\tMerging UPDB and UCR records...")
	merger = DatabaseMerger()
	merger.merge()
	print(("\tFinished. Run time: {}\n").format(datetime.now() - start))

if __name__ == "__main__":
	main()

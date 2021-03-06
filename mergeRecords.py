'''Merges UPDB data with UCR data'''

import os
from datetime import datetime
from manifest import *
from windowspath import *

class DatabaseMerger():

	def __init__(self):
		self.count = {"Merged": {"case": 0, "control": 0}, "Subset": {"case": 0, "control": 0}}
		self.infiles = getInfiles(False)
		self.headers = {}
		self.header = []
		self.columns = []
		self.outdir = setPath()
		self.outfile = setOutfile("mergedUCRrecords")
		self.subfile = setOutfile("subsetUCRrecords")
		self.incompletefile = setOutfile("incompleteUCRids")
		self.ucr = {}
		self.case = {}
		self.control = {}
		self.subset = {}
		self.incomplete = []
		self.caseids = set()
		self.controlids = set()
		self.year = 1990

	def __correctPersonID__(self, h):
		# Standardizes the personid column
		k = "PersonID"
		if k in h.keys():
			h[k.lower()] = h[k]
			del h[k]
		return h		 

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
					row = line.split(d)
					if k == "case":
						self.header = row
					h = self.__correctPersonID__(setHeader(row))
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
					h = self.__correctPersonID__(setHeader(line.split(d)))
					first = False

	def __setColumns__(self):
		# Stores list of column indeces to subset
		head = setHeader(self.header)
		for i in allColumns():
			if i in head.keys():
				self.columns.append(head[i])

	def __getHeader__(self):
		# Returns header for output file
		c = Columns()
		#self.header = list(self.headers["case"].keys())
		h = self.headers["ucr"]
		tail = list(h.keys())
		del tail[h["personid"]]
		self.header.extend(tail)
		self.header.extend(c.events)

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

	def __subsetColumns__(self, row):
		# Removes uneeded columns from subset entries
		ret = []
		for i in self.columns:
			if i < len(row):
				ret.append(row[i])
		return ret

	def __parentBirthYears__(self, line):
		# Returns True if either parental birth year is present
		for idx in [self.headers["case"]["MaByr"], self.headers["case"]["PaByr"]]:
			if idx < len(line):
				val = line[idx].strip()
				if val is not None:
					try:
						ret = int(val)
						return True
					except ValueError:
						pass
		return False

	def __from1990__(self, k):
		# Returns differnce of date of diangosis from 1990
		ret = "-1"
		col = "DATE_OF_DIAGNOSIS_YYYY"
		if col in self.headers["ucr"].keys():
			idx = self.headers["ucr"][col]
			try:
				val = int(self.ucr[k][idx])
				if val == self.year:
					# Avoid excluding records from 1990
					val = 0.5
				d = val - self.year
				if d > 0:
					ret = str(d)
			except:
				pass
		return ret

	def __getDuration__(self, k, col, case=True):
		# Returns difference between column value and 1990
		accessed = 2019
		ret = "-1"
		if case:
			if col in self.headers["case"].keys():
				idx = self.headers["case"][col]
				try:
					val = int(self.case[k][idx])
					if col == "DATE_OF_DIAGNOSIS_YYYY":
						print(idx, val)
					if col == "AgeAtDiagnosis":
						# Add age to birth year
						val += int(self.case[k][self.headers["case"]["byr"]])
					if val == self.year:
						# Avoid excluding records from 1990
						val = 0.5
					d = val - self.year
					if d > 0:
						ret = str(d)
				except:
					pass
		if ret == "-1":
			ret = str(accessed - self.year)
		return ret

	def __setDuration__(self, k, case):
		# Stores duration from 1990
		ret = "-1"
		for i in ["AgeAtDiagnosis", "Dyr"]:
			d = self.__getDuration__(k, i, case)
			if d != "-1":
				return d
		return ret

	def __setEvent__(self, k):
		# Sets appropriate event value
		ret = "-1"
		val = self.ucr[k][self.headers["ucr"]["ER"]]
		if val == "0":
			ret = "2"
		elif val == "1":
			ret = "1"
		return ret

	def __mergeCaseRecords__(self):
		# Merges ucr and case records
		tag = "1"
		for k in self.case.keys():
			if k in self.ucr.keys():
				row = self.ucr[k]
				event = self.__setEvent__(k)
				duration = self.__setDuration__(k, True)
				diagfom90 = self.__from1990__(k)
				# Delete redundant column
				del row[self.headers["ucr"]["personid"]]
				self.case[k].extend(row)
				self.case[k].append(tag)
				self.case[k].append(event)
				self.case[k].append(duration)
				self.case[k].append(diagfom90)
				self.count["Merged"]["case"] += 1
				if self.__parentBirthYears__(self.case[k]):
					self.subset[k] = self.case[k]
					self.count["Subset"]["case"] += 1
				else:
					self.incomplete.append(["case", k])

	def __addControls__(self):
		# Adds control records to output list and writes to file
		tag = "0"
		er = "-2"
		event = "3"
		from1990 = "-1"
		blank = []
		for i in range(len(self.headers["ucr"])-2):
			blank.append(".")
		blank.append(er)
		blank.append(tag)
		blank.append(event)
		res = list(self.case.values())
		for k in self.control.keys():
			duration = self.__setDuration__(k, False)
			row = self.control[k]
			# Add empty spaces to preserve case column placement
			row.extend(blank)
			row.append(duration)
			row.append(from1990)
			res.append(row)
			self.count["Merged"]["control"] += 1
			if self.__parentBirthYears__(row):
				self.subset[k] = row
				self.count["Subset"]["control"] += 1
			else:
				self.incomplete.append(["control", k])
		self.__writeList__(self.outfile, res, self.header)

	def merge(self):
		# Merges UCR and UPDB data
		self.__setCaseControl__()
		self.ucr = self.__setCases__("ucr")
		self.case = self.__setCases__("case")
		self.control = self.__setCases__("control")
		self.__getHeader__()
		self.__setColumns__()
		self.__checkCaseRecords__()
		self.__mergeCaseRecords__()
		self.__addControls__()
		self.__writeList__(self.subfile, self.subset.values(), self.header)
		self.__writeList__(self.incompletefile, self.incomplete, ["Type", "personid"])
		for i in self.count.keys():
			fileTotals("{} records".format(i), self.count[i]["case"], self.count[i]["control"])

def main():
	start = datetime.now()
	print("\n\tMerging UPDB and UCR records...")
	merger = DatabaseMerger()
	merger.merge()
	print(("\tFinished. Run time: {}\n").format(datetime.now() - start))

if __name__ == "__main__":
	main()

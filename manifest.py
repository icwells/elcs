'''Input file manifests for elcs analyses'''

import os
from glob import glob
from datetime import datetime
from windowspath import checkFile

class Columns():
	def __init__(self):
		self.target = ["personid", "byr", "MaByr", "PaByr", "MaAgeBr", "PaAgeBr", "MaDyr", "PaDyr", "MalastLivingDate", "PalastLivingDate", "NumSibs", "NumSibsDieChildhood"]
		self.income = ["HomeValue_Head1940", "RENT_ToHEAD", "EgoCenIncome", "MaCenIncome_New", "PaCenIncome_New"]
		self.ucr = ["CTC_TUMOR_MARKER1", "CTC_CS_SITE_SPECIFIC_FACTOR1", "DATE_OF_DIAGNOSIS_YYYY"]
		self.newcol = ["byrBin", "AgeAtDiagnosis", "AgeMaD", "MaAgeBr", "AgePaD", "PaAgeBr", "SibsDieKnown", "MergedSEI", "MergedNP"]
		self.adversity = ["Under10", "MAliveDiag", "MAlive18", "MaD<10", "PAliveDiag", "TeenMa", "PaD<10", "PAlive18",  "SibDeath", "LowSES", "LowIncome", "LowHomeVal", ">5Sibs", "AdversityScore","%Score","Complete"]
		self.plot = ["AgeMaD", "MaAgeBr", "AgePaD", "PaAgeBr", "NumSibs", "SibsDieKnown", "MergedSEI", "MergedNP", "HomeValue_Head1940", "RENT_ToHEAD", "byrBin", "Complete", "TeenMa"]

def allColumns():
	# Returns list of all column names
	c = Columns()
	ret = []
	for i in [c.target, c.income, c.ucr, c.newcol]:
		ret.extend(i)
	return ret

def newColumns():
	# Returns new columns
	c = Columns()
	ret = c.newcol
	ret.extend(c.adversity)
	return ret

#-----------------------------------------------------------------------------

def __getTime__(f):
	# Returns timestamp from filename
	stamp = f[f.find(".")+1:f.rfind(".")]
	return datetime.strptime(stamp, "%Y-%m-%d")

def __getNewest__(path):
	# Returns file with newest datestamp
	files = {}
	g = glob(path)
	if len(g) == 1:
		return g[0]
	for f in g:
		if "_summary" not in f:
			files[__getTime__(f)] = f
	# Return newest file
	mx = max(files.keys())
	return files[mx]

def getMergedFile(subset = False):
	# Returns path to most recent merged file
	if subset:
		infile = __getNewest__("Z:/ELCS/subsetUCRrecords.*.csv")
	else :
		infile = __getNewest__("Z:/ELCS/mergedUCRrecords.*.csv")
	checkFile(infile)
	return infile

def getInfiles(orig = True):
	# Returns dict of input files
	infiles = {}
	infiles["casecontrol"] = "Z:/NewDataFromDavid/David_Ken_BreastCancer_CaseControl_New.csv"
	if orig == True:
		# Read in original source data
		infiles["ucr"] = "Z:/u0918416/Amycasedat_051916.csv"
		infiles["case"] = "Z:/NewDataFromDavid/20191121/David_Amy_BreastCancer_Main_20191121.csv"
		infiles["control"] = "Z:/NewDataFromDavid/20191121/David_Amy_BreastCancer_Main_Ctrl_20191121.csv"
		for k in infiles.keys():
			checkFile(infiles[k])
	else:
		# Read updated files
		infiles["ucr"] = __getNewest__("Z:/ELCS/ucr.*.csv")
		infiles["case"] = __getNewest__("Z:/ELCS/updbCases.*.csv")
		infiles["control"] = __getNewest__("Z:/ELCS/updbControl.*.csv")
	return infiles

def setPath():
	# Sets path to outdir
	wd = os.getcwd()
	# Remove possible trailing slash and drop last directory
	wd = wd[:-1]
	return wd[:wd.rfind(os.path.sep)+1]

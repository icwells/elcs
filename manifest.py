'''Input file manifests for elcs analyses'''

import os
from glob import glob
from datetime import datetime
from windowspath import checkFile

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

def getMergedFile():
	# Returns path to most recent merged file
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
		infiles["case"] = "Z:/NewDataFromDavid/David_Ken_BreastCancer_Main_20190924.txt"
		infiles["control"] = "Z:/NewDataFromDavid/David_Ken_BreastCancer_Main_Ctrl_20190924.txt"
	else:
		# Read updated files
		infiles["ucr"] = __getNewest__("Z:/ELCS/ucr.*.csv")
		infiles["case"] = __getNewest__("Z:/ELCS/updbCases.*.csv")
		infiles["control"] = __getNewest__("Z:/ELCS/updbControl.*.csv")
	for k in infiles.keys():
		checkFile(infiles[k])
	return infiles

def setPath():
	# Sets path to outdir
	wd = os.getcwd()
	# Remove possible trailing slash and drop last directory
	wd = wd[:-1]
	return wd[:wd.rfind(os.path.sep)+1]

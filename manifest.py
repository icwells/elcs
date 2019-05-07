'''Input file manifests for elcs analyses'''

from windowspath import checkFile

def getInfiles():
	# Returns dict of input files
	infiles = {}
	infiles["ucr"] = "Z:/u0918416/Amycasedat_051916.csv"
	infiles["casecontrol"] = "Z:/u0918416/David_Ken_BreastCancer_CaseControl_New20171024.csv"
	infiles["case"] = "Z:/u0918416/David_Ken_BreastCancer_Main_20160617.csv"
	infiles["control"] = "Z:/u0918416/David_Ken_BreastCancer_Main_Ctrl_20160617.csv"
	for k in infiles.keys():
		checkFile(infiles[k])
	return infiles

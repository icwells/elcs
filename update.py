'''Updates all relevant files'''

from adversity import Adversity
from argparse import ArgumentParser
from datetime import datetime
from erColumn import ERupdate
from getTotals import Counter
from histograms import Histograms
from impute import Impute
from manifest import *
from mergeRecords import DatabaseMerger
import os
from summary import Summary
from windowspath import *

def summarize(ucr):
	# Wraps calls to Summary
	infiles = []
	newfiles = getInfiles(False)
	infiles.append(getMergedFile())
	infiles.append(getMergedFile(True))
	infiles.append(getMergedFile(imputed = True))
	if ucr:
		infiles.append(newfiles["ucr"])
	infiles.append(newfiles["case"])
	for i in infiles:
		print(("\n\tSummarizing {}...").format(os.path.split(i)[1]))
		Summary(i)

def main():
	start = datetime.now()
	parser = ArgumentParser("Updates all relevant files.")
	parser.add_argument("--ucr", action = "store_true", default = False, help = "Add ER column to updated UCR file.")
	parser.add_argument("--hist", action = "store_true", default = False, help = "Plot new histograms.")
	args = parser.parse_args()
	if args.ucr:
		print("\n\tUpdating ER status in UCR records...")
		er = ERupdate()
		er.getERstatus()
	print("\n\tCalculating adversity scores in UPDB records...")
	a = Adversity()
	a.getAdversityScores()
	print("\n\tMerging UPDB and UCR records...")
	merger = DatabaseMerger()
	merger.merge()
	# Get summaries
	print("\n\tImputing missing data...")
	i = Impute()
	i.imputeRecords()
	summarize(args.ucr)
	print("\n\tCalculating totals from merged records...")
	c = Counter()
	c.writeXLSX()
	c.printComplete()
	if args.hist:
		Histograms(c)
	print(("\tTotal runtime: {}\n").format(datetime.now() - start))

if __name__ == "__main__":
	main()

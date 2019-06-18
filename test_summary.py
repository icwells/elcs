'''Tests summary script'''

import os
import pytest
import unixpath
from summary import Summary

INFILE = "tests/testmergedUCRrecords.csv"
OUTFILE = "tests/testmergedUCRrecords_summary.csv"
EXPECTED = "tests/testOutput.csv"

def readSummary(infile):
	# Reads input file as dict
	ret = {}
	first = True
	with open(infile, "r") as f:
		for line in f:
			if first == False:
				s = line.strip().split(",")
				ret[s[0]] = s[1:]
			else:
				first = False
	return ret

def test_Summary():
	Summary(INFILE)
	assert os.path.isfile(OUTFILE)
	expected = readSummary(EXPECTED)
	actual = readSummary(OUTFILE)
	for k in expected.keys():
		for idx, i in enumerate(expected[k]):
			assert i == actual[k][idx]
	os.remove(OUTFILE)

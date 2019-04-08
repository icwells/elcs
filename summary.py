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
		self.total = 0
		self.complete = OrderedDict()
		self.__setOutfile__()
		self.__setSummary__()
		self.__writeSummary__()

	def __setOutfile__(self):
		# Stores output file name
		ext = getExt(self.infile)
		path = self.infile[:self.infile.rfind(".")]
		self.outfile = ("{}_summary.{}").format(path, ext)

	def __writeSummary__(self):
		# Write complete dict to outfile
		with open(self.outfile, "w") as out:
			out.write("Field,Filled,Empty,%Filled,Total\n")
			for k in self.complete.keys():
				n = self.complete[k]
				e = self.total-n
				p = n/self.total
				out.write(("{},{},{},{:.2%},{}\n").format(k, n, e, p, self.total))

	def __setKeys__(self):
		# Copies keys from header to complete dict
		for k in self.head.keys():
			self.complete[k] = 0

	def __countRow__(self, s):
		# Checks each column for entry
		for k in self.complete.keys():
			if s[self.head[k]].strip():
				self.complete[k] += 1

	def __setSummary__(self):
		# Counts entires per column in input file
		first = True
		with open(self.infile, "r") as f:
			for line in f:
				line = line.strip()
				if first == False:
					self.total += 1
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

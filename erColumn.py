'''Adds column for ER +/- to ucr data'''

from datetime import datetime
from manifest import *
from windowspath import *

def __getMarkers__():
	# Returns dict of diagnosis markers
	marker = {"1": "0", "2": "1"}
	factor = {"10": "0", "20": "1"}
	return {"CTC_TUMOR_MARKER1": marker, "CTC_CS_SITE_SPECIFIC_FACTOR1": factor}

class ERupdate():

	def __init__(self):
		self.infiles = getInfiles()
		self.header = {}
		self.outfile = ("{}ucr.{}.csv").format(setPath(), datetime.now().strftime("%Y-%m-%d"))
		self.markers = __getMarkers__()
		self.ucr = []
		self.__setUCR__()

	def __setUCR__(self):
		# Reads dict of case/control records
		first = True
		k = "ucr"
		print(("\tReading {} file...").format(k))
		with open(self.infiles[k], "r") as f:
			for line in f:
				line = line.strip()
				if first == False:
					s = line.split(d)
					self.ucr.append(s)
				else:
					d = getDelim(line)
					h = setHeader(line.split(d))
					# Store header for later
					self.header = h
					first = False

	def __writeList__(self):
		# Writes list to csv
		print(("\tWriting {} records to {}...").format(len(self.ucr), getFileName(self.outfile)))
		with open(self.outfile, "w") as out:
			out.write(",".join(self.header.keys()) + ",ER\n")
			for i in self.ucr:
				out.write(",".join(i) + "\n")

	def getERstatus(self):
		# Adds column for ER status
		for idx, i in enumerate(self.ucr):
			found = False
			for key in self.markers.keys():
				if key in self.header.keys():
					val = i[self.header[key]].strip()
					if val is not None:
						for k in self.markers[key].keys():
							if k == val:
								# Append +/-
								self.ucr[idx].append(self.markers[key][k])
								found = True
			if found == False:
				# Append NA
				self.ucr[idx].append("-1")
		self.__writeList__()
		

def main():
	start = datetime.now()
	print("\n\tUpdating ER status in UCR records...")
	er = ERupdate()
	er.getERstatus()
	print(("\tFinished. Run time: {}\n").format(datetime.now() - start))

if __name__ == "__main__":
	main()

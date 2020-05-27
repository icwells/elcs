'''Determines intervals for categorizing reproductive measures'''

from manifest import Columns
from statistics import median, stdev

class Reproduction():

	def __init__(self):
		self.columns = []
		self.dist = {}
		self.header = None
		self.intervals = {} 
		self.__setColumns__()

	def __setDicts__(self):
		# Initializes columns and dictionary
		c = Columns()
		self.columns = c.repro
		for i in self.columns:
			#self.intervals[i] = []
			self.dist[i] = []

	def __getColumn__(self, c, line):
		# Returns column value as an integer
		ret = None
		try:
			val = line[self.header[c]].strip()
			if val:
				ret = int(val)
		except:
			pass
		return ret

	def addLine(self, line):
		# Adds values from line to distributions
		for i in self.columns:
			v = self.__getColumn__(i, line)
			if v:
				self.dist[i].append(v)

	def setIntervals(self):
		# Stores median and median +/- sd
		for i in self.columns:
			md = median(self.dist[i])
			sd = stdev(self.dist[i])
			self.intervals[i] = [md-sd, md+sd]
			print(i, self.intervals[i])
			quit()

	def getIntervals(self, line, diag):
		# Returns interval codes for each column
		ret = ["0", "0", "0"]
		for idx, i in enumerate(self.columns):
			v = self.__getColumn__(i, line)
			if v and v >= 0:
				if v <= self.intervals[i][0]:
					ret[idx] = "1"
				elif v >= self.intervals[i][1]:
					ret[idx] = "3"
				else:
					ret[idx] = "2"
		return ret

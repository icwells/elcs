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

	def __setColumns__(self):
		# Initializes columns and dictionary
		c = Columns()
		self.columns = c.repro
		for i in self.columns:
			self.intervals[i] = []
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
		# Stores median +/- sd
		for i in self.columns:
			md = median(self.dist[i])
			sd = stdev(self.dist[i])
			self.intervals[i] = [md-sd, md+sd]

	def getIntervals(self, line, diag):
		# Returns interval codes for each column
		ret = []
		for i in range(len(self.columns)):
			ret.append("0")
		ret.append("-1")
		for idx, i in enumerate(self.columns):
			v = self.__getColumn__(i, line)
			if v and v >= 0:
				if v <= self.intervals[i][0]:
					ret[idx] = "1"
				elif v >= self.intervals[i][1]:
					ret[idx] = "3"
				else:
					ret[idx] = "2"
				if i == "AgeLastBirth" and diag > 0:
					if diag - v > 1:
						ret[-1] = "1"
					else:
						ret[-1] = "0"
		return ret

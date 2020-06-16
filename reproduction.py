'''Determines intervals for categorizing reproductive measures'''

from manifest import reproductionColumns

class Reproduction():

	def __init__(self):
		self.columns = reproductionColumns()
		#self.dist = {}
		self.header = None
		self.intervals = {"AgeFirstBirth": [20, 30], "AgeLastBirth": [25, 35], "MaxParity": [2, 5]} 
		'''self.__setColumns__()

	def __setColumns__(self):
		# Initializes columns and dictionary
		c = Columns()
		for i in self.dist.keys():
			self.intervals[i] = []'''

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

	'''def addLine(self, line):
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
			self.intervals[i] = [md-sd, md+sd]'''

	def __getIndex__(self, c):
		# Returns index for correct output column
		for idx, i in enumerate(self.columns):
			if i == c:
				return idx
		return -1

	def getIntervals(self, line, diag):
		# Returns interval codes for each column
		ret = []
		for i in range(len(self.columns[:-1])):
			ret.append("0")
		ret.append("-1")
		for i in self.intervals.keys():
			v = self.__getColumn__(i, line)
			if v and v >= 0:
				ret[0] = "1"
				if v <= self.intervals[i][0]:
					c = 1
				elif v >= self.intervals[i][1]:
					c = 3
				else:
					c = 2
				idx = self.__getIndex__("{}Bin{}".format(i, c))
				ret[idx] = "1"
				if i == "AgeLastBirth" and diag > 0:
					if diag - v > 1:
						ret[-1] = "1"
					else:
						ret[-1] = "0"
		return ret

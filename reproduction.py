'''Determines intervals for categorizing reproductive measures'''

from manifest import reproductionColumns

class Reproduction():

	def __init__(self):
		self.columns = reproductionColumns()
		self.header = None
		self.intervals = {"AgeFirstBirth": [20, 24, 30], "MaxParity": [2, 5]}

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

	def __getBin__(self, i, v):
		# Adds to bin value for each increasing interval
		c = 1
		for interval in self.intervals[i]:
			if v > interval:
				c += 1
			else:
				break
		return str(c)

	def getIntervals(self, line, diag): 
		# Returns interval codes for each column
		ret = []
		count = 0
		for i in range(len(self.columns)):
			ret.append("0")
		for idx, i in enumerate(self.columns[1:]):
			i = i.replace("Bin", "")
			v = self.__getColumn__(i, line)
			if v and v >= 0:
				go = True
				if i == "AgeFirstBirth" and 50 < v < 11:
					# Exclude afb less than 11 or greater than 50
					go = False
				if go:
					if v >= 1:
						count += 1
					# Account for skipped index
					ret[idx + 1] = self.__getBin__(i, v)
		if count == len(self.columns) - 1:
			ret[0] = "1"
		return ret

'''Determines intervals for categorizing reproductive measures'''

from manifest import reproductionColumns

class Reproduction():

	def __init__(self):
		self.columns = reproductionColumns()
		self.header = None
		self.intervals = {"AgeFirstBirth": [18, 28, 38], "AgeLastBirth": [25, 35], "MaxParity": [2, 5]}

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

	'''def __getIndex__(self, c):
		# Returns index for correct output column
		for idx, i in enumerate(self.columns):
			if i == c:
				return idx
		return -1'''

	def getIntervals(self, line, diag):
		# Returns interval codes for each column
		ret = []
		for i in range(len(self.columns[:-1])):
			ret.append("0")
		ret.append("-1")
		for idx, i in enumerate(self.columns[1:-1]):
			v = self.__getColumn__(i, line)
			if v and v >= 0:
				ret[0] = "1"
				# Add to bin value for each increasing interval
				c = 1
				for interval in self.intervals[i]:
					if v > interval:
						c += 1
					else:
						break
				'''if v <= self.intervals[i][0]:
					c = 1
				elif v <= self.intervals[i][1]:
					c = 2
				elif i != "AgeFirstBirth" or v <= self.intervals[i][2]:
					c = 3
				else:
					c = 4
				idx = self.__getIndex__("{}Bin{}".format(i, c))'''
				ret[idx + 1] = str(c)
				if i == "AgeLastBirth" and diag > 0:
					if diag - v > 1:
						ret[-1] = "1"
					else:
						ret[-1] = "0"
		return ret

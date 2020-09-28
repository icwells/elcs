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
				if v >= 1:
					count += 1
				# Add to bin value for each increasing interval
				c = 1
				for interval in self.intervals[i]:
					if v > interval:
						c += 1
					else:
						break
				# Account for skipped index
				ret[idx + 1] = str(c)
		if count == len(self.columns) - 1:
			ret[0] = "1"
		return ret

'''Deinfes class for storing UPDB records'''

from collections import OrderedDict

def getRent(val):
	# Sorts rent codes from values
	ret = -1
	if val != "0000" and val != "0001" and val != "9998" and val != "9999":
		try:
			ret = float(val)
		except ValueError:
			pass
	return ret

def getMax(x, y, line):
	# Returns higher value of line[x] or line[y]
	ret = -1
	vals = []
	for i in [x, y]:
		if i < len(line):
			try:
				v = int(line[i].strip())
				vals.append(v)
			except ValueError:
				pass
	if len(vals) > 0:
		ret = max(vals)
	return ret

class UPDBRecord():

	def __init__(self, h, columns, income, line):
		self.start = 1904
		self.d = OrderedDict()
		self.__setDict__(columns)
		self.__setAges__(h, line)
		self.__setIncomeMeasures__(h, income, line)

	def __setDict__(self, columns):
		# Initialized dict by column name (skip adversity score columns)
		for k in columns[:-2]:
			self.d[k] = -1

	def __setScore__(self):
		# Returns score as string
		ret = 0
		d := 0
		# Isolate income scores first to evaluate numsibs
		for k in ["LowSES", "LowIncome", "LowHomeVal"]:
			if self.d[k] >= 0:
				d += 1
				if self.d[k] == 1:
					ret += 1
		if self.d[">5Sibs"] >= 0:
			d += 1
			if self.d[">5Sibs"] == 1 and ret > 0:
				ret += 1
		for k in ["MaD<10", "TeenMa", "PaD<10", "SibDeath"]:
			if self.d[k] >= 0:
				d += 1
				if self.d[k] == 1:
					ret += 1
		return [str(ret), "{:.2%}".format(ret/d)]

	def __isSet__(self):
		# Returns false if all values are NA
		for k in self.d.keys():
			if self.d[k] > -1:
				return True
		return False

	def toList(self, limits):
		# Returns stored values as list of strings
		if self.__isSet__():
			ret = []
			for k in self.d.keys():
				if k in limits.keys():
					# Replace illogical values with -1
					if limits[k].xmax is not None and self.d[k] > limits[k].xmax:
						self.d[k] = -1
					elif self.d[k] < limits[k].xmin:
						self.d[k] = -1
				ret.append(str(self.d[k]))
			ret.extend(self.__setScore__())
		else:
			# Return list of NAs
			ret = ["-1", "-1"]
			for k in self.d.keys():
				ret.append("-1")
		return ret

#-----------------------------------------------------------------------------

	def __getComparison__(self, idx, line, less=None, greater=None):
		# Performs given comparison, appends to ext and returns adversity point
		ret = self.__getCol__(idx, line)
		if ret >= 0:
			if less is not None and ret < less:
				ret = 1
			elif greater is not None and ret > greater:
				ret = 1
			else:
				ret = 0
		return ret

	def __lessThanTen__(self, v):
		# Returns 1 if <= 10 when parent died
		if 0 <= v <= 10:
			return 1
		elif v >= 0:
			return 0
		else:
			return -1

	def __setAge__(self, p, e, filt = False):
		# Returns string of p-e
		ret = p-e
		if filt and 13 <= ret <= 55:
			return ret
		elif ret >= 0:
			return ret
		else:
			return -1

	def __getCol__(self, idx, line):
		# Returns column value/-1
		ret = -1
		if idx < len(line):
			val = line[idx].strip()
			if val is not None:
				try:
					ret = int(val)
				except ValueError:
					pass
		return ret

	def __aliveAt18__(self, idx, line, birth):
		# Returns -1/0/1 if parent alive when ego was 18
		ret = -1
		val = line[idx].strip()
		if val is not None:
			# Strip month and day
			if "-" in val:
				val = val.split("-")[0]
			elif "/" in val:
				val = val.split("/")[-1]
			try:
				v = int(val)
				if v >= 0:
					ret = 0
					if v - birth >= 18:
						ret = 1
			except ValueError:
					pass
		return ret

#-----------------------------------------------------------------------------

	def __setIncome__(self, h, income, line):
		# Finds single income value for family
		eci = self.__getComparison__(h["EgoCenIncome"], line, less=income["EgoCenIncome"])
		mci = self.__getComparison__(h["MaCenIncome_New"], line, less=income["MaCenIncome_New"])
		pci = self.__getComparison__(h["PaCenIncome_New"], line, less=income["PaCenIncome_New"])
		if eci == 1 or mci == 1 or pci == 1: 
			self.d["LowIncome"] = 1
		elif eci == 0 or mci == 0 or pci == 0: 
			self.d["LowIncome"] = 0


	def __setHomeVal__(self, h, income, line):
		# Sets vlaues for low rent/home value
		self.d["LowHomeVal"] = -1
		own = self.__getCol__(h["OWNERSHP_ToHEAD"], line)
		if own == 1:
			self.d["LowHomeVal"] = self.__getComparison__(h["HomeValue_Head1940"], line, less=income["HomeValue_Head1940"])
		elif own == 2:
			self.d["LowHomeVal"] = 1

	def __setIncomeMeasures__(self, h, income, line):
		# Sets values for income
		self.d["LowSES"] = -1
		self.d["MergedSEI"] = getMax(h["MaCenSEI"], h["PaCenSEI"], line)
		self.d["MergedNP"] = getMax(h["MaCenNamPow"], h["PaCenNamPow"], line)
		if self.d["MergedSEI"] > 0 or self.d["MergedNP"] > 0:
			self.d["LowSES"] = 0
			if self.d["MergedSEI"] < income["MergedSEI"] or self.d["MergedNP"] < income["MergedNP"]:
				self.d["LowSES"] = 1
		self.__setIncome__(h, income, line)
		self.__setHomeVal__(h, income, line)
		self.d[">5Sibs"] = self.__getComparison__(h["NumSibs"], line, greater=5)

	def __sibsDieKnown__(self, h, line):
		# Zero-fills number of siblings died column and stores sibling death point
		sibs = self.__getCol__(h["NumSibs"], line)
		self.d["SibsDieKnown"] = self.__getCol__(h["NumSibsDieChildhood"], line)
		if sibs > 30 or self.d["SibsDieKnown"] > sibs:
			self.d["SibsDieKnown"] = -1
		elif self.d["SibsDieKnown"] < 1 and sibs >= 0:
	 		self.d["SibsDieKnown"] = 0
		# Record whether or not any siblings died
		if self.d["SibsDieKnown"] > 0:
			self.d["SibDeath"] = 1
		elif self.d["SibsDieKnown"] == 0:
			self.d["SibDeath"] = 0

	def __setMaAges__(self, h, line, birth, mb):
		# Sets values relating to mother's age
		md = self.__getCol__(h["MaDyr"], line)
		if md > 0:
			self.d["AgeMaD"] = self.__setAge__(md, birth)
		self.d["MaAgeBr"] = self.__setAge__(birth, mb, True)
		self.d["MaD<10"] = self.__lessThanTen__(self.d["AgeMaD"])
		if self.d["MaD<10"] == 1:
			self.d["MAlive18"] = 0
		elif self.d["AgeMaD"] >= 18:
			self.d["MAlive18"] = 1
		else:
			self.d["MAlive18"] = self.__aliveAt18__(h["MalastLivingDate"], line, birth)
		if 0 <= self.d["MaAgeBr"] <= 18:
			# Set 1 for teenage mother
			self.d["TeenMa"] = 1

	def __setPaAges__(self, h, line, birth, pb):
		# Sets values relating to father's age
		pd = self.__getCol__(h["PaDyr"], line)
		if pd > 0:
			self.d["AgePaD"] = self.__setAge__(pd, birth)
		self.d["PaAgeBr"] = self.__setAge__(birth, pb, True)	
		self.d["PaD<10"] = self.__lessThanTen__(self.d["AgeMaD"])
		if self.d["PaD<10"] == 1:
			self.d["PAlive18"] = 0
		elif self.d["AgePaD"] >= 18:
			self.d["PAlive18"] = 1
		else:
			self.d["PAlive18"] = self.__aliveAt18__(h["PalastLivingDate"], line, birth)

	def __setAges__(self, h, line):
		# Stores age-based calculations
		# Get self, mother's, and father's birth year
		birth = self.__getCol__(h["byr"], line)
		if birth > self.start:
			# Ignore records from before 1904
			mb = self.__getCol__(h["MaByr"], line)
			pb = self.__getCol__(h["PaByr"], line)
			if birth > 0:
				if mb > 0:
					self.__setMaAges__(h, line, birth, mb)
				if pb > 0:
					self.__setPaAges__(h, line, birth, pb)
			self.__sibsDieKnown__(h, line)

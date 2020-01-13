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

	def __init__(self, h, columns, income, line, diagdate):
		self.start = 1904
		self.diagdate = diagdate
		self.birth = -1
		self.d = OrderedDict()
		self.__setDict__(columns)
		self.__setAges__(h, line)
		self.__setIncomeMeasures__(h, income, line)

	def __setDict__(self, columns):
		# Initialized dict by column name (skip adversity score and byrBin columns)
		for k in columns[1:-2]:
			self.d[k] = -1

	def __setPercent__(self, score):
		# Returns formatted percent score
		ret = 0
		if score > 0:
			d = 0 
			for k in self.d.keys():
				if self.d[k] >= 0:
					d += 1
			if d > 0:
				ret = score/d
		return "{:.2%}".format(ret)
		

	def __setScore__(self):
		# Returns score as string
		ret = 0
		d = 0
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
		return [str(ret), self.__setPercent__(ret)]

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
		# Returns 1 if <= 10
		if 0 <= v <= 10:
			return 1
		elif v >= 0:
			return 0
		else:
			return -1

	def __setAge__(self, p, e, filt = False):
		# Returns p-e
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

	def __aliveAt__(self, val, year, target):
		# Returns -1/0/1 if parent alive when val - year >= target
		ret = -1
		if val > year:
			ret = 0
			if val - year >= target:
				ret = 1
		return ret

	def __lastLiving__(self, idx, line):
		# Returns formatted last living date
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
					ret = v
			except ValueError:
					pass
		return ret

#-----------------------------------------------------------------------------

	def __setIncome__(self, h, income, line):
		# Finds single income value for family
		eci = self.__getComparison__(h["EgoCenIncome"], line, less=income["EgoCenIncome"])
		mci = self.__getComparison__(h["MaCenIncome_New"], line, less=income["MaCenIncome_New"])
		pci = self.__getComparison__(h["PaCenIncome_New"], line, less=income["PaCenIncome_New"])
		l = [eci, mci, pci]
		for i in l:
			if i == 1:
				self.d["LowIncome"] = 1
				break
			elif i == 0: 
				self.d["LowIncome"] = 0

	def __setHomeVal__(self, h, income, line):
		# Sets vlaues for low rent/home value
		self.d["LowHomeVal"] = -1
		own = self.__getCol__(h["OWNERSHP_ToHEAD"], line)
		if own == 10 or own == 1:
			self.d["LowHomeVal"] = self.__getComparison__(h["HomeValue_Head1940"], line, less=income["HomeValue_Head1940"])
		elif own == 20 or own == 2:
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

	def __setParentalAges__(self, h, k, line, pb):
		# Sets values relating to parent's age
		pd = self.__getCol__(h["{}aDyr".format(k)], line)
		lld = self.__lastLiving__(h["{}alastLivingDate".format(k)], line)
		if pd > 0:
			self.d["Age{}aD".format(k)] = self.__setAge__(pd, self.birth)
		self.d["{}AliveDiag".format(k)] = self.__aliveAt__(lld, self.diagdate, 0) 
		self.d["{}aAgeBr".format(k)] = self.__setAge__(self.birth, pb, True)	
		self.d["{}aD<10".format(k)] = self.__lessThanTen__(self.d["AgeMaD"])
		if self.d["{}aD<10".format(k)] == 1:
			self.d["{}Alive18".format(k)] = 0
		elif self.d["Age{}aD".format(k)] >= 18:
			self.d["{}Alive18".format(k)] = 1
		else:
			self.d["{}Alive18".format(k)] = self.__aliveAt__(pd, self.birth, 18)

	def __setAges__(self, h, line):
		# Stores age-based calculations
		# Get self, mother's, and father's birth year
		self.birth = self.__getCol__(h["byr"], line)
		if self.birth > self.start:
			# Ignore records from before 1904
			if self.diagdate > self.start:
				self.d["AgeAtDiagnosis"] = self.__setAge__(self.diagdate, self.birth)
				self.d["Under10"] = self.__lessThanTen__(self.d["AgeAtDiagnosis"])
			mb = self.__getCol__(h["MaByr"], line)
			pb = self.__getCol__(h["PaByr"], line)
			if mb > 0:
				self.__setParentalAges__(h, "M", line, mb)
				if self.d["MaAgeBr"] > 0: 
					self.d["TeenMa"] = 0
					if self.d["MaAgeBr"] <= 18:
						# Set 1 for teenage mother
						self.d["TeenMa"] = 1
			if pb > 0:
				self.__setParentalAges__(h, "P", line, pb)
			self.__sibsDieKnown__(h, line)

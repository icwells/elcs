'''Deinfes class for storing UPDB records'''

from collections import OrderedDict
from manifest import measureColumns

MEASURES = measureColumns()

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
		self.h = h
		self.line = line
		self.diagdate = diagdate
		self.birth = -1
		self.complete = 0
		self.all = 0
		self.score = 0
		self.d = OrderedDict()
		self.__setDict__(columns)
		self.__setAges__()
		self.__setIncomeMeasures__(income)

	def __setDict__(self, columns):
		# Initialized dict by column name
		for k in columns:
			if k != "byrBin":
				self.d[k] = 0

	def __setPercent__(self):
		# Returns formatted percent score
		ret = 0
		if self.score > 0:
			d = 0 
			for k in self.d.keys():
				if self.d[k] >= 0:
					d += 1
			if d > 0:
				ret = self.score/d
		return "{:.2%}".format(ret)

	def __setScore__(self):
		# Returns score as string
		# Isolate income scores first to evaluate numsibs
		for k in ["LowSES", "LowHomeVal"]:
			if self.d[k] >= 0:
				self.score += self.d[k]
		if self.d[">5Sibs"] >= 0:
			if self.d[">5Sibs"] == 1 and self.score > 0:
				self.score += 1
		for k in ["MaD<10", "TeenMa", "PaD<10", "SibDeath"]:
			if self.d[k] >= 0:
				self.score += self.d[k]
		return [str(self.score), self.__setPercent__()]

	def __setComplete__(self):
		# Stores 1 for complete if all family fields are set
		go = True
		for i in ["MaAgeBr", "PaAgeBr", "SibsDieKnown", "LowSES"]:
			if self.d[i] == -1:
				if "Ma" in i:
					if self.d["MaD<10"] != 0:
						go = False
				elif "Pa" in i:
					if self.d["PaD<10"] != 0:
						go = False
				else:
					go = False
				if not go:
					break
		if go:
			self.complete = 1
		for k in MEASURES:
			# Determine if all fields are complete
			if k in self.d.keys():
				if self.d[k] < 0:
					go = False
					break
			else:
				v = self.line[self.h[k]]
				if v and int(v) < 0:
					go = False
					break
		if go:
			self.all = 1

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
			self.__setComplete__()
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
				ret.append("0")
		ret.append(str(self.complete))
		ret.append(str(self.all))
		return ret

#-----------------------------------------------------------------------------

	def __getComparison__(self, idx, less=None, greater=None):
		# Performs given comparison, appends to ext and returns adversity point
		ret = self.__getCol__(idx)
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
		else:
			return 0

	def __setAge__(self, p, e, filt = False):
		# Returns p-e
		ret = p-e
		if filt and 13 <= ret <= 55:
			return ret
		elif ret >= 0:
			return ret
		else:
			return 0

	def __getCol__(self, idx):
		# Returns column value
		ret = 0
		if idx < len(self.line):
			val = self.line[idx].strip()
			if val is not None:
				try:
					ret = int(val)
				except ValueError:
					pass
		return ret

	def __aliveAt__(self, val, year, target):
		# Returns 0/1 if parent alive when val - year >= target
		ret = 0
		if val > year:
			if val - year >= target:
				ret = 1
		return ret

	def __lastLiving__(self, idx):
		# Returns formatted last living date
		ret = 0
		val = self.line[idx].strip()
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

	def __setIncome__(self, income):
		# Finds single income value for family
		eci = self.__getComparison__(self.h["EgoCenIncome"], less=income["EgoCenIncome"])
		mci = self.__getComparison__(self.h["MaCenIncome_New"], less=income["MaCenIncome_New"])
		pci = self.__getComparison__(self.h["PaCenIncome_New"], less=income["PaCenIncome_New"])
		l = [eci, mci, pci]
		for i in l:
			if i == 1:
				self.d["LowIncome"] = 1
				break
			elif i == 0: 
				self.d["LowIncome"] = 0

	def __setHomeVal__(self, income):
		# Sets vlaues for low rent/home value
		own = self.__getCol__(self.h["OWNERSHP_ToHEAD"])
		if own == 10 or own == 1:
			self.d["LowHomeVal"] = self.__getComparison__(self.h["HomeValue_Head1940"], less=income["HomeValue_Head1940"])
		elif own == 20 or own == 2:
			self.d["LowHomeVal"] = 1

	def __setIncomeMeasures__(self, income):
		# Sets values for income
		self.d["MergedSEI"] = getMax(self.h["MaCenSEI"], self.h["PaCenSEI"], self.line)
		self.d["MergedNP"] = getMax(self.h["MaCenNamPow"], self.h["PaCenNamPow"], self.line)
		if self.d["MergedSEI"] > 0 or self.d["MergedNP"] > 0:
			self.d["LowSES"] = 0
			if self.d["MergedSEI"] < income["MergedSEI"] or self.d["MergedNP"] < income["MergedNP"]:
				self.d["LowSES"] = 1
		self.__setIncome__(income)
		self.__setHomeVal__(income)
		self.d[">5Sibs"] = self.__getComparison__(self.h["NumSibs"], greater=5)

	def __sibsDieKnown__(self):
		# Zero-fills number of siblings died column and stores sibling death point
		sibs = self.__getCol__(self.h["NumSibs"])
		self.d["SibsDieKnown"] = self.__getCol__(self.h["NumSibsDieChildhood"])
		if sibs > 30 or self.d["SibsDieKnown"] > sibs:
			self.d["SibsDieKnown"] = 0
		elif self.d["SibsDieKnown"] < 0 and sibs >= 0:
	 		self.d["SibsDieKnown"] = 0
		# Record whether or not any siblings died
		if self.d["SibsDieKnown"] > 0:
			self.d["SibDeath"] = 1
		elif self.d["SibsDieKnown"] == 0:
			self.d["SibDeath"] = 0

	def __setParentalAges__(self, k, pb):
		# Sets values relating to parent's age
		pd = self.__getCol__(self.h["{}aDyr".format(k)])
		lld = self.__lastLiving__(self.h["{}alastLivingDate".format(k)])
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

	def __setAges__(self):
		# Stores age-based calculations
		# Get self, mother's, and father's birth year
		self.birth = self.__getCol__(self.h["byr"])
		if self.birth > self.start:
			# Ignore records from before 1904
			if self.diagdate > self.start:
				self.d["AgeAtDiagnosis"] = self.__setAge__(self.diagdate, self.birth)
				self.d["Under10"] = self.__lessThanTen__(self.d["AgeAtDiagnosis"])
			mb = self.__getCol__(self.h["MaByr"])
			pb = self.__getCol__(self.h["PaByr"])
			if mb > 0:
				self.__setParentalAges__("M", mb)
				if self.d["MaAgeBr"] > 0: 
					self.d["TeenMa"] = 0
					if self.d["MaAgeBr"] <= 18:
						# Set 1 for teenage mother
						self.d["TeenMa"] = 1
			if pb > 0:
				self.__setParentalAges__("P", pb)
			self.__sibsDieKnown__()

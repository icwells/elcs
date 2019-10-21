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

class UPDBRecord():

	def __init__(self, h, columns, income, line):
		self.score = 0
		self.d = OrderedDict()
		self.__setDict__(columns)
		self.__setAges__(h, line)
		self.__setIncomeMeasures__(h, income, line)

	def __setDict__(self, columns):
		# Initialized dict by column name (skip adversity score column)
		for k in columns[:-1]:
			self.d[k] = -1
	
	def toList(self):
		# Returns stored values as list of strings
		ret = []
		for k in self.d.keys():
			ret.append(str(self.d[k]))
		ret.append(str(self.score))
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
		# Returns Y if <= 10 when parent died
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
		own = self.__getCol__(h["OWNERSHP_ToHEAD"], line)
		if own == 1:
			self.d["LowHomeVal"] = self.__getComparison__(h["HomeValue_Head1940"], line, less=income["HomeValue_Head1940"])
		elif own == 2:
			rent = getRent(line[h["RENT_ToHEAD"]])
			if rent >= 0:
				if rent <= income["RENT_ToHEAD"]:
					self.d["LowHomeVal"] = 1
				else:
					self.d["LowHomeVal"] = 0

	def __setIncomeMeasures__(self, h, income, line):
		# Sets values for income
		low = False
		self.d["LowMaNP"] = self.__getComparison__(h["MaCenNamPow"], line, less=income["MaCenNamPow"])
		self.d["LowMaSEI"] = self.__getComparison__(h["MaSEI1940"], line, less=income["MaSEI1940"])
		self.d["LowPaNP"] = self.__getComparison__(h["PaCenNamPow"], line, less=income["PaCenNamPow"])
		self.d["LowPaSEI"] = self.__getComparison__(h["PaSEI1940"], line, less=income["PaSEI1940"])
		self.__setIncome__(h, income, line)
		self.__setHomeVal__(h, income, line)
		# Give max of one point for low income status per self/parent
		if self.d["LowMaSEI"] == 1 or self.d["LowMaNP"] == 1:
			self.score += 1
			low = True
		if self.d["LowPaSEI"] == 1 or self.d["LowPaNP"] == 1:
			self.score += 1
			low = True
		self.d[">5Sibs"] = self.__getComparison__(h["NumSibs"], line, greater=5)
		if self.d[">5Sibs"]:
			if low or self.d["LowIncome"] == 1 or self.d["LowHomeVal"] == 1:
				# Only consider large number of siblings adversity if low income
				self.score += 1

	def __setMaAges__(self, h, line, birth, mb):
		# Sets values relating to mother's age
		md = self.__getCol__(h["MaDyr"], line)
		if md > 0:
			self.d["AgeMaD"] = self.__setAge__(md, birth)
		self.d["MaAgeBr"] = self.__setAge__(birth, mb, True)
		self.d["MaD<10"] = self.__lessThanTen__(self.d["AgeMaD"])
		if self.d["MaD<10"] == 0:
			self.d["MAlive18"] = 0
			self.score += 1
		else:
			self.d["MAlive18"] = self.__aliveAt18__(h["MaLastResUtahDate"], line, birth)
		if 0 <= self.d["MaAgeBr"] <= 18:
			# Set 1 for teenage mother
			self.d["TeenMa"] = 1
			self.score += 1

	def __setPaAges__(self, h, line, birth, pb):
		# Sets values relating to father's age
		pd = self.__getCol__(h["PaDyr"], line)
		if pd > 0:
			self.d["AgePaD"] = self.__setAge__(pd, birth)
		self.d["PaAgeBr"] = self.__setAge__(birth, pb, True)	
		self.d["PaD<10"] = self.__lessThanTen__(self.d["AgeMaD"])
		if self.d["PaD<10"] == 0:
			self.score += 1
			self.d["PAlive18"] = 0
		else:
			self.d["PAlive18"] = self.__aliveAt18__(h["PaLastResUtahDate"], line, birth)

	def __setAges__(self, h, line):
		# Stores age-based calculations
		# Get self, mother's, and father's birth year
		birth = self.__getCol__(h["byr"], line)
		mb = self.__getCol__(h["MaByr"], line)
		pb = self.__getCol__(h["PaByr"], line)
		if birth > 0:
			if mb > 0:
				self.__setMaAges__(h, line, birth, mb)
			if pb > 0:
				self.__setPaAges__(h, line, birth, pb)
		self.d["SibDeath"] = self.__getComparison__(h["NumSibsDieChildhood"], line, greater=1)
		if self.d["SibDeath"] == 1:
			self.score += 1

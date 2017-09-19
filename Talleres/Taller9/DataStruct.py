class HashTable:
	def __init__(self, size = 100):
		self.size = size
		self.table = [None for e in range(size)]

	def _hash_function(self, key):
		if type(key) == str:
			acum = 0
			i = 1
			n = len(key)
			for let in key:
				acum += ord(let)*(31**(n - i))
				i += 1
			return (acum)%(self.size)
		else:
			print("The key passed is not a string")

	def add(self, keys):
		for key in keys:
			hash_value = self._hash_function(key["key"])
			if self.table[hash_value] == None:
				self.table[hash_value] = []
			self.table[hash_value].append(key["value"])

	def get(self, key):
		hash_value = self._hash_function(key)
		if self.table[hash_value] == None:
			print("There's no value assinged to that key")
			return None
		else:
			if len(self.table[hash_value]) == 1:
				return self.table[hash_value][0]
			else:
				return self.table[hash_value]

	def arcget(self, value):
		self.table.index(value)


# 4...
def iscompany(hash, key):
	if hash.get(key) != None:
		return True
	else:
		return False

myhash = HashTable(25)
myhash.add([{"key": "Google", "value": "USA"},
			{"key": "La locura", "value": "COL"},
			{"key": "Nokia", "value": "FIN"},
			{"key": "Sony", "value": "JAP"}])

print(str(iscompany(myhash, "Google")))


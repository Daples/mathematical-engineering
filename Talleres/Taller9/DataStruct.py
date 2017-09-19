class HashTable:
    def __init__(self, size=100):
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
            return acum % self.size
        else:
            print("The key passed is not a string")

    def add(self, keys):
        for key in keys:
            hash_value = self._hash_function(key["key"])
            if self.table[hash_value] is None:
                self.table[hash_value] = []
            self.table[hash_value].append(key["value"])

    def get(self, key):
        hash_value = self._hash_function(key)
        if self.table[hash_value] is None:
            print("There's no value assinged to that key")
            return None
        else:
            if len(self.table[hash_value]) == 1:
                return self.table[hash_value][0]
            else:
                return self.table[hash_value]

    # 4
    def is_key(self, key):
        if self.get(key) is None:
            return False
        else:
            return True

    # 5
    def is_value(self, value):
        for i in range(self.size):
            if self.table[i] is not None:
                for j in range(len(self.table[i])):
                    if self.table[i][j] == value:
                        return True

        return False

my_hash = HashTable(25)
my_hash.add([{"key": "Google", "value": "USA"},
            {"key": "La locura", "value": "COL"},
            {"key": "Nokia", "value": "FIN"},
            {"key": "Sony", "value": "JAP"}])
"""
For the exercise 4 and 5 use the is_key and is_value function respectively to answer both of the questions.
This workshop is made by:
    - David Plazas
    - Juan Sebastián Cárdenas
"""

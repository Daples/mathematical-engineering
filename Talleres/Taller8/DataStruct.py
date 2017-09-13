class Stack:
	def __init__(self, size):
		self.size = size
		self.index = 0
		self.data = []

	def push(self, data):
		if len(self.data) <= self.size:
			self.data.append(data)
			self.index += 1
		else:
			print("The stack is full")

	def peek(self):
		return self[self.index]

	def pop(self):
		self.index -= 1
		aux = self.data[self.index]
		self.data.remove(aux)
		return aux

	def isEmpty(self):
		return len(self.data) == 0

	def isFull(self):
		return len(self.data) == self.size

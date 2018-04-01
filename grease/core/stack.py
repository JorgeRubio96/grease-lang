class Stack(object):
	def __init__(self):
		self.values = []
	def isEmpty(self):
		return self.values == []
	def push(self,  value):
		self.values.append(value)
	def pop(self):
		if(len(self.values) > 0):
			return self.values.pop()
		else:
			return None
	def peek(self):
		if(len(self.values) == 0):
			return None
		else:
			return self.values[-1]
	def size(self):
		return len(self.values)
	def pprint(self):
		print(self.values)
	def inStack(self, var_name):
		return var_name in self.values
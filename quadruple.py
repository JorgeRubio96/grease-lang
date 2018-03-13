from enum import Enum
import sys

class Quadruple(object):
	def __init__(self):
		self.id = -1 # auto_incremented
		self.operator = None
		self.left_operand = None
		self.right_operand = None
		self.result = None

	def build(self, operator, left_operand, right_operand, result):
		self.operator = operator
		self.left_operand = left_operand
		self.right_operand = right_operand
		self.result = result

	def get_list(self):
		op = inv_op_dict[self.operator]
		return [op, self.left_operand, self.right_operand, self.result]

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
		else :
			print("Empty Stack")
	def peek(self):
		if(len(self.values) == 0):
			return None
		else:
			return self.values[len(self.values)-1]
	def size(self):
		return len(self.values)
	def pprint(self):
		print(self.values)
	def inStack(self, var_name):
		return var_name in self.values

class Quadruples(object):
	# Class variables
	quad_list = []
	op_list = []
	op_jump_stack = Stack()
	jump_stack = Stack()
	next_free_quad = 0
	op_next_free_quad = 0
	__shared_state_op = {}
	__shared_state = {}
	def __init__(self):
		self.__dict__ = self.__shared_state

	# Quad Methods
	@classmethod
	def push_quad(cls, quad):
		quad.id = cls.next_free_quad
		cls.quad_list.append(quad)
		cls.next_free_quad = len(cls.quad_list)

	@classmethod
	def pop_quad(cls):
		cls.next_free_quad = len(cls.quad_list) - 1
		return cls.quad_list.pop()

	@classmethod
	def fill_missing_quad(cls, quad_id, value):
		cls.quad_list[quad_id].result = value

	# Jump Stack Methods
	@classmethod
	def push_jump(cls, offset):
		cls.jump_stack.push(cls.next_free_quad + offset)

	@classmethod
	def pop_jump(cls):
		return cls.jump_stack.pop()
		
	@classmethod
	def peek_jump(cls):
		return cls.jump_stack.peek()

	@classmethod
	def print_jump_stack(cls):
		cls.jump_stack.pprint()

	@classmethod
	def print_all(cls):
		"""prints all quadruples from list """
		count = 0
		print("Quads ===============================")
		l = [x.get_list() for x in cls.quad_list]
		for e in l:
			sys.stdout.write(str(count) + ":\t")
			for se in e:
				if not se == None:
					sys.stdout.write(str(se))
				sys.stdout.write("\t")
			count += 1
			print("")
		pass




class Operation(Enum):
	TIMES = 1
	DIVIDE = 2
	PLUS = 3 
	MINUS = 4
	EQ = 5
	GT = 6
	LT = 7 
	GE = 8
	LE = 9 
	NOT = 10
	ASSIGN = 11
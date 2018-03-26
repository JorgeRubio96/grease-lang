from enum import Enum
from stack import Stack
import sys
from type import GreaseTypeClass

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
	U_MINUS = 12
	JMP_F = 13
	JMP = 14
	AND = 15
	OR = 16
	CONST = 17
	WHILE = 18
	PRINT = 19
	SCAN = 20
	EQUALS = 21
	IF = 22
	ELSE = 23


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

	def get_op_Stack():
		return op_Stack

	def get_list(self):
		op = Operation(self.operator).value
		return [op, self.left_operand, self.right_operand, self.result]

class Quadruples(object):
	# Class variables
	quad_list = []
	jump_stack = Stack()
	op_Stack = Stack()
	next_free_quad = 0
	op_next_free_quad = 0
	__shared_state_op = {}
	__shared_state = {}
	def __init__(self):
		self.__dict__ = self.__shared_state

	#Op Methods
	@classmethod
	def push_op(self, op):
		op.id = self.next_free_quad
		self.op_Stack.push(op)
		self.next_free_quad = self.op_Stack.size

	@classmethod
	def pop_op(self):
		self.next_free_quad = self.op_Stack.size - 1
		return self.op_Stack.pop()

	# Quad Methods
	@classmethod
	def push_quad(cls, quad):
		quad.id = cls.next_free_quad
		cls.quad_list.append(quad)
		cls.next_free_quad = len(cls.quad_list)
		#For test only
		x = 0
		while x < len(cls.quad_list):
			var = cls.quad_list[x]
			print(var)
			x+=1

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
		#Traer lista de cuadruplos
		l = [x.get_list() for x in cls.quad_list]
		#mientras el elemento(cuadruplo) este en la lista
		for e in l:
			sys.stdout.write(str(count) + ":\t")
			#por cada single element en el elemento (cuadruplo)
			for se in e:
				if not se == None:
					sys.stdout.write(str(se))
				sys.stdout.write("\t")
			count += 1
			print("")
		pass
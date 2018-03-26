import pprint
from type import GreaseTypeClass
from quadruple import Operation

class SemanticCube(object):
	"""docstring for SemanticCube"""
	n = len(GreaseTypeClass)
	ops = len(Operation)
	cube = {}

	def set_return_value_for(cls, left, op, right, res):
		if not isinstance(left, GreaseTypeClass) or not isinstance(right, GreaseTypeClass) \
			or not isinstance(op, Operation) or not isinstance(res, GreaseTypeClass):
				return False
		
		if op not in cls.cube:
			cls.cube[op] = {}

		if left not in cls.cube[op]:
			cls.cube[op][left] = {}

		cls.cube[op][left][right] = res

		return True



	def print_cube(cls):
		pp.print(cls)

obj = SemanticCube()
obj.set_return_value_for(GreaseTypeClass.Int, Operation.PLUS, GreaseTypeClass.Int, GreaseTypeClass.Int)
obj.set_return_value_for(GreaseTypeClass.Int, Operation.PLUS, GreaseTypeClass.Float, GreaseTypeClass.Float)
obj.set_return_value_for(GreaseTypeClass.Float, Operation.PLUS, GreaseTypeClass.Float, GreaseTypeClass.Float)
obj.set_return_value_for(GreaseTypeClass.Float, Operation.PLUS, GreaseTypeClass.Int, GreaseTypeClass.Float)
obj.set_return_value_for(GreaseTypeClass.Int, Operation.MINUS, GreaseTypeClass.Int, GreaseTypeClass.Int)
obj.set_return_value_for(GreaseTypeClass.Int, Operation.MINUS, GreaseTypeClass.Float, GreaseTypeClass.Float)
obj.set_return_value_for(GreaseTypeClass.Float, Operation.MINUS, GreaseTypeClass.Int, GreaseTypeClass.Float)
obj.set_return_value_for(GreaseTypeClass.Float, Operation.MINUS, GreaseTypeClass.Float, GreaseTypeClass.Float)
obj.set_return_value_for(GreaseTypeClass.Int, Operation.U_MINUS, None, GreaseTypeClass.Int)
obj.set_return_value_for(GreaseTypeClass.Float, Operation.U_MINUS, None, GreaseTypeClass.Float)
obj.set_return_value_for(GreaseTypeClass.Int, Operation.TIMES, GreaseTypeClass.Int, GreaseTypeClass.Int)
obj.set_return_value_for(GreaseTypeClass.Int, Operation.TIMES, GreaseTypeClass.Float, GreaseTypeClass.Float)
obj.set_return_value_for(GreaseTypeClass.Float, Operation.TIMES, GreaseTypeClass.Int, GreaseTypeClass.Float)
obj.set_return_value_for(GreaseTypeClass.Float, Operation.TIMES, GreaseTypeClass.Float, GreaseTypeClass.Float)
obj.set_return_value_for(GreaseTypeClass.Int, Operation.DIVIDE, GreaseTypeClass.Int, GreaseTypeClass.Int)
obj.set_return_value_for(GreaseTypeClass.Int, Operation.DIVIDE, GreaseTypeClass.Float, GreaseTypeClass.Float)
obj.set_return_value_for(GreaseTypeClass.Float, Operation.DIVIDE, GreaseTypeClass.Int, GreaseTypeClass.Float)
obj.set_return_value_for(GreaseTypeClass.Float, Operation.DIVIDE, GreaseTypeClass.Float, GreaseTypeClass.Float)
obj.set_return_value_for(GreaseTypeClass.Int, Operation.EQ, GreaseTypeClass.Int, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Int, Operation.EQ, GreaseTypeClass.Float, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Float, Operation.EQ, GreaseTypeClass.Int, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Float, Operation.EQ, GreaseTypeClass.Float, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Int, Operation.LT, GreaseTypeClass.Int, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Int, Operation.LT, GreaseTypeClass.Float, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Float, Operation.LT, GreaseTypeClass.Int, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Float, Operation.LT, GreaseTypeClass.Float, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Int, Operation.GE, GreaseTypeClass.Int, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Int, Operation.GE, GreaseTypeClass.Float, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Float, Operation.GE, GreaseTypeClass.Int, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Float, Operation.GE, GreaseTypeClass.Float, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Int, Operation.GT, GreaseTypeClass.Int, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Int, Operation.GT, GreaseTypeClass.Float, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Float, Operation.GT, GreaseTypeClass.Int, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Float, Operation.GT, GreaseTypeClass.Float, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Int, Operation.LE, GreaseTypeClass.Int, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Int, Operation.LE, GreaseTypeClass.Float, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Float, Operation.LE, GreaseTypeClass.Int, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Float, Operation.LE, GreaseTypeClass.Float, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Int, Operation.NOT, GreaseTypeClass.Int, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Int, Operation.NOT, GreaseTypeClass.Float, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Float, Operation.NOT, GreaseTypeClass.Int, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Float, Operation.NOT, GreaseTypeClass.Float, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Int, Operation.ASSIGN, GreaseTypeClass.Int, GreaseTypeClass.Bool)
obj.set_return_value_for(GreaseTypeClass.Float, Operation.ASSIGN, GreaseTypeClass.Float, GreaseTypeClass.Bool)
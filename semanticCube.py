import pprint 
from variable import GreaseType
from quadruple import Operation
class SemanticCube(object):
	"""docstring for SemanticCube"""
	n = len(type_dict)
	ops = len(operator_dict)
	cube = [[[-1 for j in xrange(n)] for i in xrange(n)] for k in xrange(ops)]

	def set_return_value_for(cls, type1, op_or_list, type2, value):
		i = type_dict[type1]
		j = type_dict[type2]
		value = type_dict[value]
		if isinstance(op_or_list, list):
			indeces = [operator_dict[x] for x in op_or_list]
			for k in indeces:
				cls.set_cube_value(k, i, j, value)
		else:
			k = operator_dict[op_or_list]
			cls.set_cube_value(k, i, j, value)

	def set_cube_value(cls, op, t1, t2, v):
			cls.cube[op][t1][t2] = v
			cls.cube[op][t2][t1] = v

	def print_cube(cls):
		pp.print(cls);

obj = SemanticCube()
obj.set_return_value_for(GreaseType.Int, Operation.Plus, GreaseType.Int, GreaseType.Int)
obj.set_return_value_for(GreaseType.Int, Operation.Plus, GreaseType.Float, GreaseType.Float)
obj.set_return_value_for(GreaseType.Float, Operation.Plus, GreaseType.Float, GreaseType.Float)
obj.set_return_value_for(GreaseType.Float, Operation.Plus, GreaseType.Int, GreaseType.Float)
obj.set_return_value_for(GreaseType.Int,Operation.Minus,GreaseType.Int,GreaseType.Int)
obj.set_return_value_for(GreaseType.Int,Operation.Minus,GreaseType.Float,GreaseType.Float)
obj.set_return_value_for(GreaseType.Float,Operation.Minus,GreaseType.Int,GreaseType.Float)
obj.set_return_value_for(GreaseType.Float,Operation.Minus,GreaseType.Float,GreaseType.Float)
obj.set_return_value_for(GreaseType.Int, Operation.U_Minus, None, GreaseType.Int)
obj.set_return_value_for(GreaseType.Float, Operation.U_Minus, None, GreaseType.Float)
obj.set_return_value_for(GreaseType.Int,Operation.Times,GreaseType.Int,GreaseType.Int)
obj.set_return_value_for(GreaseType.Int,Operation.Times,GreaseType.Float,GreaseType.Float)
obj.set_return_value_for(GreaseType.Float,Operation.Times,GreaseType.Int,GreaseType.Float)
obj.set_return_value_for(GreaseType.Float,Operation.Times,GreaseType.Float,GreaseType.Float)
obj.set_return_value_for(GreaseType.Int,Operation.Divide,GreaseType.Int,GreaseType.Int)
obj.set_return_value_for(GreaseType.Int,Operation.Divide,GreaseType.Float,GreaseType.Float)
obj.set_return_value_for(GreaseType.Float,Operation.Divide,GreaseType.Int,GreaseType.Float)
obj.set_return_value_for(GreaseType.Float,Operation.Divide,GreaseType.Float,GreaseType.Float)
obj.set_return_value_for(GreaseType.Int,Operation.EQ,GreaseType.Int,GreaseType.Bool)
obj.set_return_value_for(GreaseType.Int,Operation.EQ,GreaseType.Float, GreaseType.Bool)
obj.set_return_value_for(GreaseType.Float,Operation.EQ,GreaseType.Int,GreaseType.Bool)
obj.set_return_value_for(GreaseType.Float,Operation.EQ,GreaseType.Float,GreaseType.Bool)
obj.set_return_value_for(GreaseType.Int,Operation.LT,GreaseType.Int,GreaseType.Bool)
obj.set_return_value_for(GreaseType.Int,Operation.LT,GreaseType.Float, GreaseType.Bool)
obj.set_return_value_for(GreaseType.Float,Operation.LT,GreaseType.Int,GreaseType.Bool)
obj.set_return_value_for(GreaseType.Float,Operation.LT,GreaseType.Float,GreaseType.Bool)
obj.set_return_value_for(GreaseType.Int,Operation.GE,GreaseType.Int,GreaseType.Bool)
obj.set_return_value_for(GreaseType.Int,Operation.GE,GreaseType.Float, GreaseType.Bool)
obj.set_return_value_for(GreaseType.Float,Operation.GE,GreaseType.Int,GreaseType.Bool)
obj.set_return_value_for(GreaseType.Float,Operation.GE,GreaseType.Float,GreaseType.Bool)
obj.set_return_value_for(GreaseType.Int,Operation.GT,GreaseType.Int,GreaseType.Bool)
obj.set_return_value_for(GreaseType.Int,Operation.GT,GreaseType.Float, GreaseType.Bool)
obj.set_return_value_for(GreaseType.Float,Operation.GT,GreaseType.Int,GreaseType.Bool)
obj.set_return_value_for(GreaseType.Float,Operation.GT,GreaseType.Float,GreaseType.Bool)
obj.set_return_value_for(GreaseType.Int,Operation.LE,GreaseType.Int,GreaseType.Bool)
obj.set_return_value_for(GreaseType.Int,Operation.LE,GreaseType.Float, GreaseType.Bool)
obj.set_return_value_for(GreaseType.Float,Operation.LE,GreaseType.Int,GreaseType.Bool)
obj.set_return_value_for(GreaseType.Float,Operation.LE,GreaseType.Float,GreaseType.Bool)
obj.set_return_value_for(GreaseType.Int,Operation.NOT,GreaseType.Int,GreaseType.Bool)
obj.set_return_value_for(GreaseType.Int,Operation.NOT,GreaseType.Float, GreaseType.Bool)
obj.set_return_value_for(GreaseType.Float,Operation.NOT,GreaseType.Int,GreaseType.Bool)
obj.set_return_value_for(GreaseType.Float,Operation.NOT,GreaseType.Float,GreaseType.Bool)
obj.set_return_value_for(GreaseType.Int,Operation.ASSIGN,GreaseType.Int,GreaseType.Bool)
obj.set_return_value_for(GreaseType.Float,Operation.ASSIGN,GreaseType.Float,GreaseType.Bool)
import pprint 
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
obj.set_return_value_for('int', '+', 'int', 'int')
obj.set_return_value_for('int', '+', 'float', 'float')
obj.set_return_value_for('float', '+', 'float', 'float')
obj.set_return_value_for('float', '+', 'int', 'float')
obj.set_return_value_for('string','+','string','string')
obj.set_return_value_for('int','-','int','int')
obj.set_return_value_for('int','-','float','float')
obj.set_return_value_for('float','-','int','float')
obj.set_return_value_for('float','-','float','float')
obj.set_return_value_for('int','*','int','')
import pprint as pp
from grease.core.type import GreaseTypeClass
from grease.core.quadruple import Operation

class SemanticCube(object):
  """docstring for SemanticCube"""
  def __init__(self):
    self.cube = {}

  def set_return_value_for(self, left, op, right, res):
    if not isinstance(left, GreaseTypeClass) or not isinstance(right, GreaseTypeClass) \
      or not isinstance(op, Operation) or not isinstance(res, GreaseTypeClass):
        return False
    
    if op not in self.cube:
      self.cube[op] = {}

    if left not in self.cube[op]:
      self.cube[op][left] = {}

    self.cube[op][left][right] = res

    return True

  def check(self, lhs, op, rhs):
    try:
      return self.cube[op][lhs.type.type_class][rhs.type.type_class]
    except:
      return None

  def print_cube(self):
    pp.print(self)

cube = SemanticCube()
cube.set_return_value_for(GreaseTypeClass.Int, Operation.PLUS, GreaseTypeClass.Int, GreaseTypeClass.Int)
cube.set_return_value_for(GreaseTypeClass.Int, Operation.PLUS, GreaseTypeClass.Float, GreaseTypeClass.Float)
cube.set_return_value_for(GreaseTypeClass.Float, Operation.PLUS, GreaseTypeClass.Float, GreaseTypeClass.Float)
cube.set_return_value_for(GreaseTypeClass.Float, Operation.PLUS, GreaseTypeClass.Int, GreaseTypeClass.Float)
cube.set_return_value_for(GreaseTypeClass.Int, Operation.MINUS, GreaseTypeClass.Int, GreaseTypeClass.Int)
cube.set_return_value_for(GreaseTypeClass.Int, Operation.MINUS, GreaseTypeClass.Float, GreaseTypeClass.Float)
cube.set_return_value_for(GreaseTypeClass.Float, Operation.MINUS, GreaseTypeClass.Int, GreaseTypeClass.Float)
cube.set_return_value_for(GreaseTypeClass.Float, Operation.MINUS, GreaseTypeClass.Float, GreaseTypeClass.Float)
cube.set_return_value_for(GreaseTypeClass.Int, Operation.U_MINUS, None, GreaseTypeClass.Int)
cube.set_return_value_for(GreaseTypeClass.Float, Operation.U_MINUS, None, GreaseTypeClass.Float)
cube.set_return_value_for(GreaseTypeClass.Int, Operation.TIMES, GreaseTypeClass.Int, GreaseTypeClass.Int)
cube.set_return_value_for(GreaseTypeClass.Int, Operation.TIMES, GreaseTypeClass.Float, GreaseTypeClass.Float)
cube.set_return_value_for(GreaseTypeClass.Float, Operation.TIMES, GreaseTypeClass.Int, GreaseTypeClass.Float)
cube.set_return_value_for(GreaseTypeClass.Float, Operation.TIMES, GreaseTypeClass.Float, GreaseTypeClass.Float)
cube.set_return_value_for(GreaseTypeClass.Int, Operation.DIVIDE, GreaseTypeClass.Int, GreaseTypeClass.Int)
cube.set_return_value_for(GreaseTypeClass.Int, Operation.DIVIDE, GreaseTypeClass.Float, GreaseTypeClass.Float)
cube.set_return_value_for(GreaseTypeClass.Float, Operation.DIVIDE, GreaseTypeClass.Int, GreaseTypeClass.Float)
cube.set_return_value_for(GreaseTypeClass.Float, Operation.DIVIDE, GreaseTypeClass.Float, GreaseTypeClass.Float)
cube.set_return_value_for(GreaseTypeClass.Int, Operation.EQ, GreaseTypeClass.Int, GreaseTypeClass.Bool)
cube.set_return_value_for(GreaseTypeClass.Int, Operation.EQ, GreaseTypeClass.Float, GreaseTypeClass.Bool)
cube.set_return_value_for(GreaseTypeClass.Float, Operation.EQ, GreaseTypeClass.Int, GreaseTypeClass.Bool)
cube.set_return_value_for(GreaseTypeClass.Float, Operation.EQ, GreaseTypeClass.Float, GreaseTypeClass.Bool)
cube.set_return_value_for(GreaseTypeClass.Int, Operation.LT, GreaseTypeClass.Int, GreaseTypeClass.Bool)
cube.set_return_value_for(GreaseTypeClass.Int, Operation.LT, GreaseTypeClass.Float, GreaseTypeClass.Bool)
cube.set_return_value_for(GreaseTypeClass.Float, Operation.LT, GreaseTypeClass.Int, GreaseTypeClass.Bool)
cube.set_return_value_for(GreaseTypeClass.Float, Operation.LT, GreaseTypeClass.Float, GreaseTypeClass.Bool)
cube.set_return_value_for(GreaseTypeClass.Int, Operation.GE, GreaseTypeClass.Int, GreaseTypeClass.Bool)
cube.set_return_value_for(GreaseTypeClass.Int, Operation.GE, GreaseTypeClass.Float, GreaseTypeClass.Bool)
cube.set_return_value_for(GreaseTypeClass.Float, Operation.GE, GreaseTypeClass.Int, GreaseTypeClass.Bool)
cube.set_return_value_for(GreaseTypeClass.Float, Operation.GE, GreaseTypeClass.Float, GreaseTypeClass.Bool)
cube.set_return_value_for(GreaseTypeClass.Int, Operation.GT, GreaseTypeClass.Int, GreaseTypeClass.Bool)
cube.set_return_value_for(GreaseTypeClass.Int, Operation.GT, GreaseTypeClass.Float, GreaseTypeClass.Bool)
cube.set_return_value_for(GreaseTypeClass.Float, Operation.GT, GreaseTypeClass.Int, GreaseTypeClass.Bool)
cube.set_return_value_for(GreaseTypeClass.Float, Operation.GT, GreaseTypeClass.Float, GreaseTypeClass.Bool)
cube.set_return_value_for(GreaseTypeClass.Int, Operation.LE, GreaseTypeClass.Int, GreaseTypeClass.Bool)
cube.set_return_value_for(GreaseTypeClass.Int, Operation.LE, GreaseTypeClass.Float, GreaseTypeClass.Bool)
cube.set_return_value_for(GreaseTypeClass.Float, Operation.LE, GreaseTypeClass.Int, GreaseTypeClass.Bool)
cube.set_return_value_for(GreaseTypeClass.Float, Operation.LE, GreaseTypeClass.Float, GreaseTypeClass.Bool)
cube.set_return_value_for(GreaseTypeClass.Bool, Operation.NOT, None, GreaseTypeClass.Bool)
cube.set_return_value_for(GreaseTypeClass.Int, Operation.ASSIGN, GreaseTypeClass.Int, GreaseTypeClass.Bool)
cube.set_return_value_for(GreaseTypeClass.Float, Operation.ASSIGN, GreaseTypeClass.Float, GreaseTypeClass.Bool)


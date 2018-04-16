from enum import Enum
from grease.core.stack import Stack
from grease.core.type import GreaseTypeClass

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
  PRINT = 17
  SCAN = 18
  HALT = 19
  RETURN = 20
  ERA = 21
  PARAM = 22
  GOSUB = 23
  ADDR = 24

class Quadruple(object):
  def __init__(self, operation, lhs=None, rhs=None, result=None):
    self.operator = operation
    self.left_operand = lhs
    self.right_operand = rhs
    self.result = result

  def to_list(self):
    op = Operation(self.operator).value
    return [op, self.left_operand, self.right_operand, self.result]

class QuadrupleStore:
  def __init__(self):
    self.quads = []
    self.next_free_quad = 0

  def push_quad(self, quad):
    quad.address = self.next_free_quad
    self.quads.append(quad)
    self.next_free_quad += 1
          
  def pop_quad(self):
    self.next_free_quad -= 1
    return self.quads.pop()

  def fill_quad(self, quad_id, value):
    self.quads[quad_id].result = value

  def print_all(self):
    """prints all quadruples from list """
    count = 0
    print("Quads ===============================")
    #Traer lista de cuadruplos
    l = [x.get_list() for x in self.quads]
    #mientras el elemento(cuadruplo) este en la lista
    for e in l:
      print(str(count), end=':\t')
      #por cada single element en el elemento (cuadruplo)
      for se in e:
        if not se == None:
          print(str(se), end='')
        print(end='\t')
      count += 1
      print()
    pass

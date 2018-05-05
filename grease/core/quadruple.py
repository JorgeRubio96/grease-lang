from enum import Enum
from grease.core.stack import Stack
from grease.core.type import GreaseTypeClass
from grease.core.variable import AddressingMethod
from sys import byteorder

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
  GOSUB = 22
  ADDR = 23
  VER = 24
  PARAM = 25
  ACCESS = 25
  DEREF = 26

class Quadruple(object):
  def __init__(self, operation, lhs=None, rhs=None, result=None):
    self.operator = operation
    self.left_operand = lhs
    self.right_operand = rhs
    self.result = result

  def to_list(self, global_offset):
    op = Operation(self.operator).value
    
    if self.left_operand is None:
      lhs = None
    else:
      lhs = self.left_operand.address
      if self.left_operand.method is AddressingMethod.Direct:
        lhs += global_offset * 4


    if self.right_operand is None:
      rhs = None
    else:
      rhs = self.right_operand.address
      if self.right_operand.method is AddressingMethod.Direct:
        rhs += global_offset * 4

    if self.result is None:
      res = None
    else:
      res = self.result.address
      if self.result.method is AddressingMethod.Direct:
        res += global_offset * 4

    return [op, lhs, rhs, res]

class QuadrupleStore:
  def __init__(self):
    self._quads = []
    self.next_free_quad = 0

  def push_quad(self, quad):
    quad.address = self.next_free_quad
    self._quads.append(quad)
    self.next_free_quad += 1
          
  def pop_quad(self):
    self.next_free_quad -= 1
    return self._quads.pop()

  def fill_quad(self, quad_no, value):
    self._quads[quad_no].result = value

  def write_to_file(self, out_file):
    for quad in self._quads:
      for el in quad.to_list(self.next_free_quad):
        if el is None:
          out_file.write((0).to_bytes(8, byteorder))
        else:
          out_file.write(el.to_bytes(8,byteorder))


  def print_all(self):
    """prints all quadruples from list """
    count = 0
    print("Quads ===============================")
    #Traer lista de cuadruplos
    l = [x.to_list(self.next_free_quad) for x in self._quads]
    #mientras el elemento(cuadruplo) este en la lista
    for e in l:
      print(str(count), end=':  ')
      #por cada single element en el elemento (cuadruplo)
      for se in e:
        if not se == None:
          print(format(se, '#018x'), end='  ')
        else:
          print('                  ', end='  ')
      count += 1
      print()
    pass

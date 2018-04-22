from grease.core.struct import GreaseStruct
from grease.core.variable import GreaseVar
from grease.core.type import GreaseTypeClass, GreaseType
from grease.core.function import GreaseFn
from grease.core.quadruple import Quadruple, QuadrupleStore, Operation
from grease.core.variable_table import VariableTable
from grease.core.struct_table import StructTable
from grease.core.interface_table import InterfaceTable
from grease.core.function_directory import FunctionDirectory
from grease.core.exceptions import TypeMismatch, UndefinedVariable, UndefinedFunction
from grease.core.exceptions import UndefinedMember, UndefinedType, UndefinedInterface, UndefinedStruct
from grease.core.stack import Stack
from grease.core.substruct import SubstructNodeType
from grease.semantic_cube import cube

type_class_dict = {
  'Int': GreaseTypeClass.Int,
  'Float': GreaseTypeClass.Float,
  'Char': GreaseTypeClass.Char,
  'Bool': GreaseTypeClass.Bool,
}

operators_dict = {
  'TIMES' : Operation.TIMES,
  'DIVIDE' : Operation.DIVIDE, 
  'PLUS' : Operation.PLUS,
  'MINUS' : Operation.MINUS,
  'EQ' : Operation.EQ,
  'GT' : Operation.GT,
  'LT' : Operation.LT,
  'GE' : Operation.GE,
  'LE' : Operation.LE,
  'NOT' : Operation.NOT,
  'ASSIGN' : Operation.ASSIGN,
  'U_MINUS' : Operation.U_MINUS,
  'JMP_F' : Operation.JMP_F,
  'JMP' : Operation.JMP,
  'AND' : Operation.AND,
  'OR' : Operation.OR,
  'PRINT' : Operation.PRINT,
  'SCAN' : Operation.SCAN
}

class Greaser:
  def __init__(self):
    self._global_vars = VariableTable()
    self._global_fns = FunctionDirectory()
    self._structs = StructTable()
    self._scope = self._global_vars
    self._interfaces = InterfaceTable()
    self._operator_stack = Stack()
    self._operand_stack = Stack()
    self._jump_stack = Stack()
    self._agregate_stack = Stack()
    self._quads = QuadrupleStore()
    self._next_local_address = 0x3000000000000000
    self._next_global_address = 0x0000000000000000

  def find_function(self, name):
    fn = self._global_fns.find_function(name)

    if fn is None:
      raise UndefinedFunction(name)
    
    return fn

  def find_variable(self, name):
    var = self._scope.find_variable(name)

    if var is None:
      raise UndefinedVariable(name)

    return var

  def find_struct(self, name):
    struct = self._structs.find_struct(name)

    if struct is None:
      raise UndefinedStruct(name)

    return struct

  def find_type(self, name):
    struct = self._structs.find_struct(name)

    if struct is not None:
      return GreaseType(GreaseTypeClass.Struct, struct)
    
    interface = self._interfaces.find_interface(name)  
    
    if interface is not None:
      return GreaseType(GreaseTypeClass.Interface, interface)

    raise UndefinedType(name)

  def find_interface(self, name):
    interface = self._interfaces.find_interface(name)

    if interface is None:
      raise UndefinedInterface(name)

    return interface

  def add_variable(self, name, var):
    if self._scope is self._global_vars:
      var.address = self._next_global_address
      self._next_global_address += var.type.size
    else:
      var.address = self._next_local_address
      self._next_local_address += var.type.size

    self._scope.add_variable(name,var)

  def add_function(self, name, fn, struct=None):
    fn.start = self._quads.next_free_quad
    if struct is not None:
      struct.functions.add_function(name, fn)
    else:
      self._global_fns.add_function(name, fn)

  def add_struct(self, name, struct):
    self._structs.add_struct(name, struct)

  def add_interface(self, name, interface):
    self._interfaces.add_interface(name, interface)

  def open_scope(self, scope):
    scope.parent = self._scope
    self._scope = scope

  def close_scope(self):
    self._scope = self._scope.parent

  def push_operator(self, operator):
    self._operator_stack.push(operator)

  def check_top_operator(self, operators):
    if self._operator_stack.peek() in operators:
      self.make_expression()
  
  def push_operand(self, operand):
    self._operand_stack.push(operand)

  def push_agregate_stack(self):
    self._agregate_stack.push(self._operand_stack.pop())
    pass

  def make_jump(self, to=None):
    if to is None:
      self._jump_stack.push(self._quads.next_free_quad)
      quad = Quadruple(Operation.JMP)
    else:
      quad = Quadruple(Operation.JMP, lhs=0X2000000000000000 + to)

    self._quads.push_quad(quad)
  
  def make_jump_f(self, to=None):
    if to is None:
      self._jump_stack.push(self._quads.next_free_quad)
      quad = Quadruple(Operation.JMP_F)
    else:
      quad = Quadruple(Operation.JMP_F, lhs=0X2000000000000000 + to)
    
    self._quads.push_quad(quad)

  def fill_jump(self):
    quad_no = self._jump_stack.pop()

    if quad_no is not None:
      next_quad = self._quads.next_free_quad
      self._quads.fill_quad(quad_no, 0X2000000000000000 + next_quad)
    else:
      raise GreaseError('No jumps pending to be resolved')

  #Exp quad helper
  def make_expression(self):
    """Exp quad helper:
    Pops 2 operands from typestack and operand stack, checks type and calls build_and_push_quad"""
    op = self._operator_stack.pop()
    
    t2 = self._operator_stack.pop()
    t1 = self._operator_stack.pop()
    
    return_type_class = cube.check(t1, op, t2)
    
    if return_type_class is None:
      raise TypeMismatch('{} {} {}'.format(t1, op, t2))

    tmp_type = GreaseType(return_type_class)
    tmp_var = GreaseVar(tmp_type, addr)

    # Generate Quadruple and push it to the list
    quad = Quadruple(op, lhs, rhs, tmp_var)
    self._quads.push_quad(quad)

    # push the tmp_var to stack
    self._operand_stack.push(tmp_var)
  
  def make_assign(self, lhs):
    t1 = self._type_stack.pop()
    t2 = self._type_stack.pop()
    if t1 != t2:
      raise TypeMismatch('')
    op = self._operator_stack.pop()
    o1 = self._operand_stack.pop()
    o2 = self._operand_stack.pop()
    print(">Second Operand {}".format(o2))

    #generate quad and push it to the list
    Greaser.build_and_push_quad(op, o1, None, o2)

  def resolve_main(self):
    main = self.find_function('main')
    jump_to_main = self._jump_stack.pop()

    self._quads.fill_quad(jump_to_main, 0X2000000000000000 + main.start)

  def print_stacks(self):
    """Print Stacks

    Prints the operand, operator and type stack
    """
    print("> Operand Stack = ")
    self._operand_stack.pprint()

    print("> Operator Stack = ")
    self._operator_stack.pprint()

  def reset_local_address(self):
    self._next_local_address = 0x3000000000000000

  @staticmethod
  def basic_type_from_text(name):
    return GreaseType(type_class_dict.get(name))

  @staticmethod
  def operator_from_text(text):
    return operators_dict.get(text)


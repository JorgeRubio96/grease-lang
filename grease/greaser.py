from grease.core.struct import GreaseStruct
from grease.core.variable import GreaseVar
from grease.core.type import GreaseTypeClass, GreaseType
from grease.core.function import GreaseFn
from grease.core.quadruple import Quadruple, QuadrupleStore, Operation
from grease.core.variable_table import VariableTable
from grease.core.struct_table import StructTable
from grease.core.interface_table import InterfaceTable
from grease.core.function_directory import FunctionDirectory
from grease.core.exceptions import TypeMismatch, UndefinedVariable, UndefinedFunction, GreaseError
from grease.core.exceptions import UndefinedMember, UndefinedType, UndefinedInterface, UndefinedStruct
from grease.core.stack import Stack
from grease.core.substruct import SubstructNodeType
from grease.semantic_cube import cube
from sys import byteorder

type_class_dict = {
  'Int'  : GreaseTypeClass.Int,
  'Float': GreaseTypeClass.Float,
  'Char' : GreaseTypeClass.Char,
  'Bool' : GreaseTypeClass.Bool,
}

operators_dict = {
  '*' : Operation.TIMES,
  '/' : Operation.DIVIDE, 
  '+' : Operation.PLUS,
  '-' : Operation.MINUS,
  'eq' : Operation.EQ,
  'gt' : Operation.GT,
  'lt' : Operation.LT,
  'ge' : Operation.GE,
  'le' : Operation.LE,
  'not' : Operation.NOT,
  '=' : Operation.ASSIGN,
  'and' : Operation.AND,
  'or' : Operation.OR,
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
    self._active_fn = None
    self._next_param = 0

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

  def top_operand_type(self):
    return self._operand_stack.peek().type

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

  def push_constant(self, cnst):
    t = GreaseType(GreaseTypeClass.Int)
    self._operand_stack.push(GreaseVar(t,0X2000000000000000 + cnst))

  def make_jump(self, to_stack=False):
    if to_stack:
      to = self._jump_stack.pop()
      quad = Quadruple(Operation.JMP, result=0X2000000000000000 + to)
    else:
      self._jump_stack.push(self._quads.next_free_quad)
      quad = Quadruple(Operation.JMP)

    self._quads.push_quad(quad)
  
  def make_jump_f(self):
    self._jump_stack.push(self._quads.next_free_quad)
    quad = Quadruple(Operation.JMP_F)
    
    self._quads.push_quad(quad)

  def push_jmp(self):
    self._jump_stack.push(self._quads.next_free_quad)

  def fill_jump(self):
    quad_no = self._jump_stack.pop()

    if quad_no is not None:
      next_quad = self._quads.next_free_quad
      self._quads.fill_quad(quad_no, 0X2000000000000000 + next_quad)
    else:
      raise GreaseError('No jumps pending to be resolved')

  def make_fn_call(self, fn):
    era = Quadruple(Operation.ERA, fn.size)
    self._quads.push_quad(era)
    self._active_fn = fn
    self._next_param = 0

  def make_param(self):
    arg = self._operand_stack.pop()
    param = self._active_fn.params[self._next_param]

    if not Greaser.can_assign(arg.type, param.type):
      raise TypeMismatch('Found {} but expected {} in arg {}'.format(arg, param, self._next_param))

    param_quad = Quadruple(Operation.PARAM, arg.address, result=self._next_param)
    
    self._quads.push_quad(param_quad)

  #Exp quad helper
  def make_expression(self):
    """Exp quad helper:
    Pops 2 operands from typestack and operand stack, checks type and calls build_and_push_quad"""
    op = self._operator_stack.pop()
    
    rhs = self._operand_stack.pop()
    lhs = self._operand_stack.pop()
    
    return_type_class = cube.check(lhs, op, lhs)
    
    if return_type_class is None:
      raise TypeMismatch('{} {} {}'.format(lhs, op, rhs))

    tmp_type = GreaseType(return_type_class)
    tmp_var = GreaseVar(tmp_type, self._next_local_address)

    self._next_local_address += 1

    # Generate Quadruple and push it to the list
    quad = Quadruple(op, lhs.address, rhs.address, tmp_var.address)
    self._quads.push_quad(quad)

    # push the tmp_var to stack
    self._operand_stack.push(tmp_var)
  
  def make_assign(self):
    expr = self._operand_stack.pop()
    var = self._operand_stack.pop()
    if var.type.type_class is not expr.type.type_class:
      raise TypeMismatch('')
    op = self._operator_stack.pop()

    #generate quad and push it to the list
    self._quads.push_quad(Quadruple(op, lhs=expr.address, result=var.address))

  def make_io(self, operator):
    expr = self._operand_stack.pop()

    self._quads.push_quad(Quadruple(operator, expr.address))

  def resolve_main(self):
    main = self.find_function('main')
    jump_to_main = self._jump_stack.pop()

    self._quads.fill_quad(jump_to_main, 0X2000000000000000 + main.start)
    self._quads.push_quad(Quadruple(Operation.HALT))

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

  def write_to_file(self, name):
    out_file = open(name, 'wb')
    out_file.write((2000).to_bytes(8, byteorder))
    self._quads.write_to_file(out_file)

  @staticmethod
  def basic_type_from_text(name):
    return GreaseType(type_class_dict.get(name))

  @staticmethod
  def operator_from_text(text):
    return operators_dict.get(text)

  @staticmethod
  def can_assign(type_l, type_r):
    
    if type_l.type_class is GreaseTypeClass.Array:
      # ArraysTypes cannot be assigned
      return False

    elif type_l.type_class is GreaseTypeClass.Struct:
      # StructTypes have struct variable in type_data
      return type_l.type_data is type_r.type_data

    elif type_l.type_class is GreaseTypeClass.Interface:
      # InterfaceTypes may be assigned an interface of the same type
      # or a struct that satisfies that interface
      if type_r.type_class is GreaseTypeClass.Interface:
        # InterfaceTypes have interface variable in type_data
        return type_l.type_data is type_r.type_data

      # Second type is struct. Check if it satisfies interface
      return type_r.type_data.has_interface(type_l.type_data)

    elif type_l.type_class is GreaseTypeClass.Pointer:
      # PointerTypes have type variable in type_data
      return Greaser.can_assign(type_l.type_data, type_r.type_data)

    # All other type_classes may be assigned to themselves
    return type_l.type_class is type_r.type_class

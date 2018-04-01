from grease.core.struct import GreaseStruct
from grease.core.variable import GreaseVar
from grease.core.type import GreaseTypeClass, GreaseType
from grease.core.function import GreaseFn
from grease.core.quadruple import Quadruple, Quadruples, Operation
from grease.semantic_cube import SemanticCube
from grease.core.variable_table import VariableTable
from grease.core.struct_table import StructTable
from grease.core.interface_table import InterfaceTable
from grease.core.function_directory import FunctionDirectory
from grease.core.exceptions import TypeMismatch, UndefinedVariable, UndefinedFunction, UndefinedMember, UndefinedType, UndefinedInterface
from grease.core.stack import Stack

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
  'CONST' : Operation.CONST,
  'WHILE' : Operation.WHILE,
  'PRINT' : Operation.PRINT,
  'SCAN' : Operation.SCAN,
  'EQUALS' : Operation.EQUALS,
  'IF' : Operation.IF,
  'ELSE' : Operation.ELSE
}

#Quads global structures
operator_stack = Stack()
operand_stack = Stack()
type_stack = Stack()
#Temp QuadQueue
tmp_quad_stack = Stack()

class Greaser:
  def __init__(self):
    self._global_vars = VariableTable()
    self._global_fns = FunctionDirectory()
    self._structs = StructTable()
    self._scope = self._global_vars
    self._current_fn = None
    self._interfaces = InterfaceTable()

  def find_function(self, name):
    fn_name = name.pop()
  
    if len(name) > 0:
      var = self.find_variable(name)

      if var.is_class(GreaseTypeClass.Struct) or var.is_class(GreaseTypeClass.Interface):
        fn = var.type.type_data.functions.find_function(fn_name)

      else:
        raise TypeMismatch('{}'.format(name) + 'is not a Struct or Interface')
    else:
      fn = self._global_fns.find_function(fn_name)

    if fn is None:
      raise UndefinedFunction(fn_name)
    
    return fn

  def find_variable(self, name):
    var_name = name[0]
    var = self._scope.find_variable(var_name)

    if var is None:
      raise UndefinedVariable(var_name)

    for var_name in name[1:]:
      if var.is_class(GreaseTypeClass.Struct) or var.is_class(GreaseTypeClass.Interface):
        struct = var.type.type_data
        var = struct.variables.find_variable(var_name)

        if var is None:
          raise UndefinedMember('{} in type {}'.format(var_name, type_name))
      else:
        raise TypeMismatch('\"{}\" is not a struct'.format(var_name))

    return var

  def find_struct(self, name):
    struct = self._structs.find_struct(name)

    if struct is None:
      raise UndefinedType(name)

    return struct

  def find_interface(self, name):
    interface = self._interfaces.find_interface(name)

    if interface is None:
      raise UndefinedInterface(name)

    return interface

  def add_variable(self, name, var):
    self._scope.add_variable(name,var)

  def add_function(self, name, fn, struct=None):
    if struct is not None:
      struct.functions.add_function(name, fn)
    else:
      self._global_fns.add_function(name, fn)

  def add_struct(self, name, struct):
    self._structs.add_struct(name, struct)

  def add_interface(self, name, interface):
    self._interfaces.add_interface(name, interface)

  def open_scope(self):
    self._scope = VariableTable(self._scope)

  def close_scope(self):
    self._scope = self._scope.parent

  @staticmethod
  def basic_type_from_text(name):
    return GreaseType(type_class_dict.get(name))


########################################################
  # Helper Functions for quadruples
  #Create quad
  @staticmethod
  def build_and_push_quad(op, l_op, r_op, res):
    tmp_quad = Quadruple()
    tmp_quad.build(op, l_op, r_op, res)
    Quadruples.push_quad(tmp_quad)

  #Exp quad helper
  @staticmethod
  def exp_quad_helper(p, op_list, operator_stack, type_stack,operand_stack):
    """Exp quad helper:
    Pops 2 operands from typestack and operand stack, checks type and calls build_and_push_quad"""
    if operator_stack.isEmpty():
      return
    op = operator_stack.peek()
    id_op = p.Operation(op).value
    if id_op in op_list:
      t1 = type_stack.pop()
      t2 = type_stack.pop()
      return_type = SemanticCube.cube[op][t1][t2]
    if return_type == -1:
      raise TypeMismatch('')
    o1 = operand_stack.pop()
    o2 = operand_stack.pop()
    tmp_var_id = SemanticInfo.get_next_var_address(return_type)

    # Generate Quadruple and push it to the list
    Greaser.build_and_push_quad(op, o2, o1, tmp_var_id)
    operator_stack.pop()

    # push the tmp_var_id and the return type to stack
    operand_stack.push(tmp_var_id)
    type_stack.push(return_type)

    print("\n> PUSHING OPERATOR '{}' -> op2 = {}, op1 = {}, res = {}".format(str_op, o2, o1, tmp_var_id))
    Greaser.print_stacks()

  @staticmethod
  def push_const_operand_and_type(operand, type):
    '''Builds the constant quadruple for operands and type'''
    type_stack.push(type_class_dict[type])
    if operand in operators_dict.keys():
      operand_stack.push(operators_dict[operand])
    return

  @staticmethod
  def assign_quad_helper(p):
    t1 = type_stack.pop()
    t2 = type_stack.pop()
    if t1 != t2:
      raise TypeMismatch('')
    op = operator_stack.pop()
    o1 = operand_stack.pop()
    o2 = operand_stack.pop()
    print(">Second Operand {}".format(o2))

    #generate quad and push it to the list
    Greaser.build_and_push_quad(op, o1, None, o2)

  @staticmethod
  def print_stacks():
    """Print Stacks

    Prints the operand, operator and type stack
    """
    print("> Operand Stack = ")
    operand_stack.pprint()

    print("> Operator Stack = ")
    operator_stack.pprint()

    print("> Type Stack = ")
    type_stack.pprint()

########################################################

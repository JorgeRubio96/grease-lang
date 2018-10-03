from grease.core.variable import GreaseVar, AddressingMethod
from grease.core.type import GreaseTypeClass, GreaseType
from grease.core.quadruple import Quadruple, QuadrupleStore, Operation
from grease.core.variable_table import VariableTable
from grease.core.struct_table import StructTable
from grease.core.interface_table import InterfaceTable
from grease.core.function_directory import FunctionDirectory
from grease.core.exceptions import TypeMismatch, UndefinedVariable, UndefinedFunction, GreaseError
from grease.core.exceptions import UndefinedMember, UndefinedType, UndefinedInterface, UndefinedStruct
from grease.core.stack import Stack
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
    self._interfaces = InterfaceTable()
    self._quads = QuadrupleStore()
    
    self._operator_stack = Stack()
    self._operand_stack = Stack()
    self._jump_stack = Stack()
    self._agregate_stack = Stack()
    self._era_stack = Stack()
    
    self._scope = self._global_vars
    self._param_quads = []
   
    self._next_local_address = 0
    self._next_global_address = 0
    self._next_param = 0
    self._dim = 0
    
    self._active_fn = None
    self._parsing_fn = None

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
      return GreaseType(GreaseTypeClass.Struct, struct, size=struct.size)
    
    interface = self._interfaces.find_interface(name)  
    
    if interface is not None:
      return GreaseType(GreaseTypeClass.Intererface, interface)

    raise UndefinedType(name)

  def find_interface(self, name):
    interface = self._interfaces.find_interface(name)

    if interface is None:
      raise UndefinedInterface(name)

    return interface

  def add_variable(self, name, var):
    if self._scope is self._global_vars:
      var._address = self._next_global_address
      var.method = AddressingMethod.Direct
      self._next_global_address += var.type.size
    else:
      var._address = self._next_local_address
      var.method = AddressingMethod.Relative
      self._next_local_address += var.type.size

    self._scope.add_variable(name,var)

  def add_function(self, name, fn, struct=None):
    if name is None:
      raise SyntaxError()

    fn.start = self._quads.next_free_quad
    # Frame pointer and return address are in the
    # first two momry locations of the stack
    self.reset_local_address(len(fn.param_types) + 2)
    if struct is not None:
      struct.functions.add_function(name, fn)
    else:
      self._global_fns.add_function(name, fn)

    self._active_fn = fn

  def add_struct(self, name, struct):
    self._structs.add_struct(name, struct)

  def add_interface(self, name, interface):
    self._interfaces.add_interface(name, interface)

  def open_scope(self, scope):
    scope.parent = self._scope
    self._scope = scope

  def close_scope(self):
    self._scope = self._scope.parent

  def pop_fake_bottom(self):
    if self._operator_stack.pop() is not '(':
      raise GreaseError("Not Fake bottom")

  def push_fake_bottom(self):
    self._operator_stack.push('(')

  def push_jmp(self):
    self._jump_stack.push(self._quads.next_free_quad)

  def push_fn_size(self):
    self._active_fn.size = self._next_local_address
    while self._era_stack.peek() is not None:
      quad = self._quads._quads[self._era_stack.pop()]
      quad.left_operand = GreaseVar(GreaseType(GreaseTypeClass.Int), self._next_local_address, AddressingMethod.Literal)

  def push_return(self, with_data=False):
    return_quad = Quadruple(Operation.RETURN)
    
    if with_data:
      data = self._operand_stack.pop()
      return_reg = GreaseVar(self._active_fn.return_type, self._next_global_address)

      if data is None:
        raise GreaseError('No data to return!')

      if not self.can_assign(return_reg, data):
        raise TypeMismatch('Return type is not compatible with function')

      return_quad.left_operand = data
      return_quad.result = return_reg
    
    self._quads.push_quad(return_quad)
  
  def push_constant(self, cnst, cnst_type):
    self._operand_stack.push(GreaseVar(cnst_type, cnst, AddressingMethod.Literal))

  def push_substruct(self, name):    
    if self._operator_stack.peek() is Operation.ACCESS:
      self._operator_stack.pop() # This operation can not be executed by VM
      parent = self._operand_stack.pop()

      if parent is None:
        raise UndefinedVariable('Struct does not exist')

      if self._operator_stack.peek() is Operation.DEREF:
        self._operand_stack.pop() # This operation can not be executed by VM
        if parent.type.type_class is not GreaseTypeClass.Pointer:
          raise GreaseError('Expected pointer')

        parent_addr = GreaseVar(parent.type, parent._address, parent.method)
        parent_type = parent.type.type_data
      else:
        parent_addr = GreaseVar(GreaseType(GreaseTypeClass.Pointer, parent.type), parent._address, parent.method)
        parent_type = parent.type

      if parent_type.type_class is not GreaseTypeClass.Struct:
        raise TypeMismatch('Expression must be struct')

      var_table = parent_type.type_data.variables
      var = var_table.find_variable(name)

      if var is None:
        raise UndefinedMember(name)

      offset = GreaseVar(GreaseType(GreaseTypeClass.Int), var._address, AddressingMethod.Literal)
      parent_addr.type.type_data = var.type
      
      self.push_operand(offset)
      self.push_operand(parent_addr)
      self.make_offset(var.type)
    else:
      var = self.find_variable(name)
      self.push_operand(var)

  def push_operator(self, operator):
    self._operator_stack.push(operator)

  def check_top_operator(self, operators):
    if self._operator_stack.peek() in operators:
      self.make_expression()

  def top_operand_type(self):
    operand = self._operand_stack.peek()
    if operand is None:
      raise GreaseError('Empty operand stack!')

    return operand.type 
  
  def push_operand(self, operand):
    self._operand_stack.push(operand)

  def push_agregate_stack(self):
    arr = self._operand_stack.pop()
    if arr.type.type_class is not GreaseTypeClass.Array:
      raise TypeMismatch("Operand is not array.")
    self._agregate_stack.push(arr)
    self.push_fake_bottom()
    self._dim = 0

  def push_dim_stack(self):
    arr = self._agregate_stack.peek()
    if len(arr.type.dimens) > self._dim : #if the next pointer is different from null then
      t = self._operand_stack.peek()
      size = GreaseVar(GreaseType(GreaseTypeClass.Int), arr.type.dimens[self._dim].size, AddressingMethod.Literal)
      offset = GreaseVar(GreaseType(GreaseTypeClass.Int), arr.type.dimens[self._dim].offset, AddressingMethod.Literal)
      ver = Quadruple(Operation.VER, t, size)
      self._quads.push_quad(ver)
      self.push_operator(Operation.TIMES)
      self.push_operand(offset)
      self.make_expression()
    if self._dim > 0:
      self._operator_stack.push(Operation.PLUS)
      self.make_expression()
  
  def add_dim(self):
    self._dim = self._dim + 1
    #actualizar DIM EN PILADIMENSIONADAS

  def set_arr_add(self):
    arr = self._agregate_stack.pop()

    arr_addr = GreaseVar(GreaseType(GreaseTypeClass.Pointer, arr.type.type_data), arr._address, arr.method)

    self._operand_stack.push(arr_addr)
    self.make_offset(arr.type.type_data)
    self.pop_fake_bottom()

  def make_addr(self):
    aux = self._operand_stack.pop()
    temp = GreaseVar(GreaseType(GreaseTypeClass.Int), self._next_local_address, AddressingMethod.Relative)
    quad = Quadruple(Operation.ADDR, aux, result=temp)
    self._quads.push_quad(quad)
    self.push_operand(temp)
    self._next_local_address += 1

  def make_gosub(self):
    self.pop_fake_bottom()

    if self._next_param < len(self._parsing_fn.param_types):
      raise UndefinedFunction('Invalid function signature. Check argument count.')

    # Recursive functions dont have their size
    # calculated yet. Add them to era stack.
    if self._parsing_fn is self._active_fn:
      self._era_stack.push(self._quads.next_free_quad)
    size = GreaseVar(GreaseType(GreaseTypeClass.Int), self._parsing_fn.size, AddressingMethod.Literal)

    # Make ERA
    era = Quadruple(Operation.ERA, size)
    self._quads.push_quad(era)

    for param_quad in self._param_quads:
      self._quads.push_quad(param_quad)

    self._param_quads = []
    
    start = GreaseVar(GreaseType(GreaseTypeClass.Int), self._parsing_fn.start, AddressingMethod.Literal)
    gosub = Quadruple(Operation.GOSUB, start)
    self._quads.push_quad(gosub)

    if self._parsing_fn.return_type is not None:
      return_var = GreaseVar(self._parsing_fn.return_type, self._next_global_address)
      temp = GreaseVar(return_var.type, self._next_local_address, AddressingMethod.Relative)
      self._next_local_address += temp.type.size
      self._quads.push_quad(Quadruple(Operation.ASSIGN, return_var, result=temp))
      self.push_operand(temp)
  
  def make_fn(self, name):
    self.push_fake_bottom()
    self._parsing_fn = self.find_function(name)

    if self._parsing_fn is None:
      raise UndefinedFunction(name)
    
    self._next_param = 0

  def make_deref(self):
    pointer = self._operand_stack.pop()

    if pointer.type.type_class is not GreaseTypeClass.Pointer:
      raise TypeMismatch('Expression is not a pointer')

    # Copy address to stack in order to treat all pointers as relative addresses
    pointer_addr = GreaseVar(pointer.type, self._next_local_address, AddressingMethod.Relative)
    pointer_deref = GreaseVar(pointer.type, pointer_addr._address, AddressingMethod.Indirect)

    self._quads.push_quad(Quadruple(Operation.ASSIGN, pointer, result=pointer_addr))
    self.push_operand(pointer_deref)

  def make_offset(self, var_type):
    self.push_operator(Operation.PLUS)
    self.make_expression()
    res = self._operand_stack.pop()
    res.type = GreaseType(GreaseTypeClass.Pointer, res.type)

    res_ref = GreaseVar(GreaseType(GreaseTypeClass.Pointer, var_type), res._address, AddressingMethod.Indirect)
    self._operand_stack.push(res_ref)

  def make_param(self):
    arg = self._operand_stack.pop()
    param_type = self._parsing_fn.param_types[self._next_param]

    # Params start at the third address location in the stack.
    # The first two are occupied by the previous FP and PC
    param = GreaseVar(param_type, self._next_param + 2, AddressingMethod.Relative)

    if not Greaser.can_assign(arg, param):
      raise TypeMismatch('Found {} but expected {} in arg {}'.format(arg.type, param_type, self._next_param))

    param_quad = Quadruple(Operation.PARAM, arg, result=param)
    self._param_quads.append(param_quad)
    self._next_param += 1

  #Exp quad helper
  def make_expression(self):
    """Exp quad helper:
    Pops 2 operands from typestack and operand stack, checks type and calls build_and_push_quad"""
    op = self._operator_stack.pop()
    
    rhs = self._operand_stack.pop()

    if op is Operation.ADDR:
      self.make_addr()
    elif op is Operation.DEREF:
      self.make_deref()
    elif op in [Operation.U_MINUS, Operation.NOT]:
      return_type_class = cube.check(rhs,op,None)
      
      if return_type_class is None:
        raise TypeMismatch('{} {}'.format(op, rhs))

      tmp_var = GreaseVar(GreaseType(return_type_class), self._next_local_address, AddressingMethod.Relative)
      self._next_local_address += tmp_var.type.size
      self._quads.push_quad(Quadruple(op, rhs, result=tmp_var))
      self.push_operand(tmp_var)
    else:
      lhs = self._operand_stack.pop()
      
      return_type_class = cube.check(lhs, op, lhs)
      
      if return_type_class is None:
        raise TypeMismatch('{} {} {}'.format(lhs, op, rhs))

      tmp_type = GreaseType(return_type_class)
      tmp_var = GreaseVar(tmp_type, self._next_local_address, AddressingMethod.Relative)

      self._next_local_address += tmp_var.type.size

      # Generate Quadruple and push it to the list
      quad = Quadruple(op, lhs, rhs, tmp_var)
      self._quads.push_quad(quad)

      # push the tmp_var to stack
      self._operand_stack.push(tmp_var)
  
  def make_assign(self):
    expr = self._operand_stack.pop()
    var = self._operand_stack.pop()

    if var is None or expr is None:
      raise GreaseError('Assigning None values')
    
    if not self.can_assign(var, expr):
      raise TypeMismatch('Expression can not be assigned')

    #generate quad and push it to the list
    self._quads.push_quad(Quadruple(Operation.ASSIGN, expr, result=var))

  def make_io(self, operator):
    expr = self._operand_stack.pop()

    self._quads.push_quad(Quadruple(operator, expr))
  
  def make_jump(self, to_stack=False):
    if to_stack:
      to = self._jump_stack.pop()

      if to is None:
        raise GreaseError('Empty jump stack!')

      address = GreaseVar(GreaseType(GreaseTypeClass.Int), to, AddressingMethod.Literal)
      quad = Quadruple(Operation.JMP, result=address)
    else:
      self._jump_stack.push(self._quads.next_free_quad)
      quad = Quadruple(Operation.JMP)

    self._quads.push_quad(quad)
  
  def make_jump_f(self):
    self._jump_stack.push(self._quads.next_free_quad)
    cond = self._operand_stack.pop()

    if cond is None:
      self._quads.print_all()
      raise GreaseError('Empty jump stack!')

    quad = Quadruple(Operation.JMP_F, cond)    
    self._quads.push_quad(quad)

  def fill_jump(self, offset=0):
    quad_no = self._jump_stack.pop()

    if quad_no is not None:
      next_quad = self._quads.next_free_quad
      address = GreaseVar(GreaseType(GreaseTypeClass.Int), next_quad + offset, AddressingMethod.Literal)
      self._quads.fill_quad(quad_no, address)
    else:
      raise GreaseError('No jumps pending to be resolved')

  def make_call_main(self):
      self.push_jmp()
      self._quads.push_quad(Quadruple(Operation.ERA))
      self.push_jmp()
      self._quads.push_quad(Quadruple(Operation.GOSUB))
      self._quads.push_quad(Quadruple(Operation.HALT))


  def resolve_main(self):
    main = self.find_function('main')
    if main is None:
      raise UndefinedFunction('Main is not defined. No entry point for this program.')

    address = GreaseVar(GreaseType(GreaseTypeClass.Int), main.start, AddressingMethod.Literal)
    size = GreaseVar(GreaseType(GreaseTypeClass.Int), main.size, AddressingMethod.Literal)
    self._quads._quads[self._jump_stack.pop()].left_operand = address
    self._quads._quads[self._jump_stack.pop()].left_operand = size
    

  def print_stacks(self):
    """Print Stacks

    Prints the operand, operator and type stack
    """
    print("> Operand Stack = ")
    self._operand_stack.pprint()

    print("> Operator Stack = ")
    self._operator_stack.pprint()

    print("> Jump Stack = ")
    self._jump_stack.pprint()

  def reset_local_address(self, addr=0):
    self._next_local_address = addr

  def write_to_file(self, name):
    # Initial SP location
    # Remember that there are 4 adrresses per quad
    sp = (self._quads.next_free_quad * 4) + self._next_global_address + 1

    out_file = open(name, 'wb')
    out_file.write((200000).to_bytes(8, byteorder))
    out_file.write(sp.to_bytes(8, byteorder))
    self._quads.write_to_file(out_file)

  @staticmethod
  def basic_type_from_text(name):
    return GreaseType(type_class_dict.get(name))

  @staticmethod
  def operator_from_text(text):
    return operators_dict.get(text)

  @staticmethod
  def can_assign(l, r):
    def check_type(type_l, type_r):
      if type_l is None or type_r is None:
        return False

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
        return check_type(type_l.type_data, type_r.type_data)

      # All other type_classes may be assigned to themselves
      return type_l.type_class is type_r.type_class

    if l.method is AddressingMethod.Indirect:
      t1 = l.type.type_data
    else:
      t1 = l.type

    if r.method is AddressingMethod.Indirect:
      t2 = r.type.type_data
    else:
      t2 = r.type

    return check_type(t1, t2)

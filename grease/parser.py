import sys
import ply.yacc as yacc
from grease.scanner import tokens
from grease.greaser import Greaser
from grease.core.variable import GreaseVarBuilder
from grease.core.function import GreaseFnBuilder
from grease.core.struct import GreaseStructBuilder, GreaseStruct
from grease.core.interface import GreaseInterface
from grease.core.exceptions import GreaseError
from grease.core.quadruple import QuadrupleStore, Quadruple, Operation
from grease.core.stack import Stack
from grease.core.type import GreaseType, GreaseTypeClass
from grease.core.substruct import SubstrctBuilder

greaser = Greaser()

#Quads global structures
operator_stack = Stack()
operand_stack = Stack()
type_stack = Stack()
agregate_stack = Stack()

current_struct = None

next_global_address = 0
next_local_address = 0

quads = QuadrupleStore()

struct_builder = GreaseStructBuilder()
var_builder = GreaseVarBuilder()
fn_builder = GreaseFnBuilder()

precedence = (
  ('left', 'PLUS', 'MINUS'),
  ('left', 'TIMES', 'DIVIDE'),
  ('right', 'UMINUS'),
  ('left', 'DOT', 'ARROW')
)

def p_program(p):
  '''program : np_jump_to_main optional_imports optional_declarations main'''
  Quadruples.print_all()

def p_np_jump_to_main(p):
  '''np_jump_to_main : '''
  # Agregar primer cuadruplo salto a main
  Quadruples.jump_stack.push(Quadruples.next_free_quad)
  Greaser.build_and_push_quad(Operation.JMP, None, None, None)

# Permite tener 0 o mas import statements
# Left recursive
def p_optional_imports(p):
  '''optional_imports : optional_imports import
                      | empty'''
  pass

def p_import(p):
  '''import : IMPORT import_body'''

def p_import_body(p):
  '''import_body : import_decl NEW_LINE
                 | FROM ID NEW_LINE INDENT import_decl import_more_ids NEW_LINE DEDENT'''
  pass

def p_import_decl(p):
  '''import_decl : ID optional_import_as'''
  pass

def p_optional_import_as(p):
  '''optional_import_as : AS ID
                        | empty'''
  pass

def p_import_more_ids(p):
  '''import_more_ids : import_more_ids COMMA NEW_LINE import_decl
                     | empty'''
  pass

# Permite tener 0 o mas declaraciones
def p_optional_declarations(p):
  '''optional_declarations : optional_declarations declaration
                           | empty'''
  pass

def p_declaration(p):
  '''declaration : variable
                 | function
                 | alias
                 | struct
                 | interface'''
  pass

def p_variable(p):
  '''variable : VAR ID variable_body NEW_LINE'''
  try:
    var_builder.add_address(next_local_id)
    v = var_builder.build()
    greaser.add_variable(p[2], v)
    var_builder.reset()
  except GreaseError as e:
    e.print(p.lineno(2))
    raise
  
  var_builder.reset()


def p_variable_body(p):
  '''variable_body : COLON compound_type
                   | EQUALS expression'''
  if p[1] is ':':
    # Type assignment
    t = p[2]
  else:
    # Expession assignment
    # TODO: Enable when quadruples are ready
    #last_quad = Quadruples.quad_list[-1]
    #t = last_quad.result.type
    t = GreaseType(GreaseTypeClass.Int)

  var_builder.add_type(t)


def p_function(p):
  '''function : FN optional_method_declaration function_id OPEN_PAREN optional_params CLOSE_PAREN optional_return_type np_insert_function NEW_LINE block'''
  # Close the function scope
  greaser.close_scope()

def p_function_id(p):
  '''function_id : ID'''
  fn_builder.add_name(p[1])

def p_optional_method_declaration(p):
  '''optional_method_declaration : OPEN_PAREN ID COLON ID CLOSE_PAREN
                                 | empty'''
  if len(p) > 2:
    try:
      struct = greaser.find_struct(p[4])
      t = GreaseType(GreaseTypeClass.Struct, struct)
      var_builder.add_type(t)
      var = var_builder.build()
      var_builder.reset()
      
      fn_builder.add_param(p[2], var)
      fn_builder.add_struct(struct)
    except GreaseError as e:
      e.print(p.lineno(2))
      raise

def p_optional_params(p):
  '''optional_params : param more_params
                     | empty'''
  pass

def p_param(p):
  '''param : ID COLON basic_type'''
  try:
    var_builder.add_type(p[3])
    var = var_builder.build()
    var_builder.reset()
    fn_builder.add_param(p[1], var)
  except GreaseError as e:
    e.print(p.lineno(3))
    raise

def p_more_params(p):
  '''more_params : more_params COMMA param
                 | empty'''
  pass

def p_optional_return_type(p):
  '''optional_return_type : COLON basic_type
                          | empty'''
  if len(p) > 2:
    try:
      fn_builder.add_return_type(p[2])
    except GreaseError as e:
      e.print(p.lineno(2))
      raise

def p_np_insert_function(p):
  '''np_insert_function : '''
  try:
    name, struct, fn = fn_builder.build()
    fn_builder.reset()
    greaser.add_function(name, fn, struct)
    greaser.open_scope(fn.open_scope())
  except GreaseError as e:
    e.print(p.lineno(0))
    raise

def p_alias(p):
  '''alias : ALIAS compound_type AS ID NEW_LINE'''
  pass

def p_struct(p):
  '''struct : STRUCT struct_id optional_struct_interfaces NEW_LINE np_insert_struct INDENT struct_member more_struct_members DEDENT'''
    struct_builder.reset()

def p_struct_error(p):
  '''struct : STRUCT struct_id COLON error'''
  struct_builder.reset()

def p_struct_id(p):
  '''struct_id : ID'''
  struct_builder.add_name(p[1])

def p_optional_struct_interfaces(p):
  '''optional_struct_interfaces : COLON more_interfaces interface_id
                                | empty'''
  if len(p) > 2:
      vtable_t = greaser.find_struct('vtable')
      var_builder.add_type(GreaseType(GreaseTypeClass.Pointer, vtable_t))
      vtable = var_builder.build()
      struct_builder.add_member('vtable', vtable)

def p_interface_id(p):
  '''interface_id : ID'''
  try:
    interface = greaser.find_interface(p[1])
    struct_builder.add_interface(p[1], interface)
  except GreaseError as e:
    e.print(p.lineno(1))
    raise

def p_more_interfaces(p):
  '''more_interfaces : more_interfaces interface_id COMMA
                     | empty'''
  pass

def p_np_insert_struct(p):
  '''np_insert_struct : '''
  try:
    name, s = struct_builder.build()
    greaser.add_struct(name, s)
    global current_struct = s
  except GreaseError as e:
    e.print(p.lineno(2))
    raise

def p_struct_member(p):
  '''struct_member : ID COLON basic_type NEW_LINE'''
  try:
    var_builder.add_type(p[3])
    current_struct.add_variable(p[1], var_builder.build())
    var_builder.reset()
  except GreaseError as e:
    e.print(p.lineno(1))
    raise

def p_more_struct_members(p):
  '''more_struct_members : more_struct_members struct_member
                         | empty'''
  pass

def p_interface(p):
  '''interface : INTERFACE ID np_insert_interface NEW_LINE INDENT interface_function more_interface_functions DEDENT'''
  pass

def p_np_insert_interface(p):
  '''np_insert_interface : '''
  greaser.add_interface(p[-1], GreaseInterface())

def p_interface_error(p):
  '''interface : INTERFACE ID error'''
  pass

def p_interface_function(p):
  '''interface_function : FN ID OPEN_PAREN optional_interface_fn_params CLOSE_PAREN optional_return_type NEW_LINE'''
  pass

def p_optional_interface_fn_params(p):
  '''optional_interface_fn_params : interface_fn_param more_interface_fn_params
                                  | empty'''
  pass

def p_interface_fn_param(p):
  '''interface_fn_param : ID COLON basic_type'''
  pass

def p_more_interface_fn_params(p):
  '''more_interface_fn_params : more_interface_fn_params COMMA interface_fn_param
                              | empty'''
  pass

def p_more_interface_functions(p):
  '''more_interface_functions : more_interface_functions interface_function
                              | empty'''
  pass

def p_basic_type(p):
  '''basic_type : INT
                | FLOAT
                | CHAR
                | BOOL
                | pointer'''
  if isinstance(p[1], str):
    # p[1] is not a pointer
    p[0] = Greaser.basic_type_from_text(p[1])
  else:
    p[0] = p[1]

def p_compound_type(p):
  '''compound_type : ID
                   | array
                   | basic_type'''
  if isinstance(p[1], str):
    try:
      p[0] = greaser.find_type(p[1])
    except GreaseError as e:
      e.print(p.lineno(1))
      raise
  else:
    p[0] = p[1]

def p_pointer(p):
  '''pointer : compound_type TIMES'''
  p[0] = GreaseType(GreaseTypeClass.Pointer, p[1])

def p_array(p):
  '''array : OPEN_BRACK basic_type SEMICOLON CONST_INT array_more_dimens CLOSE_BRACK'''
  dimens = [p[4]] + p[5]
  p[0] = GreaseType(GreaseTypeClass.Array, p[2], dimens)
  #TODO: Signal as array

def p_array_more_dimens(p):
  '''array_more_dimens : array_more_dimens COMMA CONST_INT
                       | empty'''
  if len(p) > 2:
    p[0] = [p[3]] + p[1]
  else:
    p[0] = []

def p_block(p):
  '''block : INDENT block_body DEDENT'''
  pass

def p_block_body(p):
  '''block_body : block_body block_line
                | empty'''
  pass

def p_block_line(p):
  '''block_line : statement
                | variable'''
  pass

def p_statement(p):
  '''statement : statement_body'''
  pass

def p_statement_body(p):
  '''statement_body : assignment NEW_LINE
                    | print NEW_LINE
                    | scan NEW_LINE
                    | RETURN expression NEW_LINE
                    | fn_call NEW_LINE
                    | condition
                    | cycle'''
  pass

def p_assignment(p):
  '''assignment : sub_struct EQUALS expression'''
  try:
    var = greaser.find_variable(p[1])
  except GreaseError as e:
    e.print(p.lineno(1))
    raise

def p_condition(p):
  '''condition : IF expression COLON NEW_LINE block optional_else'''
  pass

def p_optional_else(p):
  '''optional_else : ELSE COLON NEW_LINE block
                   | empty'''
  pass

def p_cycle(p):
  '''cycle : WHILE expression COLON NEW_LINE block'''
  pass

def p_print(p):
  '''print : PRINT expression'''
  pass

def p_scan(p):
  '''scan : SCAN sub_struct'''

def p_expression(p):
  '''expression : logic_expr np_check_or optional_or'''
  pass

def p_np_check_or(p):
  '''np_check_or : '''
  # Revisar si hay un OR en el tope de la pila de operadores
  # if op_stack.isEmpty():
  #   pass
  # else :
  #   if op_stack.peek() == 'OR':
  #     l = []
  #     i = 1
  #     while i <= len(Operation):
  #       if Operation(i).value == Operation.AND.value or Operation(i).value == Operation.OR.value :
  #         l.append(Operation(i).value)
  #         i += 1
  #     greaser.exp_quad_helper(p, l,  operator_stack, type_stack, operand_stack)
  #     op_stack.pop()
  #   else :
  #     pass

def p_optional_or(p):
  '''optional_or : OR expression
                 | empty'''
  if len(p) > 2:
    quad = Quadruple()
    quad.operator = Operation.OR
    op_stack.push(quad)

def p_logic_expr(p):
  '''logic_expr : negation np_check_and optional_and'''
  if p[2] is None:
    p[0] = p[1]
  else:
    p[0] = p[2]

def p_np_check_and(p):
  '''np_check_and : '''
  # Revisar si hay un AND en el tope de la pila de operadores
  # if op_stack.isEmpty():
  #   pass
  # else :
  #   if op_stack.peek() == 'AND':
  #     l = []
  #     i = 1
  #     while i <= len(Operation):
  #       if Operation(i).value == Operation.AND.value or Operation(i).value == Operation.OR.value :
  #         l.append(Operation(i).value)
  #         i += 1
  #     greaser.exp_quad_helper(p, l,  operator_stack, type_stack, operand_stack)
  #     op_stack.pop()
  #   else :
  #     pass

def p_optional_and(p):
  '''optional_and : AND logic_expr
                  | empty'''
  if len(p) > 2:
    quad = Quadruple()
    quad.operator = Operation.AND
    op_stack.push(quad)

def p_negation(p):
  '''negation : np_check_negation optional_not rel_expr'''
  pass

def p_np_check_negation(p):
  '''np_check_negation : '''
  # Revisar si hay un NOT en el tope de la pila de operadores
  # if op_stack.isEmpty():
  #   pass
  # else :
  #   if op_stack.peek() == 'NOT':
  #     l = []
  #     i = 1
  #     while i <= len(Operation):
  #       if Operation(i).value == Operation.NOT.value:
  #         l.append(Operation(i).value)
  #         i += 1
  #     greaser.exp_quad_helper(p, l,  operator_stack, type_stack, operand_stack)
  #     op_stack.pop()
  #   else :
  #     pass

def p_optional_not(p):
  '''optional_not : NOT
                  | empty'''
  quad = Quadruple()
  quad.operator = Operation.NOT
  op_stack.push(quad)

def p_rel_expr(p):
  '''rel_expr : arith_expr np_check_comparison optional_comparison'''
  pass

def p_np_check_comparison(p):
  '''np_check_comparison : '''
  # Revisar si hay un Comparison operator en el tope de la pila de operadores
  # if op_stack.isEmpty():
  #   pass
  # else :
  #   l = []
  #   i = 1
  #   while i <= len(Operation):
  #     if Operation(i).value == Operation.value or Operation(i).value == Operation.value or :
  #       l.append(Operation(i).value)
  #       i += 1
  #   if op_stack.peek() in l:
  #     greaser.exp_quad_helper(p, l,  operator_stack, type_stack, operand_stack)
  #     op_stack.pop()

def p_optional_comparison(p):
  '''optional_comparison : optional_not comparison_operator rel_expr
                         | empty'''
  quad = Quadruple()
  quad.operator = Operation.GT
  op_stack.push(quad)

def p_comparison_operator(p):
  '''comparison_operator : EQ
                         | GT
                         | LT
                         | GE
                         | LE'''
  quad = Quadruple()
  quad.operator = Greaser.operator_from_text(p[1])
  op_stack.push(quad)

def p_arith_expr(p):
  '''arith_expr : term optional_arith_op'''
  pass

def p_optional_arith_op(p):
  '''optional_arith_op : PLUS arith_expr
                       | MINUS arith_expr
                       | empty'''
  quad = Quadruple()
  quad.operator = Greaser.operator_from_text(p[1])
  op_stack.push(quad)

def p_term(p):
  '''term : factor optional_mult_div'''
  pass

def p_optional_mult_div(p):
  '''optional_mult_div : TIMES term
                       | DIVIDE term
                       | empty'''
  quad = Quadruple()
  quad.operator = Greaser.operator_from_text(p[1])
  op_stack.push(quad)

def p_factor(p):
  '''factor : optional_sign value'''
  pass

def p_optional_sign(p):
  '''optional_sign : MINUS %prec UMINUS
                    | empty'''
  pass

def p_value(p):
  '''value : OPEN_PAREN expression CLOSE_PAREN
           | fn_call
           | const
           | sub_struct np_found_variable'''
  ########################################
  #operand_Stack.push(v.id)
  ########################################
  #type_Stack.push(v.type)

def p_np_found_variable(p):
  '''np_found_variable : '''
  pass

def p_fn_call(p):
  '''fn_call : sub_struct OPEN_PAREN optional_arguments CLOSE_PAREN'''
  try:
    greaser.find_function(p[1])
  except GreaseError as e:
    e.print(p.lineno(1))
    raise

def p_optional_arguments(p):
  '''optional_arguments : expression more_arguments
                        | empty'''
  pass

def p_more_arguments(p):
  '''more_arguments : more_arguments COMMA expression
                    | empty'''
  pass

def p_sub_struct(p):
  '''sub_struct : optional_pointer_op sub_struct_body more_sub_struct'''
  pass

def p_optional_pointer_op(p):
  '''optional_pointer_op : AMP
                         | TIMES
                         | empty'''
  if p[1] == '&':
    #TODO: Change addressing to literal 
    pass
  elif p[i] == '*':
    #TODO: Change adrressing to indirect
    pass

def p_sub_struct_body(p):
  '''sub_struct_body : ID np_found_id optional_sub_index'''
  p[0] = p[1]

def p_np_found_id(p):
  '''np_found_id : '''
  greaser.push_id(p[-1])

def p_optional_sub_index(p):
    '''optional_sub_index : OPEN_BRACK np_found_array expression more_sub_index CLOSE_BRACK
                          | empty'''
    pass

def p_np_found_array(p):
  '''np_found_array : '''
  pass
  #TODO: Move identifier into substruct stack

def p_more_sub_index(p):
  '''more_sub_index : more_sub_index COMMA np_next_sub_index expression
                    | empty'''
  pass

def p_np_next_sub_index(p):
  '''np_next_sub_index : '''
  #TODO: Calculate subindex address
  pass

def p_more_sub_struct(p):
  '''more_sub_struct : more_sub_struct sub_struct_operator sub_struct_body
                     | empty'''
  pass
  
def p_sub_struct_operator(p):
  '''sub_struct_operator : DOT
                         | ARROW'''
  #TODO: Move last id into substruct stack
  #TODO: Calculate new address
  pass

def p_main(p):
  '''main : FN MAIN np_main_fill_quad OPEN_PAREN CLOSE_PAREN COLON INT NEW_LINE block'''
  # greaser.build_and_push_quad(Operation.END, None, None, None)

def p_main_error(p):
  '''main : FN MAIN error'''
  # Consume parse error to continue reporting additional errors
  # Clear the list of quadruples. Nothing to compile.
  Quadruples.quad_list.clear()

def p_np_main_fill_quad(p):
  '''np_main_fill_quad : '''
  tmp_end = Quadruples.pop_jump()

  if tmp_end is not None:
    tmp_count = Quadruples.next_free_quad
    Quadruples.fill_missing_quad(tmp_end, tmp_count)

def p_const(p):
  '''const : CONST_INT
          | CONST_CHAR
          | CONST_STR
          | CONST_REAL
          | TRUE
          | FALSE'''
  p[0] = p[1]

def p_empty(p):
  'empty :'
  pass

def p_error(p):
  if p is None:
    print("Unexpected EOF")
  else:
    print("Unexpected {} at line {}".format(p.type, p.lexer.lineno))

grease_parser = yacc.yacc()

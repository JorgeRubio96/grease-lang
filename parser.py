import scanner
from greaser import Greaser
from variable import GreaseVarBuilder, GreaseVar
from function import GreaseFnBuilder
from struct import GreaseStructBuilder
from exceptions import GreaseError, TypeMismatch, UndefinedType, UndefinedVariable
from quadruple import *
from type import GreaseType, GreaseTypeClass

greaser = Greaser()

#Quads global structures
op_stack = Stack()
operand_Stack = Stack()
type_Stack = Stack()
#Temp QuadQueue
tmp_quad_stack = Stack()


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
  global var_builder
  try:
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
  global var_builder
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
  '''function : FN optional_method_declaration ID OPEN_PAREN optional_params CLOSE_PAREN optional_return_type NEW_LINE block'''
  global fn_builder
  try:
    fn = fn_builder.build()
    fn_builder.reset()
    greaser.add_function(p[3], fn, p[2])

  except GreaseError as e:
    e.print(p.lineno(2))
    raise

  #global_addr = operand_Stack.pop()
  #type_Stack.pop()
  #greaser.build_and_push_quad(Operation.EQ, global_addr, None, next_id)
  #operand_Stack.push(next_id)
  #type_Stack.push('function.type')

def p_optional_method_declaration(p):
  '''optional_method_declaration : OPEN_PAREN ID COLON struct_id CLOSE_PAREN
                                 | empty'''
  global var_builder, fn_builder
  if len(p) > 2:
    try:
      t = GreaseType(GreaseTypeClass.Struct, p[4])
      var_builder.add_type(t)
      var = var_builder.build()
      var_builder.reset()
      
      fn_builder.add_param(p[2], var)
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

def p_alias(p):
  '''alias : ALIAS compound_type AS ID NEW_LINE'''
  pass

def p_struct(p):
  '''struct : STRUCT ID optional_struct_interfaces NEW_LINE INDENT struct_member more_struct_members DEDENT'''
  global struct_builder
  try:
    s = struct_builder.build()
    greaser.add_struct(p[2], s)
    struct_builder.reset()
  except GreaseError as e:
    e.print(p.lineno(2))
    raise

# Maybe later: Multiple interfaces per struct
def p_optional_struct_interfaces(p):
  '''optional_struct_interfaces : COLON ID
                                | empty'''
  global struct_builder
  try:
    struct_builder.add_interface(p[2])
  except GreaseError as e:
    e.print(p.lineno(2))
    raise

def p_struct_member(p):
  '''struct_member : ID COLON basic_type NEW_LINE'''
  global struct_builder, var_builder
  try:
    var_builder.add_type(p[3])
    struct_builder.add_member(p[1], var_builder.build())
    var_builder.reset()
  except GreaseError as e:
    e.print(p.lineno(1))
    raise

def p_more_struct_members(p):
  '''more_struct_members : more_struct_members struct_member
                         | empty'''
  pass

def p_interface(p):
  '''interface : INTERFACE ID NEW_LINE INDENT interface_function more_interface_functions DEDENT'''
  pass

def p_interface_function(p):
  '''interface_function : FN ID OPEN_PAREN optional_params CLOSE_PAREN optional_return_type NEW_LINE'''
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
  '''compound_type : struct_id
                   | array
                   | basic_type'''
  if isinstance(p[1], str):
    p[0] = GreaseType(GreaseTypeClass.Struct, p[1])
  else:
    p[0] = p[1]

def p_pointer(p):
  '''pointer : compound_type TIMES'''
  p[0] = GreaseType(GreaseTypeClass.Pointer, p[1])
  #TODO: Signal as pointer

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

def p_struct_id(p):
  '''struct_id : ID'''
  try:
    greaser.find_struct(p[1])
  except GreaseError as e:
    e.print(p.lineno(1))
    raise
  
  p[0] = p[1]

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
  if p[2] is None:
    p[0] = p[1]
  else:
    p[0] = p[2]

def p_np_check_or(p):
  '''np_check_or : '''
  # Revisar si hay un OR en el tope de la pila de operadores

def p_optional_or(p):
  '''optional_or : OR expression
                 | empty'''
  if len(p) > 2:
    quad = Quadruple()
    quad.operator = Operation.OR
    op_stack.push(quad)

def p_logic_expr(p):
  '''logic_expr : negation optional_and'''
  if p[2] is None:
    p[0] = p[1]
  else:
    p[0] = p[2]

def p_optional_and(p):
  '''optional_and : AND logic_expr
                  | empty'''
  if len(p) > 2:
    quad = Quadruple()
    quad.operator = Operation.AND
    op_stack.push(quad)

def p_negation(p):
  '''negation : optional_not rel_expr'''
  quad = Quadruple()
  quad.operator = Operation.NOT
  op_stack.push(quad)

def p_optional_not(p):
  '''optional_not : NOT
                  | empty'''
  quad = Quadruple()
  quad.operator = Operation.U_MINUS
  op_stack.push(quad)

def p_rel_expr(p):
  '''rel_expr : arith_expr optional_comparison'''
  pass

def p_optional_comparison(p):
  '''optional_comparison : comparison_operator rel_expr
                         | empty'''
  pass

def p_comparison_operator(p):
  '''comparison_operator : EQ
                         | GT
                         | LT
                         | GE
                         | LE'''
  quad = Quadruple()
  quad.operator = Operation.GT
  op_stack.push(quad)

def p_arith_expr(p):
  '''arith_expr : term optional_arith_op'''
  pass

def p_optional_arith_op(p):
  '''optional_arith_op : PLUS arith_expr
                        | MINUS arith_expr
                        | empty'''
  quad = Quadruple()
  quad.operator = Operation.PLUS
  op_stack.push(quad)

def p_term(p):
  '''term : factor optional_mult_div'''
  pass

def p_optional_mult_div(p):
  '''optional_mult_div : TIMES term
                        | DIVIDE term
                        | empty'''
  quad = Quadruple()
  quad.operator = Operation.TIMES
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
  print('Found variable {} in expr line {}'.format(p[-1],p.lineno(-1)))

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
  p[0] = [p[2]] + p[3]

def p_optional_pointer_op(p):
  '''optional_pointer_op : AMP
                          | TIMES
                          | empty'''
  pass

def p_sub_struct_body(p):
    '''sub_struct_body : ID optional_sub_index'''
    p[0] = p[1]

def p_optional_sub_index(p):
    '''optional_sub_index : OPEN_BRACK expression more_arguments CLOSE_BRACK
                          | empty'''
    pass

def p_more_sub_struct(p):
  '''more_sub_struct : more_sub_struct sub_struct_operator sub_struct_body
                     | empty'''
  if len(p) == 4:
    p[0] = p[1] + [p[3]]
  else:
    p[0] = []

def p_sub_struct_operator(p):
  '''sub_struct_operator : DOT
                          | ARROW'''
  pass

def p_main(p):
  '''main : FN MAIN np_main_fill_quad OPEN_PAREN CLOSE_PAREN COLON INT NEW_LINE block'''
  # greaser.build_and_push_quad(Operation.END, None, None, None)

def p_np_main_fill_quad(p):
  '''np_main_fill_quad : '''
  tmp_end = Quadruples.pop_jump()
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
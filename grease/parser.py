import ply.yacc as yacc
import struct
from grease.scanner import tokens
from grease.greaser import Greaser
from grease.core.variable import GreaseVarBuilder
from grease.core.function import GreaseFnBuilder
from grease.core.struct import GreaseStructBuilder
from grease.core.interface import GreaseInterface
from grease.core.exceptions import GreaseError, UndefinedFunction
from grease.core.quadruple import Quadruple, Operation
from grease.core.type import GreaseType, GreaseTypeClass
from grease.core.dimension import GreaseDimension

greaser = Greaser()

#Quads global structures

struct_builder = GreaseStructBuilder()
var_builder = GreaseVarBuilder()
fn_builder = GreaseFnBuilder()
current_struct = None
declaration_assignment = False

precedence = (
  ('left', 'PLUS', 'MINUS'),
  ('left', 'TIMES', 'DIVIDE'),
  ('right', 'UMINUS'),
  ('left', 'DOT', 'ARROW')
)

def p_program(p):
  '''program : optional_imports optional_global_variables np_jump_to_main optional_declarations'''
  try:
    greaser.resolve_main()
  except GreaseError as e:
    e.print(p.lineno(4))
    raise

  # Debug print
  # TODO: Remove before release
  # greaser._quads.print_all()

def p_optional_global_variables(p):
  '''optional_global_variables : optional_global_variables variable
                               | empty'''
  pass

def p_np_jump_to_main(p):
  '''np_jump_to_main : '''
  # Agregar primer cuadruplo salto a main
  greaser.make_call_main()

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
  '''declaration : function
                 | alias
                 | struct
                 | interface'''
  pass

def p_variable(p):
  '''variable : VAR ID variable_body NEW_LINE'''
  global declaration_assignment

  try:
    v = var_builder.build()
    greaser.add_variable(p[2], v)

    if declaration_assignment:
      expr = greaser._operand_stack.pop()
      greaser.push_operand(v)
      greaser.push_operand(expr)
      greaser.make_assign()
      declaration_assignment = False
  except GreaseError as e:
    e.print(p.lineno(-1))
    raise

  var_builder.reset()

def p_variable_body(p):
  '''variable_body : COLON compound_type
                   | EQUALS expression'''
  if p[1] is ':':
    # Type is passed down by type
    var_builder.add_type(p[2])
  else:
    global declaration_assignment
    var_builder.add_type(greaser.top_operand_type())
    declaration_assignment = True


def p_function(p):
  '''function : FN optional_method_declaration function_id OPEN_PAREN optional_params CLOSE_PAREN optional_return_type np_insert_function NEW_LINE block'''
  # Close the function scope
  try:
    greaser.close_scope()
    greaser.push_fn_size()
    greaser.push_return(with_data=False)
  except GreaseError as e:
    e.print(1)
    raise

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
    e.print(p.lineno(1))
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
      e.print(p.lineno(1))
      raise

def p_np_insert_function(p):
  '''np_insert_function : '''
  try:
    name, struct, fn = fn_builder.build()
    greaser.add_function(name, fn, struct)
    fn_builder.reset()
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
  global current_struct
  
  try:
    name, s = struct_builder.build()
    greaser.add_struct(name, s)
    current_struct = s
  except GreaseError as e:
    e.print(p.lineno(0))
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
  '''interface : INTERFACE interface_name NEW_LINE INDENT interface_function more_interface_functions DEDENT'''
  pass

def p_interface_name(p):
  '''interface_name : ID'''
  try:
    greaser.add_interface(p[1], GreaseInterface())
  except GreaseError as e:
    e.print(p.lineno(0))
    raise

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
  dimens = [GreaseDimension(p[4])] + p[5]
  r = 1
  for dimen in dimens:
    r = r * dimen.size
  
  total_size = r

  for dimen in dimens:
    dimen.offset = int(r / dimen.size)
    r = dimen.offset
  
  p[0] = GreaseType(GreaseTypeClass.Array, p[2], dimens, total_size)

def p_array_more_dimens(p):
  '''array_more_dimens : array_more_dimens COMMA CONST_INT
                       | empty'''
  if len(p) > 2:
    p[0] = [GreaseDimension(p[3])] + p[1]
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
                    | RETURN expression np_push_return NEW_LINE
                    | fn_call NEW_LINE
                    | condition
                    | cycle'''
  pass

def p_np_push_return(p):
  '''np_push_return : '''
  greaser.push_return(with_data=True)

def p_assignment(p):
  '''assignment : sub_struct EQUALS expression'''
  try:
    greaser.make_assign()
  except GreaseError as e:
    e.print(p.lineno(2))
    raise

def p_condition(p):
  '''condition : IF expression np_condition COLON NEW_LINE block optional_else'''
  greaser.fill_jump()

def p_np_condition(p):
  '''np_condition : '''
  try:
    greaser.make_jump_f()
  except GreaseError as e:
    e.print(p.lineno(0))
    raise
  

def p_optional_else(p):
  '''optional_else : ELSE np_found_else COLON NEW_LINE block
                   | empty'''
  pass

def p_optional_else_error(p):
  '''optional_else : ELSE np_found_else COLON NEW_LINE error'''
  pass

def p_np_found_else(p):
  '''np_found_else : '''
  try:
    greaser.fill_jump(1)
    greaser.make_jump()
  except GreaseError as e:
    e.print(p.lineno(0))
    raise

def p_cycle(p):
  '''cycle : WHILE np_begin_cycle expression np_cycle COLON NEW_LINE block '''
  greaser.fill_jump(1)
  greaser.make_jump(to_stack=True)

def p_np_begin_cycle(p):
  '''np_begin_cycle : '''
  try:
    greaser.push_jmp()
  except GreaseError as e:
    e.print(p.lineno(0))
    raise

def p_np_cycle(p):
  '''np_cycle : '''
  try:
    greaser.make_jump_f()
  except GreaseError as e:
    e.print(p.lineno(0))
    raise

def p_print(p):
  '''print : PRINT expression'''
  try:
    greaser.make_io(Operation.PRINT)
  except GreaseError as e:
    e.print(p[0])

def p_scan(p):
  '''scan : SCAN sub_struct'''
  try:
    greaser.make_io(Operation.SCAN)
  except GreaseError as e:
    e.print(p[0])
    
def p_expression(p):
  '''expression : logic_expr np_check_or optional_or'''
  pass

def p_np_check_or(p):
  '''np_check_or : '''
  try:
    greaser.check_top_operator([Operation.OR])
  except GreaseError as e:
    e.print(p.lineno(0))

def p_optional_or(p):
  '''optional_or : or expression
                 | empty'''
  pass

def p_or(p):
  '''or : OR'''
  greaser.push_operator(Operation.OR)

def p_logic_expr(p):
  '''logic_expr : negation np_check_and optional_and'''
  if p[2] is None:
    p[0] = p[1]
  else:
    p[0] = p[2]

def p_np_check_and(p):
  '''np_check_and : '''
  try:
    greaser.check_top_operator([Operation.AND])
  except GreaseError as e:
    e.print(p.lineno(0))

def p_optional_and(p):
  '''optional_and : and logic_expr
                  | empty'''
  pass    

def p_and(p):
  '''and : AND'''
  greaser.push_operator(Operation.AND)

def p_negation(p):
  '''negation : np_check_negation optional_not rel_expr'''
  pass

def p_np_check_negation(p):
  '''np_check_negation : '''
  try:
    greaser.check_top_operator([Operation.NOT])
  except GreaseError as e:
    e.print(p.lineno(0))

def p_optional_not(p):
  '''optional_not : NOT
                  | empty'''
  if p[1] is not None:
    greaser.push_operator(Operation.NOT)

def p_rel_expr(p):
  '''rel_expr : arith_expr np_check_comparison np_check_direct_not optional_comparison '''
  pass

def p_optional_comparison(p):
  '''optional_comparison : optional_not comparison_operator rel_expr
                         | empty'''
  pass

def p_comparison_operator(p):
  '''comparison_operator : EQ
                         | GT
                         | LT
                         | GE
                         | LE'''
  greaser.push_operator(greaser.operator_from_text(p[1]))

def p_np_check_comparison(p):
  '''np_check_comparison : '''
  try:
    greaser.check_top_operator([Operation.EQ, Operation.GT, Operation.LT, Operation.GE, Operation.LE])
  except GreaseError as e:
    e.print(p.lineno(0))

def p_np_check_direct_not(p):
  '''np_check_direct_not : '''
  try:
    greaser.check_top_operator([Operation.NOT])
  except GreaseError as e:
    e.print(p.lineno(0))

def p_arith_expr(p):
  '''arith_expr : term np_check_arith_expr optional_arith_op'''
  pass

def p_optional_arith_op(p):
  '''optional_arith_op : arith_operator arith_expr
                       | empty'''
  pass

def p_arith_operator(p):
  '''arith_operator : PLUS
                    | MINUS'''
  operator = greaser.operator_from_text(p[1])
  greaser.push_operator(operator)

def p_np_check_arith_expr(p):
  '''np_check_arith_expr : '''
  try:
    greaser.check_top_operator([Operation.PLUS, Operation.MINUS])
  except GreaseError as e:
    e.print(p.lineno(0))
    raise

def p_term(p):
  '''term : factor np_check_term optional_mult_div'''
  pass

def p_optional_mult_div(p):
  '''optional_mult_div : mult_operator term
                       | empty'''
  pass

def p_mult_operator(p):
  '''mult_operator : TIMES
                   | DIVIDE'''
  greaser.push_operator(greaser.operator_from_text(p[1]))


def p_np_check_term(p):
  '''np_check_term : '''
  try:
    greaser.check_top_operator([Operation.TIMES, Operation.DIVIDE])
  except GreaseError as e:
    e.print(p.lineno(0))
    raise

def p_factor(p):
  '''factor : optional_sign value np_check_factor'''
  pass

def p_optional_sign(p):
  '''optional_sign : MINUS %prec UMINUS
                    | empty'''
  if p[1] is not None:
    greaser.push_operator(Operation.U_MINUS)

def p_np_check_factor(p):
  '''np_check_factor : '''
  try:
    greaser.check_top_operator([Operation.U_MINUS])
  except GreaseError as e:
    e.print(p.lineno(0))
    raise
  
def p_value(p):
  '''value : open_paren expression close_paren
           | optional_pointer_op fn_call
           | const
           | optional_pointer_op sub_struct'''
  pass

def p_open_paren(p):
  '''open_paren : OPEN_PAREN'''
  greaser.push_fake_bottom()

def p_close_paren(p):
  '''close_paren : CLOSE_PAREN'''
  greaser.pop_fake_bottom()

def p_fn_call(p):
  '''fn_call : fn_name OPEN_PAREN optional_arguments CLOSE_PAREN'''
  try:
    greaser.make_gosub()
  except GreaseError as e:
    e.print(p.lineno(2))
    raise

def p_fn_name(p):
  '''fn_name : ID'''
  try:
    print(p[1])
    greaser.make_fn(p[1])
  except GreaseError as e:
    e.print(p.lineno(0))
    raise

def p_optional_arguments(p):
  '''optional_arguments : expression np_make_param more_arguments
                        | empty'''
  pass

def p_more_arguments(p):
  '''more_arguments : more_arguments COMMA expression np_make_param
                    | empty'''
  pass

def p_np_make_param(p):
  '''np_make_param : '''
  try:
    greaser.make_param()
  except GreaseError as e:
    e.print(p.lineno(0))
    raise

def p_sub_struct(p):
  '''sub_struct : sub_struct_body more_sub_struct'''
  try:
    greaser.check_top_operator([Operation.ADDR, Operation.DEREF])
  except GreaseError as e:
    e.print(p.lineno(2))
    raise

def p_optional_pointer_op(p):
  '''optional_pointer_op : AMP
                         | TIMES
                         | empty'''
  if p[1] == '&':
    greaser.push_operator(Operation.ADDR)
    pass
  elif p[1] == '*':
    greaser.push_operand(Operation.DEREF)
    pass

def p_sub_struct_body(p):
  '''sub_struct_body : substruct_name optional_sub_index'''
  pass

def p_substruct_name(p):
  '''substruct_name : ID'''
  try:
    greaser.push_substruct(p[1])
  except GreaseError as e:
    e.print(p.lineno(0))
    raise

def p_optional_sub_index(p):
    '''optional_sub_index : OPEN_BRACK np_found_array expression np_dim_exp more_sub_index CLOSE_BRACK np_arr_add
                          | empty'''
    pass

def p_more_sub_index(p):
  '''more_sub_index : more_sub_index COMMA np_next_sub_index expression np_dim_exp
                    | empty'''
  pass

def p_np_found_array(p):
  '''np_found_array : '''
  try:
    greaser.push_agregate_stack() #verifies in the var table, and check is type array
  except GreaseError as e:
    e.print(p.lineno(0))
    raise

def p_np_dim_exp(p):
  '''np_dim_exp : '''
  try:
    greaser.push_dim_stack() #generates Quad
  except GreaseError as e:
    e.print(p.lineno(0))
    raise

def p_np_next_sub_index(p):
  '''np_next_sub_index : '''
  try:
    greaser.add_dim()  #generates Quad
  except GreaseError as e:
    e.print(p.lineno(0))
    raise

def p_np_arr_add(p):
  '''np_arr_add : '''
  try:
    greaser.set_arr_add()
  except GreaseError as e:
    e.print(p.lineno(0))
    raise


def p_more_sub_struct(p):
  '''more_sub_struct : more_sub_struct sub_struct_operator sub_struct_body
                     | empty'''
  pass
  
def p_sub_struct_operator(p):
  '''sub_struct_operator : DOT
                         | ARROW'''  
  if p[1] == '->':
    greaser.push_operator(Operation.DEREF)

  greaser.push_operator(Operation.ACCESS)  

def p_const(p):
  '''const : const_int
           | const_char
           | const_str
           | const_real
           | true
           | false'''
  pass

def p_const_int(p):
  '''const_int : CONST_INT'''
  val = p[1]

  # Store as 32bit unsigned 2's complement
  if val < 0:
    val += 1 << 32

  greaser.push_constant(val, GreaseType(GreaseTypeClass.Int))

def p_const_char(p):
  '''const_char : CONST_CHAR'''
  val = bytes(p[1], 'utf-8').decode('unicode_escape')
  greaser.push_constant(ord(val), GreaseType(GreaseTypeClass.Char))

def p_const_str(p):
  '''const_str : CONST_STR'''
  str_t = GreaseType(GreaseTypeClass.Array, GreaseType(GreaseTypeClass.Char))
  str_t.size = len(p[1]) + 1 # Don't forget null terminator!
  greaser.push_constant(p[1], str_t)

def p_const_real(p):
  '''const_real : CONST_REAL'''
  num = struct.pack('>f', p[1])
  rep = struct.unpack('>l', num)[0]
  greaser.push_constant(rep, GreaseType(GreaseTypeClass.Float))

def p_true(p):
  '''true : TRUE'''
  greaser.push_constant(True, GreaseType(GreaseTypeClass.Bool))

def p_false(p):
  '''false : FALSE'''
  greaser.push_constant(False, GreaseType(GreaseTypeClass.Bool))

def p_empty(p):
  'empty :'
  pass

def p_error(p):
  if p is None:
    print("Unexpected EOF")
  else:
    print("Unexpected {} at line {}".format(p.type, p.lexer.lineno))

grease_parser = yacc.yacc()

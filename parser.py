import ply.yacc as yacc
import scanner
import sys
from greaser import Greaser
from variable import GreaseType, GreaseVarBuilder, GreaserVar
from function import GreaseFnBuilder
from struct import GreaseStructBuilder
from exceptions import GreaseError, TypeMismatch
from quadruple import *

tokens = scanner.tokens
greaser = Greaser()

#Quadruples
operand_stack = Stack()
operator_stack = Stack()
type_stack = Stack()
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
########################################################
# Helper Functions
#Create quad
def build_and_push_quad(op, l_op, r_op, res):
  tmp_quad = Quadruple()
  tmp_quad.build(op, l_op, r_op, res)
  Quadruples.push_quad(tmp_quad)

#Exp quad helper
def exp_quad_helper(p, op_list):
  """Exp quad helper:
  Pops 2 operands from typestack and operand stack, checks type and calls build_and_push_quad"""
  if operator_stack.isEmpty():
    return
  op = operator_stack.peek()
  str_op = Operation.
  if str_op in op_list:
    t1 = type_stack.pop()
    t2 = type_stack.pop()
    return_type = SemanticCube.cube[op][t1][t2]
    if return_type == -1:
      raise TypeMismatch()
    o1 = operand_stack.pop()
    o2 = operand_stack.pop()
    tmp_var_id = SemanticInfo.get_next_var_id(return_type)

    # Generate Quadruple and push it to the list
    build_and_push_quad(op, o2, o1, tmp_var_id)
    operator_stack.pop()

    # push the tmp_var_id and the return type to stack
    operand_stack.push(tmp_var_id)
    type_stack.push(return_type)

    print "\n> PUSHING OPERATOR '{}' -> op2 = {}, op1 = {}, res = {}".format(str_op, o2, o1, tmp_var_id)
    print_stacks()

def assign_quad_helper(p):
  """Assign quadruple helper
  
  Helper to build the assign quadruple, pops 2 operands fromthe operand_stack and checks type
  
  Arguments:
    p {p} -- p
  """
  t1 = type_stack.pop()
  t2 = type_stack.pop()
  if t1 != t2:
    raise TypeMismatch()
  op = operator_stack.pop()
  o1 = operand_stack.pop()
  o2 = operand_stack.pop()
  print ">Second Opperand {}".format(o2)

  # Generate Quadruple and push it to the list

  if not tmp_array_index.isEmpty():
    print(">Temp array index {}".format(tmp_array_index.peek()))
    build_and_push_quad(op, o1, tmp_array_index.pop(), o2)
  else:
    build_and_push_quad(op, o1, None, o2)

def print_quad_helper():
  operand = operand_stack.pop()
  op = operator_stack.pop()
  build_and_push_quad(op, None, None, operand)
  type_stack.pop()

def push_const_operand_and_type(operand, type):
  """Push constant operand and type
  
  Builds the constant quadruple for operands and type
  
  Arguments:
    operand {operand} -- Operand
    type {int} -- Type
  """
  type_stack.push(type_dict[type])
  if operand in FunctionTable.constant_dict.keys():
    operand_stack.push(FunctionTable.constant_dict[operand])
    return
  addr = SemanticInfo.get_next_const_id()
  operand_stack.push(addr)
  FunctionTable.constant_dict[operand] = addr

def print_stacks():
  """Print Stacks
  
  Prints the operand, operator and type stack
  """
  sys.stdout.write("> Operand Stack = ")
  operand_stack.pprint()

  sys.stdout.write("> Operator Stack = ")
  operator_stack.pprint()

  sys.stdout.write("> Type Stack = ")
  type_stack.pprint()

########################################################
def p_program(p):
    '''program : optional_imports optional_declarations main'''
    pass

# Permite tener 0 o mas import statements
# Left recursive
def p_optional_imports(p):
    '''optional_imports : optional_imports import
                        | empty'''
    pass

def p_import(p):
    '''import : IMPORT import_body'''

def p_import_body(p):
    '''import_body : ID optional_import_as NEW_LINE
                   | FROM ID NEW_LINE INDENT ID import_more_ids NEW_LINE DEDENT'''
    pass

def p_optional_import_as(p):
    '''optional_import_as : AS ID
                          | empty'''
    pass

def p_import_more_ids(p):
    '''import_more_ids : import_more_ids COMMA ID NEW_LINE
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
    # addVariable(id, GreaseVar(type, data, address))
    greaser.add_variable(p[2], GreaseVar(GreaseType.Struct, p[3], 0))

def p_variable_body(p):
    '''variable_body : COLON compound_type
                     | EQUALS expression'''
    p[0] = p[2]

def p_function(p):
    '''function : FN optional_method_declaration ID OPEN_PAREN optional_params CLOSE_PAREN optional_return_type NEW_LINE block'''
    fn = fn_builder.build()
    fn_builder = GreaseFnBuilder()
    greaser.add_function(p[3], fn, p[2])

def p_optional_method_declaration(p):
    '''optional_method_declaration : OPEN_PAREN ID COLON struct_id CLOSE_PAREN
                                   | empty'''
    if len(p) > 2:
        p[0] = p[4]
        var_builder.add_type(GreaseType.Struct, p[4])
        var = var_builder.build()
        var_builder = GreaseVarBuilder()
        fn_builder.add_param(p[2], var)

def p_optional_params(p):
    '''optional_params : param more_params
                       | empty'''
    pass

def p_param(p):
    '''param : ID COLON basic_type'''
    var_builder.add_type(p[3])

def p_more_params(p):
    '''more_params : more_params COMMA param
                   | empty'''
    pass

def p_optional_return_type(p):
    '''optional_return_type : COLON basic_type
                            | empty'''
    pass

def p_alias(p):
    '''alias : ALIAS compound_type AS ID NEW_LINE'''
    pass

def p_struct(p):
    '''struct : STRUCT ID optional_struct_interfaces NEW_LINE INDENT struct_member more_struct_members DEDENT'''
    
    builder = GreaseStructBuilder()

# Maybe later: Multiple interfaces per struct
def p_optional_struct_interfaces(p):
    '''optional_struct_interfaces : COLON ID
                                  | empty'''
    struct_builder.add_interface(p[2])

def p_struct_member(p):
    '''struct_member : ID COLON basic_type NEW_LINE'''

    struct_builder.add_member(p[1], p[3])

def p_more_struct_members(p):
    '''more_struct_members : more_struct_members struct_member
                           | empty'''
    if len(p) > 2:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

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
    p[0] = GreaseType.from_text(p[1])

def p_compound_type(p):
    '''compound_type : struct_id
            | array
            | basic_type'''
    p[0] = p[1]

def p_pointer(p):
    '''pointer : compound_type TIMES'''
    p[0] = p[1]
    #TODO: Signal as pointer

def p_array(p):
    '''array : OPEN_BRACK basic_type SEMICOLON CONST_INT array_more_dimens CLOSE_BRACK'''
    p[0] = 2
    #TODO: Signal as array

def p_array_more_dimens(p):
    '''array_more_dimens : array_more_dimens COMMA CONST_INT
                         | empty'''
    pass

def p_struct_id(p):
    '''struct_id : ID'''
    struct = greaser.find_struct(p[1])
    if struct is None:
        #greaser.syntax_error('Undeclared stuct \"{}\" at line {}'.format(p[1], p.lineno(1)))
        pass
    
    p[0] = p[1]

def p_block(p):
    '''block : INDENT block_body DEDENT'''
    #'''block : INDENT open_scope block_body DEDENT close_scope'''
    pass

#def p_open_scope(p):
#    '''open_scope : '''
#    global greaser
#    greaser = greaser.open_scope()

#def p_close_scope(p):
#    '''close_scope : '''
#    global greaser
#    greaser = greaser.close_scope()

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
    pass

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
    '''expression : logic_expr optional_or'''
    if p[2] is None:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_optional_or(p):
    '''optional_or : OR expression
                   | empty'''
    if len(p) > 2:
        p[0] = greaser.eval(p[1], p[-1], p[2])

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
        p[0] = greaser.eval(p[1], p[-1], p[2])

def p_negation(p):
  '''negation : optional_not rel_expr'''
  pass

def p_optional_not(p):
  '''optional_not : NOT
                  | empty'''
  pass

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
  pass

def p_arith_expr(p):
  '''arith_expr : term optional_operation'''
  pass

def p_optional_operation(p):
  '''optional_operation : PLUS arith_expr
                        | MINUS arith_expr
                        | empty'''
  pass

def p_term(p):
    '''term : factor optional_mult_div'''
    pass

def p_optional_mult_div(p):
    '''optional_mult_div : TIMES term
                         | DIVIDE term
                         | empty'''
    pass

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
             | sub_struct'''
    #'''value : OPEN_PAREN expression CLOSE_PAREN
    #         | fn_call
    #         | const
    #         | sub_struct found_sub_struct'''
    pass

#def p_found_sub_struct(p):
#    '''found_sub_struct : '''
#    var = greaser.find_variables(p[-1])
#    if var is None:
#        greaser.syntax_error('Undefined variable {} at line {}'.format(p[-1], p.lineno(-1)))

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
    '''main : FN MAIN OPEN_PAREN CLOSE_PAREN COLON INT NEW_LINE block'''
    pass

def p_const(p):
    '''const : CONST_INT
            | CONST_CHAR
            | CONST_STR
            | CONST_REAL
            | TRUE
            | FALSE'''
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p is None:
        print("Unexpected EOF")
    else:
        print("Unexpected {} at line {}".format(p.type, p.lexer.lineno))

parser = yacc.yacc()


data = ''
for line in sys.stdin:
    data = data + line

result = yacc.parse(data,lexer=scanner.lexer, debug=False, tracking=True)
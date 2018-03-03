import ply.yacc as yacc
import scanner
import sys

tokens = scanner.tokens

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
    '''declaration : variable | function | alias | struct | interface'''
    pass

def p_variable(p):
    '''variable : VAR ID variable_body NEW_LINE'''
    pass

def p_variable_body(p):
    '''varibale_body : COLON compound_type
                     | EQUALS expression'''
    pass

def p_function(p):
    '''function : FN optional_method_declaration ID
                  OPEN_PAREN optional_params CLOSE_PAREN
                  optional_return_type NEW_LINE block'''
    pass

def p_optional_method_declaration(p):
    '''optional_method_declaration : OPEN_PAREN ID COLON struct_id CLOSE_PAREN
                                   | empty'''
    pass

def p_optional_params(p):
    '''optional_params : param more_params
                       | empty'''
    pass

def p_param(p):
    '''param: ID COLON basic_type'''
    pass

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
    '''struct : STRUCT ID optional_struct_interfaces NEW_LINE
                INDENT struct_member struct_more_members DEDENT'''
    pass

# Maybe later: Multiple interfaces per struct
def p_optional_struct_interfaces(p):
    '''optional_struct_interfaces : COLON ID
                                  | empty'''
    pass

def p_struct_member(p):
    '''struct_member : ID COLON basic_type NEW_LINE'''
    pass

def p_struct_more_members(p):
    '''struct_more_members : struct_more_members struct_member
                           | empty'''
    pass

def p_interface(p):
    '''interface : INTERFACE ID NEW_LINE INDENT interface_function DEDENT'''
    pass

def p_interface_function(p):
    '''interface_function : FN ID OPEN_PAREN optional_params CLOSE_PAREN'''
    pass
    
def p_basic_type(p):
    '''type : INT
            | FLOAT
            | CHAR
            | BOOL'''
    pass

def p_compound_type(p):
    '''type : STRUCT
            | ARRAY
            | POINTER'''
    pass

def p_block(p):
    '''block : INDENT block_body DEDENT'''
    pass

def p_block_body(p):
    '''block_body : block_body block_line NEW_LINE
                  | empty'''
    pass

def p_block_line(p):
    '''block_line : statement | variable'''
    pass

def p_statement(p):
    '''statement : assignment
                 | conditional
                 | printing'''
    pass

def p_assignment(p):
    '''assignment : ID EQUALS expression SEMICOLON'''
    pass

def p_conditional(p):
    '''conditional : IF OPEN_PAREN expression CLOSE_PAREN block optional_else SEMICOLON'''
    pass

def p_optional_else(p):
    '''optional_else : ELSE block
                     | empty'''
    pass

def p_printing(p):
    '''printing : PRINT OPEN_PAREN print_parameter CLOSE_PAREN SEMICOLON'''
    pass

def p_print_parameter(p):
    '''print_parameter : CONST_STRING print_more
                       | expression print_more'''
    pass

def p_print_more(p):
    '''print_more : COMMA print_parameter
                  | empty'''
    pass

def p_expression(p):
    '''expression : logic_expr
                  | expression OR logic_expr'''
    pass

def p_logic_expr(p):
  '''logic_expr : negation
                | logic_expr AND negation'''
  pass

def p_negation(p):
  '''negation : optional_not rel_expr'''
  pass

def p_optional_not(p):
  '''optional_not : NOT
                  | empty'''
  pass

def p_rel_expr(p):
  '''rel_expr : arith_expr optional_comparisson'''
  pass

def p_optional_comparisson(p):
  '''optional_comparisson : comparisson_operator arith_expr
                          | empty'''
  pass

def p_comparisson_operator(p):
  '''comparisson_operator : EQ
                          | GT
                          | LT
                          | GE
                          | LE'''
  pass

def p_arith_expr(p):
  '''arith_expr : term 
                |arith_expr optional_operation term'''
  pass

def p_optional_operation(p):
  '''optional_operation : PLUS
                        | MINUS'''
  pass

def p_value(p):
    '''value : term optional_add_sub'''
    pass

def p_optional_add_sub(p):
    '''optional_add_sub : PLUS value
                        | MINUS value
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
    '''optional_sign : MINUS
                     | empty'''
    pass

def p_number(p):
    '''number : CONST_INT
              | CONST_REAL
              | ID'''
    pass

def p_empty(p):
    'empty :'
    pass

def p_value(p):
    '''value : OPEN_PAREN expression CLOSE_PAREN
             | fn_call
             | const
             | optional_amp sub_struct'''
    pass


def p_optional_amp(p):
  '''optional_amp: AMP
                 | empty'''
  pass

def p_fn_call(p):
  '''fn_call: sub_struct optional_fn_call ID OPEN_PAREN optional_expression CLOSE_PAREN'''
  pass

def p_optional_fn_call(p):
  '''optional_fn_call: DOT
                     | MINUS ARROW_HEAD'''
  pass

def p_optional_expression(p):
  '''optional_expression: optional_expression_add
                        | empty'''
  pass

def p_optional_expression_add(p):
  '''optional_expression_add: optional_expression_add COMMA expression
                            | empty'''
  pass

def p_sub_struct(p):
  '''sub_struct: optional_pointer more_sub_structs'''
  pass
def p_optional_pointer(p):
  '''optional_pointer: TIMES
                     | empty'''
  pass

def p_more_sub_structs(p):
  '''more_sub_structs: more_subs_structs optional_fn_call ID OPEN_BRACK optional_expression_add CLOSE_BRACK'''
  pass

def p_main(p):
  '''main: MAIN OPEN_PAREN CLOSE_PAREN COLON INT NEW_LINE block'''
  pass

def p_const(p):
  '''const: CONST_INT
          | CONST_FLOAT
          | CONST_BOOL
          | CONST_CHAR
          | CONST_STR'''
  pass

def p_error(p):
    print("Syntax error at '%s'" % p.value)
    sys.exit()

parser = yacc.yacc()


data = ''
for line in sys.stdin:
    data = data + line


yacc.parse(data)
print('Parse success')
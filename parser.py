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
            | BOOL
            | pointer'''
    pass

def p_compound_type(p):
    '''type : struct_id
            | array
            | basic_type'''
    pass

def p_pointer(p):
    '''pointer : compound_type TIMES'''
    pass

def p_array(p):
    '''array : OPEN_BRACK basic_type SEMICOLON CONST_INT array_more_dimens CLOSE_BRACK'''
    pass

def p_array_more_dimens(p):
    '''array_more_dimens : array_more_dimens COMMA CONST_INT
                         | empty'''
    pass

def p_struct_id(p):
    '''struct_id : ID'''
    pass

def p_block(p):
    '''block : INDENT block_body DEDENT'''
    pass

def p_block_body(p):
    '''block_body : block_body block_line
                  | empty'''
    pass

def p_block_line(p):
    '''block_line : statement | variable'''
    pass

def p_statement(p):
    '''statement : statement_body NEW_LINE'''
    pass

def p_statement_body(p):
    '''statement_body : assignment
                      | condition
                      | print
                      | scan
                      | cycle
                      | RETURN expression
                      | fn_call'''
    pass

def p_assignment(p):
    '''assignment : sub_struct EQUALS expression'''
    pass

def p_condition(p):
    '''condition : IF expression COLON NEW_LINE block optional_else'''
    pass

def p_optional_else(p):
    '''optional_else : ELSE NEW_LINE block
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
    '''expression : value optional_comparison'''
    pass

def p_optional_comparison(p):
    '''optional_comparison : COMPARE value
                           | empty'''
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
    '''factor : OPEN_PAREN expression CLOSE_PAREN
              | optional_sign number'''
    pass

def p_optional_sign(p):
    '''optional_sign : PLUS
                     | MINUS
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

def p_error(p):
    print("Syntax error at '%s'" % p.value)
    sys.exit()

parser = yacc.yacc()


data = ''
for line in sys.stdin:
    data = data + line


yacc.parse(data)
print('Parse success')
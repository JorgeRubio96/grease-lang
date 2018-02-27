import ply.yacc as yacc
import scanner
import sys

tokens = scanner.tokens

def p_program(p):
  '''program : '''
  pass

def p_optional_variables(p):
    '''optional_variables : variables
                          | empty'''
    pass

def p_variables(p):
    '''variables : VAR ID more_id COLON type SEMICOLON more_variables'''
    pass

def p_more_id(p):
    '''more_id : COMMA ID more_id
               | empty'''
    pass

def p_more_variables(p):
    '''more_variables : ID more_id COLON type SEMICOLON more_variables
                      | empty'''
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
    '''block : OPEN_BLOCK inner CLOSE_BLOCK'''
    pass

def p_inner(p):
    '''inner : statement inner
             | empty'''
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
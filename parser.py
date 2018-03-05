import ply.yacc as yacc
import greaser
import scanner
import sys

tokens = scanner.tokens
greaser = greaser.Greaser()


precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
    ('left', 'DOT', 'ARROW')
)

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
    # addVariable(id, type)
    greaser.add_variable(p[2], p[3])

def p_variable_body(p):
    '''variable_body : COLON compound_type
                     | EQUALS expression'''
    p[0] = p[2]

def p_function(p):
    '''function : FN optional_method_declaration ID OPEN_PAREN optional_params CLOSE_PAREN optional_return_type NEW_LINE block'''
    print(p[3])

def p_optional_method_declaration(p):
    '''optional_method_declaration : OPEN_PAREN ID COLON struct_id CLOSE_PAREN
                                   | empty'''
    pass

def p_optional_params(p):
    '''optional_params : param more_params
                       | empty'''
    pass

def p_param(p):
    '''param : ID COLON basic_type'''
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
    '''struct : STRUCT ID optional_struct_interfaces NEW_LINE INDENT struct_member struct_more_members DEDENT'''
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
    pass

def p_compound_type(p):
    '''compound_type : struct_id found_struct
            | array
            | basic_type'''
    p[0] = p[1]

def p_pointer(p):
    '''pointer : compound_type TIMES'''
    pass

def p_found_struct(p):
    '''found_struct : '''
    if greaser.find_struct(p[-1]) is not None:
        p[0] = greaser.find_struct(p[-1])
    else:
        raise SyntaxError

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
    '''block : INDENT open_scope block_body DEDENT close_scope'''
    pass

def p_open_scope(p):
    '''open_scope : '''
    global greaser
    greaser = greaser.open_scope()

def p_close_scope(p):
    '''close_scope : '''
    global greaser
    greaser = greaser.close_scope()

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
    pass

def p_optional_or(p):
    '''optional_or : OR expression
                   | empty'''
    pass

def p_logic_expr(p):
    '''logic_expr : negation optional_and'''
    pass

def p_optional_and(p):
    '''optional_and : AND logic_expr
                    | empty'''

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
    pass

def p_fn_call(p):
    '''fn_call : sub_struct OPEN_PAREN optional_arguments CLOSE_PAREN'''
    pass

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
    pass

def p_sub_struct_body(p):
    '''sub_struct_body : ID optional_sub_index'''
    pass

def p_optional_sub_index(p):
    '''optional_sub_index : OPEN_BRACK expression more_arguments CLOSE_BRACK
                          | empty'''
    pass

def p_more_sub_struct(p):
    '''more_sub_struct : more_sub_struct sub_struct_operator sub_struct_body
                       | empty'''
    pass

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
    sys.exit()

parser = yacc.yacc()


data = ''
for line in sys.stdin:
    data = data + line


yacc.parse(data,lexer=scanner.lexer, debug=False)
print('Parse success')
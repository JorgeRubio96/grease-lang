import ply.yacc as yacc
import scanner
import sys
from greaser import Greaser
from variable import GreaseVarBuilder, GreaserVar
from function import GreaseFnBuilder
from struct import GreaseStructBuilder
from exceptions import GreaseError, TypeMismatch
from quadruple import *
from type import GreaseType, GreaseTypeClass

tokens = scanner.tokens
greaser = Greaser()

#Quads global structures
op_Stack = Stack()
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
    '''program : optional_imports optional_declarations main'''
    Quadruples.print_all()

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
    global var_builder
    v = var_builder.build()
    greaser.add_variable(p[2], v)
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
        last_quad = Quadruples.quad_list[-1]
        t = last_quad.result.type

    var_builder.add_type(t)


def p_function(p):
    '''function : FN optional_method_declaration ID OPEN_PAREN optional_params CLOSE_PAREN optional_return_type NEW_LINE block'''
    global fn_builder
    fn = fn_builder.build()
    fn_builder.reset()
    greaser.add_function(p[3], fn, p[2])



def p_optional_method_declaration(p):
    '''optional_method_declaration : OPEN_PAREN ID COLON struct_id CLOSE_PAREN
                                   | empty'''
    global var_builder, fn_builder
    if len(p) > 2:
        var_builder.add_type(p[4])
        var = var_builder.build()
        var_builder.reset()
        
        fn_builder.add_param(p[2], var)

def p_optional_params(p):
    '''optional_params : param more_params
                       | empty'''
    pass

def p_param(p):
    '''param : ID COLON basic_type'''
    global var_builder
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
    global struct_builder
    s = struct_builder.build()
    greaser.add_struct(p[2], s)
    struct_builder.reset()

# Maybe later: Multiple interfaces per struct
def p_optional_struct_interfaces(p):
    '''optional_struct_interfaces : COLON ID
                                  | empty'''
    global struct_builder
    struct_builder.add_interface(p[2])

def p_struct_member(p):
    '''struct_member : ID COLON basic_type NEW_LINE'''
    global struct_builder
    try:
        struct_builder.add_member(p[1], p[3])
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
        t = Greaser.basic_type_from_text(p[1])
        p[0] = GreaseType(t)
    else:
        p[0] = p[1]

def p_compound_type(p):
    '''compound_type : struct_id
            | array
            | basic_type'''
    if isinstance(p[1], str):

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
    p[0] = greaser.find_struct(p[1])

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
        op_Stack.push_op(p[1])

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
        op_Stack.push_op(p[1])

def p_negation(p):
  '''negation : optional_not rel_expr'''
  pass

def p_optional_not(p):
  '''optional_not : NOT
                  | empty'''
  op_Stack.push_op(p[1])

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
  op_Stack.push_op(p[1])

def p_arith_expr(p):
  '''arith_expr : term optional_operation'''
  pass

def p_optional_operation(p):
  '''optional_operation : PLUS arith_expr
                        | MINUS arith_expr
                        | empty'''
  op_Stack.push_op(p[1])

def p_term(p):
    '''term : factor optional_mult_div'''
    pass

def p_optional_mult_div(p):
    '''optional_mult_div : TIMES term
                         | DIVIDE term
                         | empty'''
    op_Stack.push_op(p[1])

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
    build_and_push_quad(operators_dict['end'], None, None, None)

def p_main_fill_quad(p):
  '''main_fill_quad : '''
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
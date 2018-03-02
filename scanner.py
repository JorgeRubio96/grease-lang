import ply.lex as lex
import sys

stack_indentLevels = [0];

reserved = {
'var': 'VAR',
'float': 'FLOAT',
'print': 'PRINT',
'if': 'IF',
'else': 'ELSE',
'scan': 'SCAN',
'print': 'PRINT',
'and': 'AND',
'or': 'OR',
'Boolean': 'BOOLEAN',
'Int': 'INT',
'Float': 'FLOAT',
'Char': 'CHAR',
'true': 'TRUE',
'false': 'FALSE',
'fn': 'FUNCTION',
'interface': 'INTERFACE',
'import': 'IMPORT',
'struct':'STRUCT',
'while':'WHILE',
'for':'FOR',
'alias':'ALIAS',
'as':'AS',
'gt': 'GT',
'ge': 'GE',
'lt': 'LT',
'le': 'LE',
'gt': 'GT',
'eq': 'EQ',
'not':'NOT',
'from': 'FROM'
}

tokens = [
    'ID', 'CONST_INT', 'CONST_FLOAT', 'CONST_STR', 'CONST_CHAR','ARROW_HEAD', 
    'SEMICOLON', 'COLON', 'COMMA',
    'OPEN_BLOCK', 'CLOSE_BLOCK', 'EQUALS',
    'OPEN_PAREN', 'CLOSE_PAREN', 'PLUS', 'MINUS',
    'TIMES', 'DIVIDE', 'AMP'
    ] + list(reserved.values())


t_ignore = '\t\n '

t_SEMICOLON = r'\;'
t_COLON = r'\:'
t_COMMA = r'\,'
t_OPEN_BLOCK = r'\{'
t_CLOSE_BLOCK = r'\}'
t_EQUALS = r'\='
t_OPEN_PAREN = r'\('
t_CLOSE_PAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_AMP = r'\&'
t_ARROW_HEAD = r'\>'

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_CONST_INT(t):
    r'[1-9][0-9]*'
    t.value = int(t.value)
    return t

def t_CONST_FLOAT(t):
    r'[0-9]+"."[0-9]+'
    t.value = float(t.value)
    return t

def t_CONST_STR(t):
    r'\"[a-zA-Z ]+\"'
    t.value = t.value[1:-1]
    return t

def t_CONST_CHAR(t):
    r'\'[a-zA-Z ]\''
    t.value = t.value[1:-1]
    return t
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    sys.exit()


lexer = lex.lex()
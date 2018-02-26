import ply.lex as lex
import sys

reserved = {
'program': 'PROGRAM',
'var': 'VAR',
'int': 'INT',
'float': 'FLOAT',
'print': 'PRINT',
'if': 'IF',
'else': 'ELSE',
}

tokens = [
    'ID', 'CONST_INT', 'CONST_REAL', 'CONST_STRING',
    'COMPARE', 'SEMICOLON', 'COLON', 'COMMA',
    'OPEN_BLOCK', 'CLOSE_BLOCK', 'EQUALS',
    'OPEN_PAREN', 'CLOSE_PAREN', 'PLUS', 'MINUS',
    'TIMES', 'DIVIDE'
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
t_COMPARE = r'(\<\>)|[\<\>]'

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_CONST_INT(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_CONST_REAL(t):
    r'[0-9]+"."[0-9]+'
    t.value = float(t.value)
    return t

def t_CONST_STRING(t):
    r'\"[a-zA-Z ]+\"'
    t.value = t.value[1:-1]
    return t
    

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    sys.exit()


lexer = lex.lex()
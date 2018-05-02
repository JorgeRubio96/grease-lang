import ply.lex as lex
from grease.core.indents import Indents

reserved = {
    'var': 'VAR',
    'if': 'IF',
    'else': 'ELSE',
    'scan': 'SCAN',
    'print': 'PRINT',
    'and': 'AND',
    'or': 'OR',
    'Bool': 'BOOL',
    'Int': 'INT',
    'Float': 'FLOAT',
    'Char': 'CHAR',
    'fn': 'FN',
    'interface': 'INTERFACE',
    'import': 'IMPORT',
    'struct':'STRUCT',
    'while':'WHILE',
    'alias':'ALIAS',
    'as':'AS',
    'gt': 'GT',
    'ge': 'GE',
    'lt': 'LT',
    'le': 'LE',
    'eq': 'EQ',
    'not':'NOT',
    'from': 'FROM',
    'return': 'RETURN',
    'true': 'TRUE',
    'false': 'FALSE'
}

tokens = [
    'ID', 'CONST_INT', 'CONST_REAL', 'CONST_STR', 'CONST_CHAR',
    'ARROW', 'SEMICOLON', 'COLON', 'COMMA', 'DOT', 'EQUALS', 'NEW_LINE',
    'OPEN_BRACK','CLOSE_BRACK', 'OPEN_PAREN', 'CLOSE_PAREN', 'PLUS', 'MINUS',
    'TIMES', 'DIVIDE', 'AMP', 'INDENT', 'DEDENT'
    ] + list(reserved.values())

t_DOT = r'\.'
t_SEMICOLON = r'\;'
t_COLON = r'\:'
t_COMMA = r'\,'
t_OPEN_BRACK = r'\['
t_CLOSE_BRACK = r'\]'
t_EQUALS = r'\='
t_OPEN_PAREN = r'\('
t_CLOSE_PAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_AMP = r'\&'
t_ARROW = r'\-\>'
t_ignore = ' '

def t_ignore_SINGLE_COMMENT(t):
    r'\#.*\n'
    t.lexer.lineno += 1

def t_ignore_MULTI_COMMENT(t):
    r'\/\*[\s\S]*\*\/\s*'
    t.lexer.lineno += t.value.count('\n')

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_\-]*'
    t.type = reserved.get(t.value, 'ID')

    if t.type == 'CONST_BOOL':
        if t.value == 'true':
            t.value = True
        else:
            t.value = False

    return t

def t_CONST_REAL(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_CONST_INT(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_CONST_STR(t):
    r'\".+\"'
    t.value = t.value[1:-1]
    return t

def t_CONST_CHAR(t):
    r'\'.+\''
    t.value = t.value[1:-1]
    return t

def t_NEW_LINE(t):
    r'\n\s*[\t ]*'
    t.lexer.lineno += t.value.count('\n')
    t.value = len(t.value) - 1 - t.value.rfind('\n')
    return t

def first_word(s):
    whites = [' ', '\t', '\n']
    low = 0
    for l in s:
        if l in whites:
            break
        low += 1

    return s[0:low]

def t_error(t):
    print("Unexpected \"{}\" at line {}".format(first_word(t.value), t.lexer.lineno))

grease_lexer = Indents(lex.lex())

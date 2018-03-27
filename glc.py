import sys
import ply.lex as lex
import ply.yacc as yacc
from indents import Indents
from scanner import *
from parser import *



def main():
    lexer = Indents(lex.lex())
    parser = yacc.yacc()
    data = ''

    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as src_file:
            data = src_file.read()
    else:
        for line in sys.stdin:
            data = data + line

    result = parser.parse(data,lexer=lexer, debug=False, tracking=True)

if __name__ == '__main__':
    main()
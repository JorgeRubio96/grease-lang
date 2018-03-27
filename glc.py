import sys
from scanner import grease_lexer
from parser import grease_parser



def main():
    data = ''

    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as src_file:
            data = src_file.read()
    else:
        for line in sys.stdin:
            data = data + line

    result = grease_parser.parse(data,lexer=grease_lexer, debug=False, tracking=True)

if __name__ == '__main__':
    main()
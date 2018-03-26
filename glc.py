import sys
import scanner
import parser


def main():
    data = ''

    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as src_file:
            data = src_file.read()
    else:
        for line in sys.stdin:
            data = data + line

    result = parser.parser.parse(data,lexer=scanner.lexer, debug=False, tracking=True)

if __name__ == '__main__':
    main()
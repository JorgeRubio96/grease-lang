import sys
from grease.scanner import grease_lexer
from grease.parser import grease_parser, greaser


def _main():
    data = ''

    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as src_file:
            data = src_file.read()
    else:
        for line in sys.stdin:
            data = data + line

    compile(data)

def compile(data):
    result = grease_parser.parse(data,lexer=grease_lexer, debug=False, tracking=True)
    greaser.write_to_file('out.gbc')

if __name__ == '__main__':
    _main()

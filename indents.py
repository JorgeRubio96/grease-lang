import sys
from collections import namedtuple

IndentToken = namedtuple('IndentToken', 'type value lexer')

class Indents(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.indent_stack = [0]
        self.token_queue = []
        self.eof = False

    @property
    def input(self):
        return self.lexer.input

    @input.setter
    def input(self, value):
        self.lexer.input = value

    def token(self):
        if len(self.token_queue) > 0:
            token = self.token_queue[-1]
            self.token_queue = self.token_queue[0:-1]
            return token

        if self.eof:
            return None

        token = self.lexer.token()

        if token is None:
            self.eof = True

            if len(self.indent_stack) > 1:
                token = IndentToken('NEW_LINE', None, self.lexer)
                self.token_queue.append(IndentToken('DEDENT', None, self.lexer))

                for _ in range(len(self.indent_stack) - 2):
                    self.token_queue.append(IndentToken('NEW_LINE', None, self.lexer))
                    self.token_queue.append(IndentToken('DEDENT', None, self.lexer))


                self.indent_stack=[0]

        elif token.type == 'NEW_LINE':

            if token.value > self.indent_stack[-1]:
                self.indent_stack.append(token.value)
                self.token_queue.append(IndentToken('INDENT', None, self.lexer))

            else:

                while token.value < self.indent_stack[-1]:
                    self.indent_stack = self.indent_stack[0:-1]
                    self.token_queue.append(IndentToken('DEDENT', None, self.lexer))

                if token.value != self.indent_stack[-1]:
                    print("Indent Error")
                    sys.exit()
        
        return token

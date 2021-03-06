import sys

class GreaseError(SyntaxError):
    def __init__(self, msg):
        self.msg = msg
        self.err_name = 'Syntax error'

    def print(self, lineno):
        print(self.err_name + ' at line {}: '.format(lineno) + self.msg, file=sys.stderr)

class UndefinedVariable(GreaseError):
    def __init__(self, msg):
        self.msg = msg
        self.err_name = 'Undefined variable'

class UndefinedFunction(GreaseError):
    def __init__(self, msg):
        self.msg = msg
        self.err_name = 'Undefined function'

class UndefinedStruct(GreaseError):
    def __init__(self, msg):
        self.msg = msg
        self.err_name = 'Undefined struct'

class UndefinedType(GreaseError):
    def __init__(self, msg):
        self.msg = msg
        self.err_name = 'Undefined type'

class UndefinedMember(GreaseError):
    def __init__(self, msg):
        self.msg = msg
        self.err_name = 'Undefined member'

class UndefinedInterface(GreaseError):
    def __init__(self, msg):
        self.msg = msg
        self.err_name = 'Undefined interface'

class TypeMismatch(GreaseError):
    def __init__(self, msg):
        self.msg = msg
        self.err_name = 'Type mismatch'

class VariableRedefinition(GreaseError):
    def __init__(self, msg):
        self.msg = msg
        self.err_name = 'Variable redefinition'

class StructRedefinition(GreaseError):
    def __init__(self, msg):
        self.msg = msg
        self.err_name = 'Struct redefinition'

class FunctionRedefinition(GreaseError):
    def __init__(self, msg):
        self.msg = msg
        self.err_name = 'Method redefinition'

class DuplicateInterface(GreaseError):
    def __init__(self, msg):
        self.msg = msg
        self.err_name = 'Duplicate interface'

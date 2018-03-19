class GreaseError(SyntaxError):
    def __init__(self, msg):
        self.msg = msg
        self.err_name = 'Syntax error'

    def print(self, lineno):
        print(self.err_name + ' at line {}: '.format(lineno) + self.msg)

class UndefinedVariable(GreaseError):
    def __init__(self, msg):
        self.msg = msg
        self.err_name = 'Undefined variable'

class UndefinedFunction(GreaseError):
    pass

class UndefinedType(GreaseError):
    pass

class UndefinedMember(GreaseError):
    pass

class TypeMismatch(GreaseError):
    def __init__(self, msg):
        self.msg = msg
        self.err_name = 'Type mismatch'

class VariableRedefiniton(GreaseError):
    pass

class StructRedfinition(GreaseError):
    pass

class MethodRedefinition(GreaseError):
    pass
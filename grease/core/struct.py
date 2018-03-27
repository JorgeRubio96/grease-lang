from grease.core.variable_table import VariableTable
from grease.core.function_directory import FunctionDirectory
from grease.core.exceptions import VariableRedefinition, MethodRedefinition

class GreaseStruct:
    def __init__(self, variables={}, interface=None, functions={}):
        self.variables = VariableTable()
        self.functions = FunctionDirectory()
        self.interface = interface

        for name, varable in variables.items():
            self.variables.add_variable(name, varable)

        for name, fn in functions.items():
            self.functions.add_function(name, fn)


class GreaseStructBuilder:
    def __init__(self):
        self._variables = {}
        self._functions = {}
        self._interface = None

    def add_member(self, name, member):
        if name in self._variables:
            raise VariableRedefiniton(name)
        
        self._variables[name] = member

    def add_function(self, name, fn):
        if name in self._functions:
            raise MethodRedefinition(name)

        self._functions[name] = fn

    def add_interface(self, interface):
        self._interface = interface

    def build(self):
        return GreaseStruct(self._variables, self._interface, self._functions)

    def reset(self):
        self._variables = {}
        self._functions = {}
        self._interface = None
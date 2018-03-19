from variable_table import VariableTable
from function_directory import FunctionDirectory

class GreaseStruct:
    def __init__(self, variables=[], interface=None, functions=[]):
        self.variables = VariableTable()
        self.functions = FunctionDirectory()
        self.interface = interface

        for varable in variables:
            self.variables.add_variable(varable)

        for fn in functions:
            self.functions.add_function(fn)


class GreaseStructBuilder:
    def __init__(self):
        self._variables = []
        self._functions = []
        self._interface = None

    def add_member(self, member):
        self._variables.append(member)

    def add_function(self, variable):
        self._functions.append(variable)

    def add_interface(self, interface):
        self._interface = interface

    def build(self):
        return GreaseStruct(self._variables, self._interface, self._functions)
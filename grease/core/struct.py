from grease.core.variable_table import VariableTable
from grease.core.function_directory import FunctionDirectory
from grease.core.interface_table import InterfaceTable
from grease.core.exceptions import VariableRedefinition, FunctionRedefinition, DuplicateInterface

class GreaseStruct:
    def __init__(self, variables={}, interfaces={}, functions={}):
        self.variables = VariableTable()
        self.functions = FunctionDirectory()
        self.interfaces = InterfaceTable()
        self.total_size = 0
        self.next_addr = 0
        
        for name, variable in variables.items():
            variable.address = self.next_addr
            self.variables.add_variable(name, variable)
            self.next_addr += 1

        for name, fn in functions.items():
            self.functions.add_function(name, fn)

        for name, interface in interfaces.items():
            self.interfaces.add_interface(name, interface)

    def add_variable(self, name, var):
        var.address = self.next_addr
        self.variables.add_variable(name, var)
        self.next_addr += 1

    def has_interface(self, interface):
        return interface in self.interfaces._interfaces.values()

class GreaseStructBuilder:
    def __init__(self):
        self._variables = {}
        self._functions = {}
        self._interfaces = {}
        self._name = ''

    def add_member(self, name, member):
        if name in self._variables:
            raise VariableRedefinition(name)
        
        self._variables[name] = member

    def add_function(self, name, fn):
        if name in self._functions:
            raise FunctionRedefinition(name)

        self._functions[name] = fn

    def add_interface(self, name, interface):
        if name in self._interfaces:
            raise DuplicateInterface(name)

        self._interfaces[name] = interface
    
    def add_name(self, name):
        self._name = name

    def build(self):
        return self._name, GreaseStruct(self._variables, self._interfaces, self._functions)

    def reset(self):
        self._variables = {}
        self._functions = {}
        self._interfaces = {}

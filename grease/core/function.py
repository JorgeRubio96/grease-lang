from grease.core.variable_table import VariableTable
from grease.core.exceptions import VariableRedefinition

class GreaseFn:
    def __init__(self, params, return_type, return_data=None):
        self.params = params
        self.return_type = return_type
        self.return_data = return_data
        self._variables = None
        self.size = 0
        self.start = 0

    def open_scope(self, global_vars=None):
        self._variables = VariableTable(global_vars)
        
        for name, param in self.params.items():
            self._variables.add_variable(name, param)

        return self._variables

    def close_scope(self):
        parent = self._variables.parent
        self._variables = None
        return parent

class GreaseFnBuilder:
    def __init__(self):
        self._params = {}
        self._return_type = None
        self._return_data = None
        self._name = None
        self._struct = None

    def add_param(self, param_name, param):
        if param_name in self._params:
            raise VariableRedefinition('{}'.format(param_name))
        self._params[param_name] = param

    def add_return_type(self, return_type, return_data=None):
        self._return_type = return_type
        self._return_data = return_data

    def add_name(self, name):
        self._name = name

    def add_struct(self, struct):
        self._struct = struct

    def build(self):
        return self._name, self._struct, GreaseFn(self._params, self._return_type, self._return_data)

    def reset(self):
        self._params = {}
        self._return_type = None
        self._return_data = None

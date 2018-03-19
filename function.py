from variable_table import VariableTable
from exceptions import VariableRedefinition

class GreaseFn:
    def __init__(self, params, return_type, return_data=None):
        self.params = params
        self.return_type = return_type
        self.return_data = return_data
        self._variables = None

    def open_scope(self, global_vars):
        self._variables = VariableTable(global_vars)
        
        for id, param in self.params.items():
            self._variables.add_variable(id, param)

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

    def add_param(self, param_name, param):
        if param_name in self._params:
            raise VariableRedefiniton('{}'.format(param_name))
        self._params[id] = param

    def add_return_type(self, return_type, return_data=None):
        self._return_type = return_type
        self._return_data = return_data

    def build(self):
        return GreaseFn(self._params, self._return_type, self._return_data)

    def reset(self):
        self._params = {}
        self._return_type = None
        self._return_data = None
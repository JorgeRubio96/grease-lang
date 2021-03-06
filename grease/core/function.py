from grease.core.variable_table import VariableTable
from grease.core.exceptions import VariableRedefinition
from grease.core.variable import AddressingMethod

class GreaseFn:
  def __init__(self, params, return_type, param_types=[], size=0, start=0):
    self.params = params
    self.return_type = return_type
    self._variables = None
    self.param_types = param_types
    self.size = size
    self.start = start

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
    self._name = None
    self._struct = None
    self._param_types = []

  def add_param(self, param_name, param):
    if param_name in self._params:
      raise VariableRedefinition('{}'.format(param_name))
    self._params[param_name] = param
    
    param.method = AddressingMethod.Relative
    param._address = len(self._param_types) + 2

    self._param_types.append(param.type)

  def add_return_type(self, return_type):
    self._return_type = return_type

  def add_name(self, name):
    self._name = name

  def add_struct(self, struct):
    self._struct = struct

  def build(self):
    return self._name, self._struct, GreaseFn(self._params, self._return_type, self._param_types)

  def reset(self):
    self._params = {}
    self._return_type = None
    self._name = None
    self._struct = None
    self._param_types = []
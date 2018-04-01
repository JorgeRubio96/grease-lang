class InterfaceTable:
  def __init__(self):
    self._interfaces = {}

  def add_interface(self, name, interface):
    if name not in self._interfaces:
      self._interfaces[name] = interface
      return True
    return False

  def find_interface(self, name):
    return self._interfaces.get(name)
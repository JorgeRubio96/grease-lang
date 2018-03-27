class VariableTable:
    def __init__(self, parent=None):
        self.parent = parent
        self._variables = {}

    def find_variable(self, id):
        if self.parent is None:
            return self._variables.get(id)
        return self._variables.get(id, self.parent.find_variable(id))

    def add_variable(self, id, var):
        if id not in self._variables:
            self._variables[id] = var
            return True
        return False
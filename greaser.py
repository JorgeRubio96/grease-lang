class Greaser:
    def __init__(self, parent=None):
        self._parent = parent
        self._variables = {}
        
        if parent is None:
            self._functions = {}
            self._structs = {}

    def find_function(self, id):
        if self._parent is None:
            return self._functions.get(id, None)
        return self._parent.find_function(id)
    
    def find_variables(self, id):
        if self._parent is None:
            return self._variables.get(id, None)
        return self._variables.get(id, self._parent.find_variables(id))

    def find_struct(self, id):
        if self._parent is None:
            return self._structs.get(id, None)
        return self._parent.find_struct(id)

    def add_variable(self, id, var):
        if id in self._variables:
            return False
        self._variables[id] = var
        return True

    def add_function(self, id, fn):
        if self._parent is None:
            if id in self._functions:
                return False
            self._functions[id] = fn
            return True
        return self._parent.add_function(id, fn)

    def add_struct(self, id, fn):
        if self._parent is None:
            if id in self._structs:
                return False
            self._structs[id] = fn
            return True
        return self._parent.add_struct(id, fn)

    def open_scope(self):
        return Greaser(self)

    def close_scope(self):
        return self._parent
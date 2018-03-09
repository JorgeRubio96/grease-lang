from struct import GreaseStruct
from variable import GreaseVar

class Greaser:
    def __init__(self, parent=None):
        self._parent = parent
        self._variables = {}
        
        if parent is None:
            self._functions = {}
            self._structs = {}

    def find_function(self, id):
        fn = id[0]
        var_name = id[1:]
        if self._parent is None:
            if len(var_name) > 0: # Struct fn
                var = self.find_variables(var_name)
                
                if var is None:
                    return None
                
                return self.find_struct(var.type).functions.get(fn, None)
            else: # Global fn
                return self._functions.get(id[0], None)
        return self._parent.find_function(id)
    
    def find_variables(self, id):
        base = id[-1]
        tail = id[0:-1]

        if self._parent is None:
            var = self._variables.get(base, None)
        else:
            var = self._variables.get(base, self._parent.find_variables(id))

        while len(tail) > 0:
            var = self.find_struct(var.type).variables.get(tail[-1], None)
            
            if var is None:
                break
            
            tail = tail[0:-1]

        return var

    def find_struct(self, id):
        if self._parent is None:
            return self._structs.get(id, None)
        return self._parent.find_struct(id)

    def add_variable(self, id, t):
        if id in self._variables:
            return False
        self._variables[id] = GreaseVar(t)
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

    def _set_error(self, val):
        self.error = True
        if self._parent is not None:
            self._parent._set_error(val)

    def syntax_error(self, msg):
        self._set_error(True)        
        print(msg)
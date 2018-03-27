class FunctionDirectory:
    def __init__(self):
        self._functions = {}

    def find_function(self, id):
        self._functions.get(id)

    def add_function(self, id, fn):
        if id not in self._functions:
            self._functions[id] = fn
            return True
        return False
from grease.core.exceptions import FunctionRedefinition

class FunctionDirectory:
    def __init__(self):
        self._functions = {}

    def find_function(self, id):
        return self._functions.get(id)

    def add_function(self, id, fn):
        if id in self._functions:
            raise FunctionRedefinition(id)
        self._functions[id] = fn
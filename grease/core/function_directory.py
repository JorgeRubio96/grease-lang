from grease.core.exceptions import FunctionRedefinition

class FunctionDirectory:
    def __init__(self):
        self._functions = {}

    def find_function(self, name):
        return self._functions.get(name)

    def add_function(self, name, fn):
        if name in self._functions:
            raise FunctionRedefinition(name)
        self._functions[name] = fn
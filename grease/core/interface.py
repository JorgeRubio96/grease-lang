from grease.core.function_directory import FunctionDirectory
from grease.core.exceptions import FunctionRedefinition

class Interface:
    def __init__(self, functions={}):
        self.functions = FunctionDirectory()

        for name, fn in functions.items():
            success = self.functions.add_function(name, fn)
            if not success:
                raise FunctionRedefinition(name)
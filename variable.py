from enum import Enum

class GreaseType(Enum):
    Int = 1
    Float = 2
    Char = 3
    Array = 4
    Struct = 5
    Pointer = 6

class GreaseVar:
    def __init__(self, grease_type, address, type_data=None):
        self.type = grease_type
        self.type_data = type_data
        self.address = address

class GreaseVarBuilder:
    def __init__(self):
        self._type = None
        self._type_data = None
        self._address = None

    def add_type(self, grease_type, type_data=None):
        self._type = grease_type
        self._type_data = type_data

    def add_address(self, address):
        self._address = address

    def build(self):
        return GreaseVar(self._type, self._address, self._type_data)
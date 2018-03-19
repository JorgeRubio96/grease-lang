from enum import Enum

class GreaseTypeClass(Enum):
    Int = 1
    Float = 2
    Char = 3
    Array = 4
    Struct = 5
    Pointer = 6
    Bool = 7

class GreaseType:
    def __init__(self, type_class, type_data=None, type_size=None):
        self.type_class = type_class
        self.type_data = type_data
        self.type_size = type_size
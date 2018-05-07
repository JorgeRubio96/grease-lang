from enum import Enum

class GreaseTypeClass(Enum):
    Int = 1
    Float = 2
    Char = 3
    Array = 4
    Struct = 5
    Pointer = 6
    Bool = 7
    Interface = 8

class GreaseType:
    def __init__(self, type_class, type_data=None, dimens=None, size=1):
        self.type_class = type_class
        self.type_data = type_data
        self.dimens = dimens
        self.size = size
        
    def __repr__(self):
        if self.type_class is GreaseTypeClass.Array:
            return '[{}, {}]'.format(self.type_data, self.dimens)
        elif self.type_class is GreaseTypeClass.Pointer:
            return '* {}'.format(self.type_data)
        elif self.type_class is GreaseTypeClass.Struct:
            return 'Struct({})'.format(self.type_data)
        
        return 'Instace {}'.format(self.type_class)

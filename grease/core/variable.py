class GreaseVar:
    def __init__(self, grease_type, address, offset=0):
        self.type = grease_type
        self.address = address

    def is_class(self, type_class):
        return self.type.type_class is type_class

class GreaseVarBuilder:
    def __init__(self):
        self._type = None
        self._address = None
        self._offset = 0

    def add_type(self, grease_type):
        self._type = grease_type

    def add_address(self, address):
        self._address = address

    def add_offset(self, offset):
        self._offset = offset

    def build(self):
        return GreaseVar(self._type, self._address, self._offset)

    def reset(self):
        self._type = None
        self._address = None
        self._offset = 0

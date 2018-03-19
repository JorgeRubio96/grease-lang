class GreaseVar:
    def __init__(self, grease_type, address):
        self.type = grease_type
        self.address = address

    def is_class(self, type_class):
        return self.type.type_class is type_class

class GreaseVarBuilder:
    def __init__(self):
        self._type = None
        self._address = None

    def add_type(self, grease_type):
        self._type = grease_type

    def add_address(self, address):
        self._address = address

    def build(self):
        return GreaseVar(self._type, self._address)

    def reset(self):
        self._type = None
        self._address = None
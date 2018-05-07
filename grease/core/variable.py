from enum import IntFlag
from grease.core.type import GreaseTypeClass

class AddressingMethod(IntFlag):
  Direct = 0x0000000000000000
  Indirect = 0x1000000000000000
  Literal = 0x2000000000000000
  Relative = 0x3000000000000000
  Param  = 0x4000000000000000

addr_type = {
  GreaseTypeClass.Int     : 0x0000000000000000,
  GreaseTypeClass.Float   : 0x0100000000000000,
  GreaseTypeClass.Char    : 0x0200000000000000,
  GreaseTypeClass.Bool    : 0x0300000000000000,
  GreaseTypeClass.Pointer : 0x0400000000000000
}

other_type = 0x0500000000000000

class GreaseVar:
  def __init__(self, grease_type, address, method=AddressingMethod.Direct):
    self.type = grease_type
    self._address = address
    self.method = method

  def is_class(self, type_class):
    return self.type.type_class is type_class

  def __repr__(self):
    return '{}: {}'.format(format(self.address, '#018x'), self.type)
  
  @property
  def address(self):
    if self.method is AddressingMethod.Indirect:
      return self.method | addr_type.get(self.type.type_data.type_class, other_type) | self._address
    return self.method | addr_type.get(self.type.type_class, other_type) | self._address

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

class AddressingModel:
  def __init__(self):
    self.current_var_address = 0
    self.current_global_var_address = [0, 1000, 2000, 3000, 4000, 5000]
 
  def get_next_var_address(self, type):
    '''Obtener la siguiente direccion'''
    self.current_var_address[type] += 1
    print("Pidiendo una nueva direccion -> {}".format(self.current_var_address[type] - 1))
    return self.current_var_address[type] - 1
 
  def get_next_global_var_address(self, type):
    '''Obtener la siguiente direccion global de la variable'''
    self.current_var_address[type] += 1
    return -1 * (self.current_var_address[type] - 1)
 
  def get_next_const_address(self):
    '''Obtener la siguiente direccion de constante'''
    self.current_const_address += 1
    return self.current_const_address - 1
 
  def  reset_var_addresses(self):
    self.current_var_address
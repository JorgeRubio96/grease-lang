from struct import GreaseStruct
from variable import GreaseVar
from type import GreaseTypeClass
from function import GreaseFn
from variable_table import VariableTable
from struct_table import StructTable
from function_directory import FunctionDirectory
from exceptions import TypeMismatch, UndefinedVariable, UndefinedFunction, UndefinedMember

type_class_dict = {
    'Int': GreaseTypeClass.Int,
    'Float': GreaseTypeClass.Float,
    'Char': GreaseTypeClass.Char
}

class Greaser:
    def __init__(self):
        self._global_vars = VariableTable()
        self._global_fns = FunctionDirectory()
        self._structs = StructTable()
        self._scope = self._global_vars
        self._current_fn = None

    def find_function(self, id):
        print(id)
        fn_name = id.pop()
        var = self.find_variable(id)
    
    def find_variable(self, name):
        var_name = name[0]
        var = self._scope.find_variable(var_name)

        if var is None:
            raise UndefinedVariable(var_name)

        for var_name in name[1:]:
            if var.is_class(GreaseTypeClass.Struct) or var.is_class(GreaseTypeClass.Pointer):
                struct = self.find_struct(var.data)
                var = struct.variables.find_variable(var_name)

                if var is None:
                    raise UndefinedMember('{} in type {}'.format(var_name, var.data))
            else:
                raise TypeMismatch('Expected {} but found {}'.format(GreaseTypeClass.Struct, var.type))
        
        return var

    def find_struct(self, id):
        return self._structs.find_struct(id)

    def add_variable(self, name, var):
        self._scope.add_variable(name,var)

    def add_function(self, id, fn, member=None):
        pass

    def add_struct(self, id, struct):
        pass

    def open_scope(self):
        self._scope = VariableTable(self._scope)

    def close_scope(self):
        self._scope = self._current_fn.close_scope()

    def eval(self, ap, left, right):
        pass

    @staticmethod
    def basic_type_from_text(name):
        return 
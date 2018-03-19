class StructTable:
    def __init__(self):
        self._structs = {}

    def find_struct(self, id):
        return self._structs.get(id)

    def add_struct(self, id, struct):
        if id not in self._structs:
            self._structs[id] = struct
            return True
        return False
class TypeDeclaration:

    def __init__(self, file_path):
        self.file_path = file_path
        self.types_declared = set()
    
    def add_type_declared(self, new_type):
        if type(new_type) == set:
            self.types_declared = self.types_declared.union(new_type)
        else:
            self.types_declared.add(new_type)

    def get_json_representation(self):
        return {
            "file_path" : self.file_path,
            "type_declared" : list(self.types_declared)
        }
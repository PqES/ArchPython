class Module:

    def __init__(self, name, package, files, allowed, forbidden, required):
        
        self.name = name
        self.package = package
        self.files = files
        self.allowed = allowed
        self.forbidden = forbidden
        self.required = required

        self.allowed_file_paths = None
        self.forbidden_file_paths = None
        self.required_file_file_paths = None

        self.__types_declared = set()
        self.__types_used = set()
        self.__types_used_file_path = set()
        self.__problems = []

        self.__filter_builtin = True



    def add_used_type(self, new_type):
        self.__types_used.add(new_type)
    
    def add_type_declared(self, new_type):
        if type(new_type) == set:
            self.__types_declared = self.__types_declared.union(new_type)
        else:
            self.__types_declared.add(new_type)
    
    def assign_types_used_file_path(self, files_used_set):
        self.__types_used_file_path = self.__types_used_file_path.union(files_used_set)
    
    def get_used_files_path(self):
        if not self.__filter_builtin:
            return self.__types_used_file_path
        else:
            new_types_used_file_path = set()
            for file_path in self.__types_used_file_path:
                if not "builtins" in file_path:
                    new_types_used_file_path.add(file_path)
            return new_types_used_file_path
    
    def get_types_declared(self):
        return self.__types_declared
    
    def add_types_used_set(self, used_set):
        self.__types_used = self.__types_used.union(used_set)
    
    def get_allowed_as_set(self):
        if self.allowed != None:
            return set(self.allowed)
        return set()
    
    def get_forbidden_as_set(self):
        if self.forbidden != None:
            return set(self.forbidden)
        return set()
    
    def get_required_as_set(self):
        if self.required != None:
            return set(self.required)
        return set()
    
    def get_types_used(self):
        return self.__types_used
    
    def report_problem(self, problem):
        self.__problems.append(problem)

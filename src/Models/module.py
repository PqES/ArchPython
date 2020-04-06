class Module:

    def __init__(self, name, package, files, allowed, forbidden, required):
        
        self.name = name
        self.package = package
        self.files = files
        self.allowed = allowed
        self.forbidden = forbidden
        self.required = required

        self.__types_used = set()
        self.__problems = []

    def add_used_type(self, type):
        self.__types_used.add(type)
    
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

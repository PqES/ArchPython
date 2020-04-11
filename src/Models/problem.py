class Problem:

    def __init__(self, problem_type, origin_module, restrictions_broken, is_warning = False):
        self.problem_type = problem_type
        self.origin_module = origin_module
        self.restrictions_broken = restrictions_broken
        self.category = "warning" if is_warning else "problem"
    
    def print_problem(self):
        print(f"A {self.category} was found at {self.origin_module.name}: {self.problem_type['Message']} - Types: {str(self.restrictions_broken)}")
    

    def get_problem_as_dict(self):
        return {
            "Module" : self.origin_module.name,
            "Category" : self.category,
            "Problem_Code" : self.problem_type['Code'],
            "Problem_Message" : self.problem_type['Message'],
            "Types" : str(self.restrictions_broken),
        }
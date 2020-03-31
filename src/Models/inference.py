class Inference(object):

    def __init__(self, file, variable, detailed_path):
        self.file = file
        self.variable = variable
        self.detailed_path = detailed_path
        self.possible_types = set()
    
    def add_type(self, possible_type):
        self.possible_types.add(possible_type)
    
    #Function for debug proporses
    def print_inference(self):
        print("****")
        print(f"File: {self.file}")
        print(f"Variable: {self.variable}")
        print(f"Detailed Path: {self.detailed_path}")
        print(f"Possible types: {str(self.possible_types)}")
        print("****")


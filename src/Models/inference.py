class Inference(object):

    def __init__(self, file, variable):
        self.file = file
        self.variable = variable
        self.possible_types = set()
    
    def add_type(self, possible_type):
        self.possible_types.add(possible_type)

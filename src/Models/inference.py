class Inference(object):

    def __init__(self, file_path, file_name, class_name, class_function, variable_name, variable_type):
        self.file_path = file_path
        self.file_name = file_name
        self.class_name = class_name
        self.class_function = class_function
        
        self.inference_fullname = f"{file_name}::{class_name}::{self.class_function}"

        self.variable_name = variable_name
        self.variable_type = variable_type

    def get_tuple_representation(self):
        return (self.inference_fullname, self.variable_name, self.variable_type)
    
    def get_key(self):
        return self.inference_fullname + self.variable_name + self.variable_type



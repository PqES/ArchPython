class Inference(object):

    def __init__(self, file_path, file_name, class_name, class_function, variable_name, variable_type, inference_variable_path, is_external_package = False, line_no = 0):
        self.file_path = file_path
        self.file_name = file_name
        self.class_name = class_name
        self.class_function = class_function
        self.origin_module = None #O modulo que pertence ao tipo que estamos tentando inferir
        
        self.inference_fullname = f"{file_name}::{class_name}::{self.class_function}"

        self.variable_name = variable_name
        self.variable_type = variable_type

        self.inference_variable_path = inference_variable_path
        self.inferred_module_name = None #o módulo que pertence o tipo inferido
        self.is_external_package = is_external_package

        self.line_no = line_no

        # self.inferred_full_name = 

    def get_tuple_representation(self):
        return (self.inference_fullname, self.variable_name, self.variable_type)
    
    def set_origin_module(self, module):
        self.origin_module = module
    
    def set_inferred_module_name(self, module):
        self.inferred_module_name = module
    
    def get_key(self):
        return self.inference_fullname + self.variable_name + self.variable_type
    
    def get_detailed_inference(self):
        return {
            "file_path" : self.file_path,
            "file_name": self.file_name,
            "class_name": self.class_name,
            "class_function": self.class_function,
            "origin_module" : self.origin_module,
            "variable_name": self.variable_name,
            "variable_inferred_type": self.variable_type,
            "variable_inferred_path" : self.inference_variable_path,
            "inferred_module_name" : self.inferred_module_name
        }



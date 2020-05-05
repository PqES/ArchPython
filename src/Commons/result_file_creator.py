import json
from Enums.problems_enum import ProblemsEnum

class ResultFileCreator:

    def __init__(self, inferences, module_definitions):

        self.inferences = inferences
        self.module_definitions = module_definitions
        self.file_content = {ProblemsEnum.DIVERGENCE.name : [], ProblemsEnum.ABSENCE.name : []}
    
        self.__file_inferences_dict = {}

    def create_json_file(self):
        self.__create_file_inference_dict()
        self.find_divergences()
        self.find_abscences()
        self.write_result()
    
    def write_result(self):
        with open('./results/teste.json', 'w') as output:
            json.dump(self.file_content, output)

        
    def __create_file_inference_dict(self):
        file_inference_dict = {}
        for inference in self.inferences:
            file_path = inference.file_path
            if file_path in file_inference_dict.keys():
                file_inference_dict[file_path].append(inference)
            else:
                file_inference_dict[file_path] = [] 
                file_inference_dict[file_path].append(inference)
        self.__file_inferences_dict = file_inference_dict

    def __file_access_module(self, file, module):
        if "__init__" in file:
            return True
        inferences = self.__file_inferences_dict[file]
        for inference in inferences:
            if inference.inferred_module_name == module:
                return True
        return False    
    
    
    def find_abscences(self):
        for module in self.module_definitions:
            if module.required != None:
                for module_required in module.required:
                    for file in module.files:
                        if not self.__file_access_module(file, module_required):
                            self.__report_abcense(module, file, module_required)
    
    def __report_abcense(self, module, file, module_required_name):

        problem_description = {
            'origin_module' : module.name,
            'origin_line': '',
            'origin_file_path' : file,
            'target_module' : module_required_name,
            'target_class' : '',
            'constraint' : ProblemsEnum.ABSENCE.value['Message'].format(module.name, module_required_name)
        }
        self.file_content[ProblemsEnum.ABSENCE.name].append(problem_description)

    def __report_problem(self, module, module_required_name, problem_enum):
        problem_description = {
            'origin_module' : module.name,
            'origin_class' : module.inference_fullname,
            'target_module' : module.inferred_module_name,
            'target_class' : '',
            'constraint' : problem_enum.value['message'].format(module.name, module_required_name)
        }
        self.file_content[problem_enum.name].append(problem_description)


    def find_divergences(self):
        pass
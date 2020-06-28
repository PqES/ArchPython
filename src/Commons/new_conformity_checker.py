from Models.Visualization.Graph.graph import Graph
from Models.Visualization.Graph.node import Node
from Models.Visualization.Graph.edge import Edge
from Models.conformity import Conformity
from Enums.conformity_status_enum import ConformityStatusEnum
from Enums.edge_status_enum import EdgeStatusEnum


class NewConformityChecker:

    def __init__(self, inferences, module_definitions):
        self.inferences = inferences
        self.module_definitions = module_definitions

        self.__file_inferences_dict = {}

        self.__modules_usage = {}

        self.__all_modules = set([module.name for module in self.module_definitions])

        self.__conformities = []

    
    def check_conformity(self):
        self.__calculate_modules_usage()
        self.__create_file_inference_dict()
        self.__create_conformity_model()

        return self.__conformities

    def __calculate_modules_usage(self):
        for inference in self.inferences:
            if inference.origin_module == inference.inferred_module_name:
                continue
            else:
                key = (inference.origin_module, inference.inferred_module_name)
                if key in self.__modules_usage.keys():
                    self.__modules_usage[key] += 1
                else:
                    self.__modules_usage[key] = 1

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

    def __create_conformity_model(self):
        for module in self.module_definitions:
            self.__find_divergences(module) #Laranja dashed
            self.__find_absences(module) #Dotted red - requerido e não usado
            self.__find_warnings_and_allowed(module) #Gray Normal and black
    
    def __find_divergences(self, module):
        if module.forbidden != None:
            for module_forbidden in module.forbidden:
                key = (module.name, module_forbidden)
                if (key in self.__modules_usage.keys()):
                    conformity = Conformity(module.name, module_forbidden, self.__modules_usage[key], ConformityStatusEnum.DIVERGENCE)
                    self.__conformities.append(conformity)
    
    def __find_absences(self, module):
        if module.required != None:
    
            for module_required in module.required:
                file_dont_use_a_module = False

                for file in module.files:
                    if not self.__file_access_module(file, module_required):
                        file_dont_use_a_module = True
        
                if file_dont_use_a_module:
                    key = (module.name, module_required)
                    conformity = Conformity(module.name, module_required, self.__modules_usage[key], ConformityStatusEnum.ABSCENSE)
                    self.__conformities.append(conformity)

    #metodos que são permitidos mas não utilizados
    # 1 - explicitamente permitidos
    # 2 = não explicitamente permitidos, não está no forbidden
    def __find_warnings_and_allowed(self, module):
        all_modules_allowed = self.__get_all_modules_allowed(module)
        if all_modules_allowed != None:
            for module_allowed in all_modules_allowed:
                key = (module.name, module_allowed)
                conformity = None
                if (key not in self.__modules_usage.keys()):
                    conformity = Conformity(module.name, module_allowed, 0, ConformityStatusEnum.WARNING)
                else:
                    conformity = Conformity(module.name, module_allowed, self.__modules_usage[key], ConformityStatusEnum.ALLOWED)
                self.__conformities.append(conformity)


    def __get_all_modules_allowed(self, module):
        if module.allowed != None:
            return set(module.allowed)
        # elif module.forbidden != None:
        #     modules = self.__all_modules.difference(set(module.forbidden)) 
        #     modules.remove(module.name)
        #     return modules
        else:
            return None
    
    def __file_access_module(self, file, module):
        if "__init__" in file:
            return True
        
        if file not in self.__file_inferences_dict.keys():
            return False
            
        inferences = self.__file_inferences_dict[file]
        for inference in inferences:
            if inference.inferred_module_name == module:
                return True
        return False
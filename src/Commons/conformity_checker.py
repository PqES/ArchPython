import json
from Models.problem import Problem
from Enums.problems_enum import ProblemsEnum

class ConformityChecker:

    def __init__(self, module_definitions, inferences, types_declared):
        self.module_definitions = module_definitions
        self.inferences = inferences
        self.types_declared = types_declared

        self.__assign_types_to_modules()
        
        self.__file_types_cache = {}
        self.__inference_cache = {}
        self.__files_used_cache = {}
        self.__module_cache = {}
        self.__problems = []
    
    def check_conformity(self):
        
        # Cria um dicionário do tipo <caminho_arquivo> -> <conjunto de tipos>
        self.__create_file_types_cache()

        # Cria um dicionário do tipo <caminho_do_arquivo> -> <conjunto de inferencias>
        self.__create_inference_cache()

        # Cria um dicionário do tipo <caminho do arquivo> -> <conjuntos de arquivo utilizado>
        self.__create_files_used_cache()

        # Atribui a cada modulo os arquivos que ele está utilizando
        self.__assign_files_used()
        
        #Atribui a cada modulo todos os tipos que estão sendo usados dentro dele
        self.__assign_types_used()

        self.__create_module_by_name_cache()

        #Verificar conformidade
        self.__check_conformity()

        self.__print_problems()

        self.__write_problems()

        pass

    
    def __create_module_by_name_cache(self):
        for module in self.module_definitions:
            self.__module_cache[module.name] = module

    def __create_inference_cache(self):
        inference_cache = {}
        for inference in self.inferences:
            if not inference.file_path in inference_cache.keys():
                inference_cache[inference.file_path] = set()
            inference_cache[inference.file_path].add(inference)
        self.__inference_cache = inference_cache

    def __create_files_used_cache(self):
        files_used_cache = {}
        for module in self.module_definitions:
            for file in module.files:
                if not file in files_used_cache.keys():
                    files_used_cache[file] = set()
                inferences = self.__inference_cache[file]
                if inferences != None:
                    for inference in inferences:
                        files_used_cache[file].add(inference.inference_variable_path)
        self.__files_used_cache = files_used_cache


    def __assign_types_to_modules(self):
        for type_declaration in self.types_declared:
            for module in self.module_definitions:
                if type_declaration.file_path in module.files:
                    module.add_type_declared(type_declaration.types_declared)


    # Cria um dicionário do tipo <caminho_arquivo> -> <conjunto de tipos>
    def __create_file_types_cache(self):
        file_types_cache = {}
        for inference in self.inferences:
            if inference.file_path in file_types_cache.keys():
                file_types_cache[inference.file_path].add(inference.variable_type)
            else:
                file_types_cache[inference.file_path] = set()
                file_types_cache[inference.file_path].add(inference.variable_type)
        self.__file_types_cache = file_types_cache

    # Atribui a cada modulo todos os tipos que estão sendo usados dentro dele
    def __assign_types_used(self):
        for module in self.module_definitions:
            for file_path in module.files:
                module.add_types_used_set(self.__file_types_cache[file_path])
    
    #Atribui a cada modulo todos os arquivos que estão sendo utilizados por ele
    def __assign_files_used(self):
        for module in self.module_definitions:
            for file_path in module.files:
                module.assign_types_used_file_path(self.__files_used_cache[file_path])

    
    # Checa de fato a conformidade da arquitetura
    def __check_conformity(self):
        for module in self.module_definitions:
            if module.allowed != None:
                self.__check_allowed(module)
            
            if module.forbidden != None:
                self.__check_forbidden(module)
            
            if module.required != None:
                self.__check_required(module)
    

    def __check_allowed(self, module):
        allowed_set = module.get_allowed_as_set()
        required_set = module.get_required_as_set()

        allowed_and_required_set = allowed_set.union(required_set)

        allowed_and_required_files_per_module = self.__restriction_files_per_module(allowed_and_required_set)

        used_files_path = module.get_used_files_path()
        used_modules = module.get_types_used()


        for allowed_and_required_module in allowed_and_required_files_per_module.keys():
            allowed_and_required = set(allowed_and_required_files_per_module[allowed_and_required_module])
            if len(allowed_and_required.difference(used_files_path)) == 0:
                used_modules.remove(allowed_and_required_module)
        
        if len(used_modules) > 0:
            problem = Problem(ProblemsEnum.ALLOWED_RESTRICTION_BROKEN.value, module, used_modules, True)
            self.__report_problem(problem, module)


            

    def __check_forbidden(self, module):
        forbidden_set = module.get_forbidden_as_set()

        forbidden_files_per_module = self.__restriction_files_per_module(forbidden_set)
        used_files_path = module.get_used_files_path()

        forbidden_modules_used = set()

        for forbidden_module in forbidden_files_per_module.keys():
            forbidden_set = set(forbidden_files_per_module[forbidden_module])
            if (len(forbidden_set.intersection(used_files_path)) > 0):
                forbidden_modules_used.add(forbidden_module)

        if len(forbidden_modules_used) > 0 :
            problem = Problem(ProblemsEnum.FORBIDDEN_RESTRICTION_BROKEN.value, module, forbidden_modules_used)
            self.__report_problem(problem, module)

    
    def __check_required(self, module):
        required_set = module.get_required_as_set()

        required_files_per_module = self.__restriction_files_per_module(required_set)
        used_files_path = module.get_used_files_path()
        
        modules_used = set()

        for required_file in required_files_per_module.keys():
            requires_set = set(required_files_per_module[required_file])
            if (len(requires_set.intersection(used_files_path)) > 0):
                modules_used.add(required_file)


        if modules_used != required_set:
            required_not_used = required_set.difference(modules_used)
            problem = Problem(ProblemsEnum.REQUIRED_RESTRICTION_BROKEN.value, module, required_not_used)
            self.__report_problem(problem, module)

    
    def __restriction_files_per_module(self, restriction_set): 
        restriction_files_per_module = {}
        for module_restriction in restriction_set:
            restriction_files_per_module[module_restriction] = self.__module_cache[module_restriction].files
        return restriction_files_per_module
    
    
    def __report_problem(self, problem, module):
        self.__problems.append(problem)
        module.report_problem(problem)
    
    def __print_problems(self):
        for problem in self.__problems:
            problem.print_problem()
    
    def __write_problems(self):
        json_content = []
        for problem in self.__problems:
            json_content.append(problem.get_problem_as_dict())
        
        with open('./results/problems.json', 'w') as output:
            json.dump(json_content, output)
    



import jedi
import sys
import json
from Jedi.read_py_files import ReadPyFiles
from Enums.jedi_error_enum import JediErrorEnum
from Models.inference import Inference
from Models.call import Call
from Models.type_declaration import TypeDeclaration

#TODO mudar o nome dessa classe
class Skywalker(object):

    def __init__(self, project_root_folder):
        self.project_root_folder = project_root_folder
        self.files = None
        self.inferences = {}
        self.list_of_inferences = []
        self.list_of_calls = [] #Lista de chamadas para outros arquivos.
        
        self.file_modules_cache = {} #Cache com os dados arquivo -> Modulo que ele pertence

        self.__type_declarations = []
    
    def run_jedi(self):
        #Lê os arquivos
        self.__search_project_folder()
        
        #Faz o passe base da inferência
        self.__base_step()

        #faz o passo recursivo da inferência
        self.__recursive_step(len(self.list_of_inferences))

        #escreve as inferências em um arquivo json
        self.__write_list_of_inferences()

        #escreve as inferências de uma maneira mais detalhada
        self.__write_list_of_detailed_inferences()

        self.__write_types_declared()
    
    def get_type_declarations(self):
        return self.__type_declarations
    
    def set_modules(self, modules):
        for module in modules:
            if module.files:
                for file in module.files:
                    self.file_modules_cache[file] = module.name
            if module.packages:
                for package in module.packages:
                    self.file_modules_cache[package] = module.name
    
    def __write_types_declared(self):
        json_content = []
        for type_declared in self.__type_declarations:
            json_content.append(type_declared.get_json_representation())
        
        with open('./results/types_declared.json', 'w') as output:
            json.dump(json_content, output)
    
    def __write_list_of_inferences(self):
        json_content = []
        for inference in self.list_of_inferences:
            json_content.append(list(inference.get_tuple_representation()))
        
        with open('./results/simple_inferences.json', 'w') as output:
            json.dump(json_content, output)
        
    def __write_list_of_detailed_inferences(self):
        json_content = []
        for inference in self.list_of_inferences:
            json_content.append(inference.get_detailed_inference())
        
        with open('./results/detailed_inferences.json', 'w') as output:
            json.dump(json_content, output)


    def get_inferences(self):
        return self.list_of_inferences
    
    def get_files(self):
        return self.files
    
    def __search_project_folder(self):
        read_py_files = ReadPyFiles(self.project_root_folder)
        read_py_files.find_pys()
        all_files = read_py_files.get_files_path()

        files_filtered = []

        for file in all_files:
            if file in self.file_modules_cache.keys():
                files_filtered.append(file)
        
        self.files = files_filtered
    
    def __base_step(self):
        param_count = 0
        if self.files == None:
            raise Exception(JediErrorEnum.NO_FILES_FOUND.value)

        for file_path  in self.files:
            
            type_declaration = TypeDeclaration(file_path)
            script_names = jedi.Script(path=file_path).get_names(all_scopes=True, definitions=True, references=True)

            should_verify_params = False
            current_definition = None
            current_goto = None
            current_goto_params_names = []

            for current_index, definition in enumerate(script_names):

                if definition.type == "param":
                    param_count += 1


                if definition.description == "super":
                    inherited_class = self.find_inheritance(current_index, script_names)
                    inference_object = self.__create_inference(definition, inherited_class, True)
                    self.__add_to_list_of_inferences(inference_object)
                    continue

                if (self.__is_a_new_type_declared(definition, file_path)):
                    type_declaration.add_type_declared(definition.name)

                if should_verify_params and current_definition and current_goto:
                    if definition._name.tree_name.parent.type == "arglist" or definition._name.tree_name.parent.type == "trailer":
                        
                        file_path_from = current_definition.module_path
                        variable_from = definition.name
                        current_definition_full_name = self.__generate_function_name(current_definition)

                        file_path_to = current_goto.module_path
                        variable_to = current_goto_params_names.pop().name
                        current_goto_full_name = self.__generate_function_name(current_goto)


                        call = Call(file_path_from, variable_from, current_definition_full_name, file_path_to, variable_to, current_goto_full_name, line_no_from = current_definition.line)
                        self.list_of_calls.append(call)
                    # elif definition._name.tree_name.parent.type == "atom_expr" and len(current_goto_params_names) > 0:
                    #     continue
                    else:
                        should_verify_params = False
                        current_definition = None
                        current_definition_full_name = None

                definitions_goto = definition.goto(follow_imports=True, follow_builtin_imports=True)

                if (len(definitions_goto) > 0):
                    for goto in definitions_goto:
                        #Se chegar até aqui é pq tem uma chamada de função e devemos registrar isso 
                        if goto.type == "function" and goto != definition:
                            current_definition = definition
                            current_goto = goto
                            current_goto_params_names = goto.params[::-1]

                            should_verify_params = True

                if not self.__should_ignore_definition(definition) :
                    inferences = definition.infer()

                    file_name = definition.module_name
                    variable_name = definition.name

                    for inference in inferences:

                        #Esse cara vai ignorar o caso no qual é a instanciação de uma classe
                        # Exemplo: Classe()
                        if (inference.name == definition.name):
                            if (self.__check_if_return_exists_inline(file_path, definition.line)):
                                inference_object = self.__create_inference_from_return(definition, inference)
                                self.__add_to_list_of_inferences(inference_object)
                            continue

                            
                        # if inference.module_name != None:
                        #     continue

                        #  and "builtins" in inference.module_name:
                        inference_object = self.__create_inference(definition, inference)
                        self.__add_to_list_of_inferences(inference_object)
                
            self.__type_declarations.append(type_declaration)
        
        print(param_count)

        print("End of base step")
    
    def __is_a_new_type_declared(self, definition, current_file_path):
        if definition.type == "class":
            definitions_goto = definition.goto(follow_imports=True, follow_builtin_imports=True)
            for goto in definitions_goto:
                if goto.module_path == current_file_path:
                    return True
        return False
    
    def find_inheritance(self, current_definition_index, script_names):
        for index in range(current_definition_index, len(script_names)):
            current_definition = script_names[index]
            if current_definition.description == "__init__":
                definitions_goto = current_definition.goto(follow_imports=True, follow_builtin_imports=True)

                if (len(definitions_goto) > 0):
                    for goto in definitions_goto:
                        #Se chegar até aqui é pq tem uma chamada de função e devemos registrar isso 
                        if goto.type == "function" and goto != current_definition:
                            return goto
    
    def __check_if_return_exists_inline(self, file_path, line_no):
        with open(file_path) as file:
            lines = file.readlines()
            return "return" in str(lines[line_no - 1])



    def __recursive_step(self, current_len_of_types):

        for call in self.list_of_calls:

            infered_types = self.__find_inference(call)

            if infered_types != []:
                for infered_type in infered_types:
                    # inference_path = infered_type.module_path if not infered_type.in_builtin_module() else infered_type.full_name
                    new_inference = Inference(call.file_path_to, call.file_name_to, call.class_to, call.function_to, call.variable_to, infered_type.variable_type, infered_type.inference_variable_path, line_no=call.line_no_from)
                    if call.file_path_to in self.file_modules_cache.keys():
                        new_inference.set_origin_module(self.file_modules_cache[call.file_path_to])
                    else:
                        new_inference.set_origin_module(call.file_name_to)

                    inferred_module_name = ""
                    if "builtins" in infered_type.inference_variable_path:
                        inferred_module_name = infered_type.inference_variable_path
                    elif infered_type.is_external_package:
                        new_inference.is_external_package = True
                        inferred_module_name = infered_type.inferred_module_name
                    else:
                        inferred_module_name = self.file_modules_cache[infered_type.inference_variable_path]


                    new_inference.set_inferred_module_name(inferred_module_name)
                    self.__add_to_list_of_inferences(new_inference)
        if len(self.list_of_inferences) != current_len_of_types:
            self.__recursive_step(len(self.list_of_inferences))
        
        print("End of recursive step")
        
    
    def __find_inference(self, call):
        all_inferences = []
        for inference in self.list_of_inferences:
            if inference.inference_fullname == call.full_name_from and inference.variable_name == call.variable_from:
                all_inferences.append(inference)
        return all_inferences

    def __add_to_list_of_inferences(self,new_inference):
        # if "builtins" in new_inference.inferred_module_name or "builtinsi" in new_inference.inferred_module_name or "builtinsi" in new_inference.origin_module:
        #     return

        for inference in self.list_of_inferences:
            if new_inference.get_key() == inference.get_key():
                return
        
        self.list_of_inferences.append(new_inference)

    def __create_tuple_from_self(self, definition):
        file_class_function_key = self.__generate_function_name(definition)
        variable_name = definition.name
        inference = self.__find_current_class_name(definition)
        return (file_class_function_key, variable_name, inference)
    
    def __create_inference_from_return(self, definition, inference):
        file_path = definition.module_path
        file_name = definition.module_path.split("/")[-1].replace('.py', '')
        class_name = self.__find_current_class_name(definition)
        function_name = self.__find_current_function_name(definition)
        variable_name = "function_return"
        variable_type = inference.name
        inference_path = inference.module_path if not inference.in_builtin_module() else inference.full_name
        line_no = definition.line

        inference = Inference(file_path, file_name, class_name, function_name, variable_name, variable_type, inference_path, line_no=line_no)

        inference.set_origin_module(self.file_modules_cache[file_path])

        if "builtins" in inference_path:
            inference.set_inferred_module_name(inference_path)
        else:
            inference.set_inferred_module_name(self.file_modules_cache[inference_path])

        return inference
    
    def __create_inference_from_external_package(self,definition, inference, from_super=False):
        file_path = definition.module_path
        file_name = definition.module_path.split("/")[-1].replace('.py', '')
        class_name = self.__find_current_class_name(definition)
        function_name = self.__find_current_function_name(definition)
        variable_name = definition.name
        variable_type =  inference.name if not from_super else inference.full_name.split('.')[-2]
        inference_path = inference.module_path if not inference.in_builtin_module() else inference.full_name
        line_no = definition.line

        new_inference = Inference(file_path, file_name, class_name, function_name, variable_name, variable_type, inference_path, True, line_no=line_no)

        new_inference.set_origin_module(self.file_modules_cache[file_path])
        module_inferred = (inference.module_name.split(".")[0]).lower()
        if module_inferred in self.file_modules_cache.keys():
            new_inference.set_inferred_module_name(self.file_modules_cache[module_inferred])
        else:
            new_inference.set_inferred_module_name(module_inferred)
        return new_inference

    
    def __create_inference(self, definition, inference, from_super=False):
        
        if inference.module_path != None and "site-packages" in inference.module_path and inference.module_name != "builtins":
            inference = self.__create_inference_from_external_package(definition, inference, from_super)
            return inference
        
        if inference.module_name != None and "builtins" in inference.module_name:
            inference = self.__create_inference_from_external_package(definition, inference, from_super)
            return inference

        file_path = definition.module_path
        file_name = definition.module_path.split("/")[-1].replace('.py', '')
        class_name = self.__find_current_class_name(definition)
        function_name = self.__find_current_function_name(definition)
        variable_name = definition.name
        variable_type =  inference.name if not from_super else inference.full_name.split('.')[-2]
        inference_path = inference.module_path if not inference.in_builtin_module() else inference.full_name
        line_no = definition.line

        inference = Inference(file_path, file_name, class_name, function_name, variable_name, variable_type, inference_path, line_no=line_no)

        inference.set_origin_module(self.file_modules_cache[file_path])

        if "builtins" in inference_path:
            inference.set_inferred_module_name(inference_path)
        else:
            inference.set_inferred_module_name(self.file_modules_cache[inference_path])

        return inference
    
    
    def __should_ignore_definition(self, inference):
        if inference.description == "__name__":
            return True
        if inference.name == "__init__":
            return True
        if inference.type == "statement" or inference.type == "param":
            return False
        return True
    
    #Talvez essa função dê problema quando existir dois arquivos com mesmo nome, classe, funcao 
    def __generate_function_name(self, definition):
        file_name = definition.module_path.split("/")[-1].replace('.py', '')
        current_class_name = self.__find_current_class_name(definition)
        current_function_name = self.__find_current_function_name(definition)
        
        key = f"{file_name}::{current_class_name}::{current_function_name}"

        return key
    
    def __find_current_class_name(self, definition):
        if definition.type == "class":
            return definition.name
        parent = definition.parent()
        if parent:
            return self.__find_current_class_name(parent)
        else: 
            return "root"
    
    def __find_current_function_name(self, definition):
        if definition.type == "function":
            return definition.name
        parent = definition.parent()
        if parent:
            return self.__find_current_function_name(definition.parent())
        else: 
            return "root"
    
    def get_jedi_results(self):
        for index in self.files:
            print(self.files[index].get_as_dict())
    




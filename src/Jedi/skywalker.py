import jedi
import sys
import json
from Jedi.read_py_files import ReadPyFiles
from Enums.jedi_error_enum import JediErrorEnum
from Utils.json_writer import JsonWriter
from Models.inference import Inference
from Models.call import Call

#TODO mudar o nome dessa classe
class Skywalker(object):

    def __init__(self, project_root_folder):
        self.project_root_folder = project_root_folder
        self.files = None
        self.inferences = {}
        self.list_of_inferences = []
        self.list_of_calls = [] #Lista de chamadas para outros arquivos.
    
    def run_jedi(self):
        #Lê os arquivos
        self.__search_project_folder()
        
        #Faz o passe base da inferência
        self.__base_step()

        #faz o passo recursivo da inferência
        self.__recursive_step(len(self.list_of_inferences))

        #escreve as inferências em um arquivo json
        self.__write_list_of_inferences()
    
    def __write_list_of_inferences(self):
        json_content = []
        for inference in self.list_of_inferences:
            json_content.append(list(inference.get_tuple_representation()))
        
        with open('data.json', 'w') as output:
            json.dump(json_content, output)


    def get_inferences(self):
        return self.list_of_inferences
    
    def get_files(self):
        return self.files
    
    def __search_project_folder(self):
        read_py_files = ReadPyFiles(self.project_root_folder)
        read_py_files.find_pys()
        self.files = read_py_files.get_files_path()
    
    def __base_step(self):
        if self.files == None:
            raise Exception(JediErrorEnum.NO_FILES_FOUND.value)

        for file_path  in self.files:
            script_names = jedi.Script(path=file_path).get_names(all_scopes=True, definitions=True, references=True)

            should_verify_params = False
            current_definition = None
            current_goto = None
            current_goto_params_names = []

            for definition in script_names:

                if should_verify_params and current_definition and current_goto:
                    if definition._name.tree_name.parent.type == "arglist" or definition._name.tree_name.parent.type == "trailer":
                        
                        file_path_from = current_definition.module_path
                        variable_from = definition.name
                        current_definition_full_name = self.__generate_function_name(current_definition)

                        file_path_to = current_goto.module_path
                        variable_to = current_goto_params_names.pop().name
                        current_goto_full_name = self.__generate_function_name(current_goto)


                        call = Call(file_path_from, variable_from, current_definition_full_name, file_path_to, variable_to, current_goto_full_name)
                        self.list_of_calls.append(call)
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


                if not self.__should_ignore_definition(definition):
                    inferences = definition.infer()

                    file_name = definition.module_name
                    variable_name = definition.name

                    for inference in inferences:

                        #Esse cara vai ignorar o caso no qual é a instanciação de uma classe
                        # Exemplo: Classe()
                        if (inference.name == definition.name):
                            continue
                        
                        inference_object = self.__create_inference(definition, inference)
                        self.__add_to_list_of_inferences(inference_object)

        print("End of base step")

    def __recursive_step(self, current_len_of_types):

        for call in self.list_of_calls:

            infered_types = self.__find_inference(call)

            if infered_types != []:
                for infered_type in infered_types:
                    new_inference = Inference(call.file_path_to, call.file_name_to, call.class_to, call.function_to, call.variable_to, infered_type)
                    self.__add_to_list_of_inferences(new_inference)
        
        if len(self.list_of_inferences) != current_len_of_types:
            self.__recursive_step(len(self.list_of_inferences))
        
        print("End of recursive step")
        
    
    def __find_inference(self, call):
        all_inferences = []
        for inference in self.list_of_inferences:
            if inference.inference_fullname == call.full_name_from and inference.variable_name == call.variable_from:
                all_inferences.append(inference.variable_type)
        return all_inferences

    def __add_to_list_of_inferences(self,new_inference):
        for inference in self.list_of_inferences:
            if new_inference.get_key() == inference.get_key():
                return
        self.list_of_inferences.append(new_inference)

    def __create_tuple_from_self(self, definition):
        file_class_function_key = self.__generate_function_name(definition)
        variable_name = definition.name
        inference = self.__find_current_class_name(definition)
        return (file_class_function_key, variable_name, inference)
    
    def __create_inference(self, definition, inference):
        file_path = definition.module_path
        file_name = definition.module_path.split("/")[-1].replace('.py', '')
        class_name = self.__find_current_class_name(definition)
        function_name = self.__find_current_function_name(definition)
        variable_name = definition.name
        variable_type = inference.name

        inference = Inference(file_path, file_name, class_name, function_name, variable_name, variable_type)

        return inference
    
    def __should_ignore_definition(self, inference):
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
        return self.__find_current_class_name(definition.parent())
    
    def __find_current_function_name(self, definition):
        if definition.type == "function":
            return definition.name
        return self.__find_current_function_name(definition.parent())
    
    def get_jedi_results(self):
        for index in self.files:
            print(self.files[index].get_as_dict())
    
    def register_jedi_results(self):
        list_of_files_as_dict = []
        for index in self.files:
            list_of_files_as_dict.append(self.files[index].get_as_dict())
        JsonWriter.write_json(list_of_files_as_dict)




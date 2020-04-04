import jedi
import sys
import json
from Jedi.read_py_files import ReadPyFiles
from Enums.jedi_error_enum import JediErrorEnum
from Utils.json_writer import JsonWriter
from Models.inference import Inference

#TODO mudar o nome dessa classe
class Skywalker(object):

    def __init__(self, project_root_folder):
        self.project_root_folder = project_root_folder
        self.files = None
        self.inferences = {}
        self.list_of_inferences_tuples = []
        self.list_of_calls = [] #Lista de chamadas para outros arquivos.
    
    def run_jedi(self):
        #Lê os arquivos
        self.__search_project_folder()
        #Faz a inferência
        self.__make_inference()

        self.__recursive_step(len(self.list_of_inferences_tuples))

        self.__write_list_of_inferences()
    
    def __write_list_of_inferences(self):
        json_content = []
        for inference in self.list_of_inferences_tuples:
            json_content.append(list(inference))
        
        with open('data.json', 'w') as output:
            json.dump(json_content, output)


    def get_inferences(self):
        return self.inferences
    
    def get_files(self):
        return self.files
    
    def __search_project_folder(self):
        read_py_files = ReadPyFiles(self.project_root_folder)
        read_py_files.find_pys()
        self.files = read_py_files.get_files_dictionary()
    
    #TODO tratar quando tiver mais de dois arquivos em uma classe
    #TODO pegar o método que está chamando
    #TODO pegar o arquivo que está chamando
    def __make_inference(self):
        if self.files == None:
            raise Exception(JediErrorEnum.NO_FILES_FOUND.value)

        for key in self.files:
            file = self.files[key]

            # script_names = jedi.Script(path=file.file_path).get_names(all_scopes=True)

            script_names = jedi.Script(path=file.file_path).get_names(all_scopes=True, definitions=True, references=True)
            teste2 = jedi.Script(path=file.file_path)
            teste = teste2.get_signatures()

            should_verify_params = False
            current_function_name = None
            goto_function_name = None
            current_goto_params_names = []

            for definition in script_names:

                if should_verify_params and current_function_name != None and goto_function_name != None: 
                    if definition._name.tree_name.parent.type == "arglist" or definition._name.tree_name.parent.type == "trailer":
                        call_tuple = (current_function_name, goto_function_name, definition.name, current_goto_params_names.pop().name)
                        self.list_of_calls.append(call_tuple)
                    else:
                        should_verify_params = False
                        current_function_name = None
                        goto_function_name = None

                b = definition.get_signatures()

                goto_teste = definition.goto(follow_imports=True, follow_builtin_imports=True)

                if (len(goto_teste) > 0):
                    for goto in goto_teste:
                        #Se chegar até aqui é pq tem uma chamada de função e devemos registrar isso 
                        if goto.type == "function" and goto != definition:
                            current_function_name = self.__generate_function_name(definition)
                            goto_function_name = self.__generate_function_name(goto)
                            current_goto_params_names = goto.params[::-1]
                            should_verify_params = True


                if not self.__should_ignore_definition(definition, file):
                    inferences = definition.infer()

                    file_name = definition.module_name
                    variable_name = definition.name
                    inference_key = definition.full_name if definition.full_name != None else definition.desc_with_module

                    self.inferences[inference_key] = Inference(file_name, variable_name, inference_key)

                    for inference in inferences:

                        #Esse cara vai ignorar o caso no qual é a instanciação de uma classe
                        # Exemplo: Classe()
                        if (inference.name == definition.name):
                            continue
                        inference_tuple = self.__create_tuple_from_inference(definition, inference)
                        self.__add_to_list_of_tuples(inference_tuple)
                        self.inferences[inference_key].add_type(inference.name)
                        self.files[key].types.add(inference.name)

            
            #Debug Proposes
            for inference in self.inferences.keys():
                self.inferences[inference].print_inference()

        pass

    def __recursive_step(self, current_len_of_types):
        for call in self.list_of_calls:
            method = call[0]
            function_called = call[1]
            variable = call[2]

            infered_types = self.__find_inference(method, variable)

            if infered_types != []:
                for infered_type in infered_types:
                    inference_tuple = (function_called, call[3], infered_type)
                    self.__add_to_list_of_tuples(inference_tuple)
        
        if len(self.list_of_inferences_tuples) != current_len_of_types:
            self.__recursive_step(len(self.list_of_inferences_tuples))
        
    
    def __find_inference(self, method, variable):
        all_inferences = []
        for inference in self.list_of_inferences_tuples:
            if inference[0] == method and inference[1] == variable:
                all_inferences.append(inference[2])
        return all_inferences

    def __add_to_list_of_tuples(self,inference):
        if not inference in self.list_of_inferences_tuples:
            self.list_of_inferences_tuples.append(inference)

    def __create_tuple_from_self(self, definition):
        file_class_function_key = self.__generate_function_name(definition)
        variable_name = definition.name
        inference = self.__find_current_class_name(definition)
        return (file_class_function_key, variable_name, inference)
    
    def __create_tuple_from_inference(self, definition, inference):
        file_class_function_key = self.__generate_function_name(definition)
        variable_name = definition.name
        inference = inference.name
        return (file_class_function_key, variable_name, inference)
    
    def __should_ignore_definition(self, inference, file):
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




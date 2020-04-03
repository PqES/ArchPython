import jedi
import sys
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
        self.list_of_tuples = []
    
    def run_jedi(self):
        #Lê os arquivos
        self.__search_project_folder()
        #Faz a inferência
        self.__make_inference()
    
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

            for definition in script_names:

                goto_teste = definition.goto(follow_imports=True, follow_builtin_imports=True)

                if (len(goto_teste) > 0):
                    for goto in goto_teste:
                        #Se chegar até aqui é pq tem uma chamada de função e devemos registrar isso 
                        if goto.type == "function":
                            print("TODO: Registrar chamada de função")
                    pass


                if not self.__should_ignore_definition(definition, file):
                    inferences = definition.infer()

                    #Pegar esse cara SOMENTE se ele for passado como parâmetro para um outra função
                    #Checa se é self. Essa função é "safe" pq self é uma palavra reservada
                    # if len(inferences) == 0 and definition.type == "statement" and definition.name == "self":
                    #     inference_tuple = self.__create_tuple_from_self(definition)
                    #     list_of_tuples.append(inference_tuple)
                    #     continue

                    file_name = definition.module_name
                    variable_name = definition.name
                    inference_key = definition.full_name if definition.full_name != None else definition.desc_with_module

                    self.inferences[inference_key] = Inference(file_name, variable_name, inference_key)

                    for inference in inferences:
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

    def __add_to_list_of_tuples(self,inference):
        if not inference in self.list_of_tuples:
            self.list_of_tuples.append(inference)

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


# if __name__ == "__main__":
#     project_root_folder = "/home/eduardol/UFLA/tcc/arquivos-arthur/dataset/sistema0"

#     for key in files:
#         file_dict = files[key]

#         # script_names = jedi.Script(path=file_dict['path']).get_names(all_scopes=True, definitions=True, references=True)
#         script_names = jedi.Script(path=file_dict['path']).get_names()


#         for definition in script_names:
#             inferences = definition.infer()
#             for inference in inferences:
#                 files[key]['types'].add(inference.name)

#             # inference = definition.infer()[0].name
#             # files[key]['types'].append(inference)
        

#     a = 2




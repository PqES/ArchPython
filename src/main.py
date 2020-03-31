#TODO: Refatorar esse código


import sys
import os
from Utils.input_reader import InputReader
from Utils.module_definition_loader import ModuleDefinitionLoader
from Jedi.skywalker import Skywalker

#TODO Remover essa função deste arquivo
def get_file_absolute_path(module_definition_json_path : str):
    current_path = os.path.dirname(os.path.realpath(__file__))
    goal_path = os.path.join(current_path, module_definition_json_path)
    file_absolute_path = os.path.abspath(goal_path)
    return file_absolute_path

#TODO Remover essa função deste arquivo
def read_module_definition_file(module_definition_json_path):
    module_definition_json_path = get_file_absolute_path(module_definition_json_path)

    file_content = InputReader.get_json_content(module_definition_json_path)
    module_definitions = ModuleDefinitionLoader.get_module_definitions(file_content)

    return module_definitions

#TODO Remover essa função deste arquivo
#TODO Renomear essa função
def read_project_folder(target_project_root_path):
    skywalker = Skywalker(target_project_root_path)
    skywalker.run_jedi()
    return skywalker.get_files()

#Função que cruza as informações do modulo com as inferencias realizadas
def cross_information(module_definitions, files):
    pass





if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise Exception("Invalid number of arguments")

    module_definition_file = sys.argv[1]
    target_project_root_path = sys.argv[2]
    
    module_definitions = read_module_definition_file(module_definition_file)
    files = read_project_folder(target_project_root_path)
    cross_information(module_definitions, files)
    
    

    # print(project_folder)


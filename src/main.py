import sys
import os
from Utils.input_reader import InputReader
from Utils.module_definition_loader import ModuleDefinitionLoader

def get_file_absolute_path(file_path : str):
    current_path = os.path.dirname(os.path.realpath(__file__))
    goal_path = os.path.join(current_path, file_path)
    file_absolute_path = os.path.abspath(goal_path)
    return file_absolute_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Invalid number of arguments")
    
    file_path = get_file_absolute_path(sys.argv[1])

    file_content = InputReader.get_json_content(file_path)
    module_definitions = ModuleDefinitionLoader.get_module_definitions(file_content)

    print(module_definitions)


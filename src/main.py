#TODO: Refatorar esse código

import sys
import os
import json
from Utils.input_reader import InputReader
from Utils.module_definition_loader import ModuleDefinitionLoader
from Jedi.skywalker import Skywalker
from Commons.conformity_checker import ConformityChecker
from Utils.vis_graph_creator_util import VisGraphCreatorUtil
from Utils.matrix_creator_util import MatrixCreatorUtil
from Commons.graphs_creators.module_graph_creator import ModuleGraphCreator
from Commons.graphs_creators.inference_graph_creator import InferenceGraphCreator
from Commons.graphs_creators.problem_graph_creator import ProblemGraphCreator
from Commons.graphs_creators.reflection_graph_creator import ReflectionGraphCreator
from Commons.problem_matrix_creator import ProblemMatrixCreator



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

    graph = ModuleGraphCreator(module_definitions).create_graph_from_module()

    VisGraphCreatorUtil.create_vis_graph(graph)


    return module_definitions

#TODO Remover essa função deste arquivo
#TODO Renomear essa função
def read_project_folder(target_project_root_path, module_definitions):
    skywalker = Skywalker(target_project_root_path)
    skywalker.set_modules(module_definitions)
    skywalker.run_jedi()

    inferences = skywalker.get_inferences()

    types_defined = skywalker.get_type_declarations()

    graph = InferenceGraphCreator(inferences).create_graph_from_inference()
    VisGraphCreatorUtil.create_vis_graph(graph)

    return [inferences, types_defined]

#Função que cruza as informações do modulo com as inferencias realizadas
def cross_information(module_definitions, inferences, types_declared):
    cc = ConformityChecker(module_definitions, inferences, types_declared)
    cc.check_conformity()

    problems = cc.get_problems()

    graph = ProblemGraphCreator(inferences, problems).create_graph_from_problems()
    VisGraphCreatorUtil.create_vis_graph(graph)

    matrix = ProblemMatrixCreator(inferences, problems, module_definitions).create_matrix()
    MatrixCreatorUtil.create_matrix_file(matrix)

    refletion_matrix = ReflectionGraphCreator(inferences, problems, module_definitions).create_graph()
    VisGraphCreatorUtil.create_vis_graph(refletion_matrix)
    pass

def write_files(files):
    json_dict = {}
    for file in files.values():
        json_dict[file.file_name] = list(file.types)
    
    with open('data.json', 'w') as output:
        json.dump(json_dict, output)





if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise Exception("Invalid number of arguments")

    module_definition_file = sys.argv[1]
    target_project_root_path = sys.argv[2]
    
    module_definitions = read_module_definition_file(module_definition_file)
    inferences, types_declared = read_project_folder(target_project_root_path, module_definitions)
    # write_files(files)
    cross_information(module_definitions, inferences, types_declared)    
    

    # print(project_folder)


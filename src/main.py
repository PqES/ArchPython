import sys
import os
import json
from datetime import datetime
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
from Commons.result_file_creator import ResultFileCreator
from Commons.new_conformity_checker import NewConformityChecker
from Commons.graphs_creators.new_reflection_graph_creator import NewReflectionGraphCreator
from Commons.textual_report_creator import TextualReportCreator
from Commons.dsm_creator import DSMCreator


def get_file_absolute_path(module_definition_json_path : str):
    current_path = os.path.dirname(os.path.realpath(__file__))
    goal_path = os.path.join(current_path, module_definition_json_path)
    file_absolute_path = os.path.abspath(goal_path)
    return file_absolute_path

def read_module_definition_file(module_definition_json_path, project_root_folder, result_project_name):
    module_definition_json_path = get_file_absolute_path(module_definition_json_path)

    file_content = InputReader.get_json_content(module_definition_json_path)
    module_definitions = ModuleDefinitionLoader.get_module_definitions(file_content, project_root_folder)

    graph = ModuleGraphCreator(module_definitions).create_graph_from_module()

    VisGraphCreatorUtil.create_vis_graph(graph, result_project_name)


    return module_definitions

def read_project_folder(target_project_root_path, module_definitions, result_project_name):
    skywalker = Skywalker(target_project_root_path, result_project_name)
    skywalker.set_modules(module_definitions)
    skywalker.run_jedi()

    inferences = skywalker.get_inferences()

    types_defined = skywalker.get_type_declarations()

    graph = InferenceGraphCreator(inferences).create_graph_from_inference()
    VisGraphCreatorUtil.create_vis_graph(graph, result_project_name)

    return [inferences, types_defined]

#Função que cruza as informações do modulo com as inferencias realizadas
def cross_information(module_definitions, inferences, result_project_name, report_conformity_warnings):

    ncc = NewConformityChecker(inferences, module_definitions).check_conformity()

    result_file_creator = ResultFileCreator(inferences, module_definitions, report_conformity_warnings)
    result_file_creator.create_json_file(result_project_name)

    refletion_graph = NewReflectionGraphCreator(ncc, module_definitions).create_graph()
    VisGraphCreatorUtil.create_vis_graph(refletion_graph, result_project_name, True)

    matrix = DSMCreator(ncc, module_definitions).create_matrix()
    MatrixCreatorUtil.create_matrix_file(matrix, result_project_name)



def get_result_project_name(project_path):
    list_directories = project_path.split("\\")

    if len(list_directories) == 1:
        list_directories = project_path.split("/")

    last_name = list_directories[-1]
    first_name = list_directories[-2]

    complete_name = f"{first_name}.{last_name}.{datetime.today().strftime('%Y-%m-%d')}.{datetime.now().strftime('%H-%M')}"
    return complete_name





if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise Exception("Invalid number of arguments")

    report_conformity_warnings = False

    if len(sys.argv) > 3:
        args_content = sys.argv[3]
        if args_content == "--report-conformity-warnings" or args_content == "-rcw":
            report_conformity_warnings = True
            print("Including warnings on JSON report")


    module_definition_file = sys.argv[1]
    target_project_root_path = sys.argv[2]

    result_project_name = get_result_project_name(target_project_root_path)
    module_definitions = read_module_definition_file(module_definition_file, target_project_root_path, result_project_name)
    inferences, types_declared = read_project_folder(target_project_root_path, module_definitions, result_project_name)
    cross_information(module_definitions, inferences, result_project_name, report_conformity_warnings)


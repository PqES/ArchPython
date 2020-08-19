import json
import os
import errno
from Enums.problems_enum import ProblemsEnum

class ResultFileCreator:

    def __init__(self, inferences, module_definitions, report_warnings):

        self.inferences = inferences
        self.module_definitions = module_definitions
        self.file_content = {ProblemsEnum.DIVERGENCE.name : [], ProblemsEnum.ABSENCE.name : [], ProblemsEnum.WARNING.name : []}

        self.report_warnings = report_warnings

        self.__file_inferences_dict = {}
        self.__modules_names_cache = set()

    def create_json_file(self, project_name):
        self.__create_file_inference_dict()
        self.__define_all_modules()
        self.find_divergences()
        self.find_abscences()

        if self.report_warnings:
            self.find_warnings()

        self.write_result(project_name)

    def write_result(self, project_name):

        file_path = f'./results/{project_name}/main/violation_report.json'
        if not os.path.exists(os.path.dirname(file_path)):
            try:
                os.makedirs(os.path.dirname(file_path))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

        with open(file_path, 'w') as output:
            json.dump(self.file_content, output)


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

    #TODO: Trocar o nome dessa função
    def __file_access_module(self, file, module):
        if file not in self.__file_inferences_dict.keys():
            return None
        inferences = self.__file_inferences_dict[file]
        for inference in inferences:
            if inference.inferred_module_name == module:
                return inference.line_no
        return None


    def find_abscences(self):
        for module in self.module_definitions:
            if module.required != None:
                for module_required in module.required:
                    for file in module.files:
                        if "__init__" in file:
                            continue
                        if self.__file_access_module(file, module_required) == None:
                            self.__report_abcense(module, file, module_required)

    def find_divergences(self):
        for module in self.module_definitions:
            if module.forbidden != None:
                for module_forbidden in module.forbidden:
                    for file in module.files:
                        if "__init__" in file:
                            continue
                        line_number = self.__file_access_module(file, module_forbidden)
                        if  line_number != None:
                            self.__report_divergence(module, file, module_forbidden, line_number)

    def __get_all_modules_allowed(self, module):
        all_modules_allowed = set()
        if module.allowed != None:
            all_modules_allowed = all_modules_allowed.union(module.allowed)

        if module.required != None:
            all_modules_allowed = all_modules_allowed.union(module.required)

        if module.forbidden != None:
            modules_allowed = self.__modules_names_cache.difference(module.forbidden)
            all_modules_allowed = all_modules_allowed.union(modules_allowed)

        if module.name in all_modules_allowed:
            all_modules_allowed.remove(module.name)

        return all_modules_allowed

    def __define_all_modules(self):
        all_modules = set()
        for module in self.module_definitions:
            all_modules.add(module.name)
        self.__modules_names_cache = set(all_modules)

    #Warning é quando um módulo permitido não é utilizado
    def find_warnings(self):
        for module in self.module_definitions:

            modules_allowed = self.__get_all_modules_allowed(module)

            if len(modules_allowed) > 0:
                for module_allowed in modules_allowed:

                    should_report_warning = True #Flag que garante que pelo menos um arquivo do módulo está usando o módulo permitido
                    for file in module.files:
                        if "__init__" in file:
                            continue

                        if self.__file_access_module(file, module_allowed) != None:
                            should_report_warning = False

                    if should_report_warning:
                        self.__report_warning(module, module_allowed)


    def __report_warning(self, module, module_allowed_name):
        problem_description = {
            'origin_module' : module.name,
            'origin_line': '',
            'origin_file_path' : '',
            'target_module' : module_allowed_name,
            'constraint' : ProblemsEnum.WARNING.value['Message'].format(module.name, module_allowed_name)
        }
        self.file_content[ProblemsEnum.WARNING.name].append(problem_description)

    def __report_abcense(self, module, file, module_required_name):
        problem_description = {
            'origin_module' : module.name,
            'origin_line': '',
            'origin_file_path' : file,
            'target_module' : module_required_name,
            'constraint' : ProblemsEnum.ABSENCE.value['Message'].format(module.name, module_required_name)
        }
        self.file_content[ProblemsEnum.ABSENCE.name].append(problem_description)

    def __report_divergence(self, module, file, module_not_allowed, line_number):
        problem_description = {
            'origin_module' : module.name,
            'origin_line': line_number,
            'origin_file_path' : file,
            'target_module' : module_not_allowed,
            'constraint' : ProblemsEnum.DIVERGENCE.value['Message'].format(module.name, module_not_allowed)
        }
        self.file_content[ProblemsEnum.DIVERGENCE.name].append(problem_description)

    def __report_problem(self, module, module_required_name, problem_enum):
        problem_description = {
            'origin_module' : module.name,
            'origin_class' : module.inference_fullname,
            'target_module' : module.inferred_module_name,
            'target_class' : '',
            'constraint' : problem_enum.value['message'].format(module.name, module_required_name)
        }
        self.file_content[problem_enum.name].append(problem_description)



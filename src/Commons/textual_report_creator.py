from Enums.conformity_status_enum import ConformityStatusEnum
from Enums.problems_enum import ProblemsEnum



class TextualReportCreator:

    def __init__(self, conformity_info, module_definitions):
        self.conformity_info = conformity_info
        self.module_definitions = module_definitions

        self.file_content = {}
        self.__get_problems()

    def __get_problems(self):
        for conformity in self.conformity_info:
            if conformity.status_enum == ConformityStatusEnum.DIVERGENCE:
                a = 2
            elif conformity.status_enum == ConformityStatusEnum.ABSCENSE:
                b = 2

    def __report_abcense(self, module, file, module_required_name):
        problem_description = {
            'origin_module' : module.name,
            'origin_line': '',
            'origin_file_path' : file,
            'target_module' : module_required_name,
            'constraint' : ProblemsEnum.ABSENCE.value['Message'].format(module.name, module_required_name)
        }
        self.file_content[ProblemsEnum.DIVERGENCE.name].append(problem_description)

    def __report_divergence(self, module, file, module_not_allowed, line_number):
        problem_description = {
            'origin_module' : module.name,
            'origin_line': line_number,
            'origin_file_path' : file,
            'target_module' : module_not_allowed,
            'constraint' : ProblemsEnum.DIVERGENCE.value['Message'].format(module.name, module_not_allowed)
        }
        self.file_content[ProblemsEnum.DIVERGENCE.name].append(problem_description)
    
    def write_report(self):
        a = 2
    

    

    
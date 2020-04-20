from Models.Visualization.Matrix.matrix import Matrix
from Models.Visualization.Matrix.matrix_cell import MatrixCell
from Enums.edge_status_enum import EdgeStatusEnum
from Enums.matrix_cell_status_enum import MatrixCellStatusEnum



class ProblemMatrixCreator:

    def __init__(self, inferences, problems, module_definitions):
        self.inferences = inferences
        self.problems = problems
        self.module_definitions = module_definitions

        self.__problems_cache = {}
        self.__modules_usage = {}

        self.matrix = Matrix("Problem Matrix")

    # def construct_problems_cache(self):
    #     for problem in self.problems:
    #         for restriction_broken in problem.restrictions_broken:
    #             tuple_key = (problem.origin_module.name, restriction_broken)
    #             self.__problems_cache[tuple_key] = problem
    
    def create_matrix(self):
        # self.construct_problems_cache()
        self.__define_all_modules()
        self.__create_empty_matrix()
        self.__calculate_modules_usage()
        self.__define_relationships()

        return self.matrix
    
    def __create_empty_matrix(self):
        all_modules = self.matrix.all_modules

        for module1 in all_modules:
            for module2 in all_modules:
                cell = MatrixCell(module1, module2, MatrixCellStatusEnum.EMPTY)
                self.matrix.add_cell(cell)

    
    def __define_relationships(self):
        self._define_allowed_relationships()
        self._define_divergence_relationships()
        self._define_abscence_relationships()
        self._define_warning_relationships()
    
    def _define_allowed_relationships(self):
        for module in self.module_definitions:
            if module.allowed != None:
                for module_allowed in module.allowed:
                    origin_module = module.name

                    if self.__module_use_module(origin_module, module_allowed):
                        self.matrix.edit_cell_status(origin_module, module_allowed, MatrixCellStatusEnum.WARNING)
                        cell_key = (origin_module, module_allowed)
                        self.matrix.edit_cell_content(origin_module, module_allowed, self.__modules_usage[cell_key])
    
    def _define_divergence_relationships(self):
        for module in self.module_definitions:
            if module.forbidden != None:
                for module_forbidden in module.forbidden:
                    origin_module = module.name

                    if self.__module_use_module(origin_module, module_forbidden):
                        self.matrix.edit_cell_status(origin_module, module_forbidden, MatrixCellStatusEnum.DIVERGENCE)
                        cell_key = (origin_module, module_forbidden)
                        self.matrix.edit_cell_content(origin_module, module_forbidden, self.__modules_usage[cell_key])
    
    def _define_abscence_relationships(self):
        for module in self.module_definitions:
            if module.required != None:
                for module_required in module.required:
                    origin_module = module.name

                    if not self.__module_use_module(origin_module, module_required):
                        self.matrix.edit_cell_status(origin_module, module_required, MatrixCellStatusEnum.ABSCENCE)
                        self.matrix.edit_cell_content(origin_module, module_required, 0)
    
    def _define_warning_relationships(self):
        for module in self.module_definitions:
            if module.allowed != None:
                for module_allowed in module.allowed:
                    origin_module = module.name

                    if not self.__module_use_module(origin_module, module_allowed):
                        self.matrix.edit_cell_status(origin_module, module_allowed, MatrixCellStatusEnum.WARNING)
                        self.matrix.edit_cell_content(origin_module, module_allowed, "?")

    def __module_use_module(self, module1, module2):
        for inference in self.inferences:
            if inference.origin_module == module1 and inference.inferred_module_name == module2:
                return True
        return False
    
    def __define_all_modules(self):
        all_modules = set()
        for module in self.module_definitions:
            all_modules.add(module.name)
        modules_list = list(all_modules)
        modules_list.sort()
        self.matrix.all_modules = modules_list
    
    def __calculate_modules_usage(self):
        for inference in self.inferences:
            key = (inference.origin_module, inference.inferred_module_name)
            if key in self.__modules_usage.keys():
                self.__modules_usage[key] += 1
            else:
                self.__modules_usage[key] = 1

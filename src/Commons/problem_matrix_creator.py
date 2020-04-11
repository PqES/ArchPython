from Models.Visualization.Matrix.matrix import Matrix
from Models.Visualization.Matrix.matrix_cell import MatrixCell
from Enums.edge_status_enum import EdgeStatusEnum
from Enums.matrix_cell_status_enum import MatrixCellStatusEnum



class ProblemMatrixCreator:

    def __init__(self, inferences, problems):
        self.inferences = inferences
        self.problems = problems

        self.__problems_cache = {}

        self.matrix = Matrix("Problem Matrix")

    def construct_problems_cache(self):
        for problem in self.problems:
            for restriction_broken in problem.restrictions_broken:
                tuple_key = (problem.origin_module.name, restriction_broken)
                self.__problems_cache[tuple_key] = problem
    
    def create_matrix(self):
        self.construct_problems_cache()
        self.__define_all_modules()
        self.__define_relationships()

        return self.matrix
    
    def __define_relationships(self):
        all_modules = self.matrix.all_modules
        for module1 in all_modules:
            for module2 in all_modules:
                tuple_key = (module1, module2)
                problem = None
                try :
                    problem = self.__problems_cache[tuple_key]
                except:
                    problem = None
                
                if problem != None:
                    for restriction_broken in problem.restrictions_broken:
                        if problem.category == "problem":
                            cell = MatrixCell(problem.origin_module.name, restriction_broken, MatrixCellStatusEnum.ERROR_RESTRICTION)
                            self.matrix.add_cell(cell)
                        else:
                            cell = MatrixCell(problem.origin_module.name, restriction_broken, MatrixCellStatusEnum.WARNING_RESTRICTION)
                            self.matrix.add_cell(cell)

                elif self.__module_use_module(module1, module2):
                    cell = MatrixCell(module1, module2, MatrixCellStatusEnum.ALLOWED)
                    self.matrix.add_cell(cell)
                else:
                    cell = MatrixCell(module1, module2, MatrixCellStatusEnum.EMPTY)
                    self.matrix.add_cell(cell)


    def __module_use_module(self, module1, module2):
        for inference in self.inferences:
            if inference.origin_module == module1 and inference.inferred_module_name == module2:
                return True
        return False
        
    def __define_all_modules(self):
        all_modules = set()
        for inference in self.inferences:
            all_modules.add(inference.origin_module)
        self.matrix.all_modules = list(all_modules)

from Models.Visualization.Matrix.matrix import Matrix
from Models.Visualization.Matrix.matrix_cell import MatrixCell
from Enums.edge_status_enum import EdgeStatusEnum
from Enums.matrix_cell_status_enum import MatrixCellStatusEnum



class DSMCreator:

    def __init__(self, conformity_info, module_definitions):
        self.__module_definitions = module_definitions
        self.__conformity_info = conformity_info

        self.matrix = Matrix("DSM")

    def create_matrix(self):
        self.__define_all_modules()
        self.__create_empty_matrix()
        self.__define_relationships()

        return self.matrix
    
    def __define_all_modules(self):
        all_modules = set()
        packages = set()
        for module in self.__module_definitions:
            if module.packages != None and len(module.packages):
                packages.add(module.name)
            all_modules.add(module.name)
        modules_list = list(all_modules)
        modules_list.sort()
        self.matrix.all_modules = modules_list
        self.matrix.all_packages = list(packages)
        self.__modules_names_cache = set(all_modules)

    
    def __create_empty_matrix(self):
        for module1 in self.__module_definitions:
            for module2 in self.__module_definitions:
                cell = MatrixCell(module1.name, module2.name, MatrixCellStatusEnum.EMPTY.value)
                self.matrix.add_cell(cell)

    
    def __define_relationships(self):
        for conformity in self.__conformity_info:

            origin_module = conformity.module_origin
            final_module = conformity.module_destination
            status = conformity.status_enum.value['MatrixEnum']
            
            self.matrix.edit_cell_status(origin_module, final_module, status)
            cell_content = "?" if conformity.usage == 0 else conformity.usage
            self.matrix.edit_cell_content(origin_module, final_module, cell_content)
    
  
                
            
            # if module.required != None:
            #     for module_required in module.required:
            #         origin_module = module.name

            #         if self.__module_use_module(origin_module, module_required):
            #             self.matrix.edit_cell_status(origin_module, module_required, MatrixCellStatusEnum.ALLOWED)
            #             cell_key = (origin_module, module_required)
            #             self.matrix.edit_cell_content(origin_module, module_required, self.__modules_usage[cell_key])
            
            # if module.forbidden != None:
            #     all_modules_allowed = self.__get_all_modules_allowed(module)
            #     for module_required in module.required:
            #         origin_module = module.name

            #         if self.__module_use_module(origin_module, module_required):
            #             self.matrix.edit_cell_status(origin_module, module_required, MatrixCellStatusEnum.ALLOWED)
            #             cell_key = (origin_module, module_required)
            #             self.matrix.edit_cell_content(origin_module, module_required, self.__modules_usage[cell_key])
            
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
    
    
    def _define_divergence_relationships(self):
        self.__forbidden_modules_beign_used()
        # self.__not_explicity_allowed_methods_beign_used()
    
    def __not_explicity_allowed_methods_beign_used(self):
        for inference in self.inferences:
            origin_module = inference.origin_module 
            inferred_module_name = inference.inferred_module_name

            if origin_module == inferred_module_name:
                continue

            if not self.__module_is_explicity_allowed(origin_module, inferred_module_name):
                self.matrix.edit_cell_status(origin_module, inferred_module_name, MatrixCellStatusEnum.DIVERGENCE)
                cell_key = (origin_module, inferred_module_name)
                self.matrix.edit_cell_content(origin_module, inferred_module_name, self.__modules_usage[cell_key])
    
    def __module_is_explicity_allowed(self, origin_module, inferred_module_name):
        for module in self.module_definitions:
            if module.name == origin_module:
                # not self.__module_in_forbidden(module, inferred_module_name) and
                if (not self.__module_in_required(module, inferred_module_name) and
                    not self.__module_in_allowed(module, inferred_module_name)):
                    return False
        return True
    
    def __module_in_forbidden(self, module, inferred_module_name):
        if module.forbidden != None and len(module.forbidden) > 0:
            if inferred_module_name in module.forbidden:
                return True
        return False
    
    def __module_in_required(self, module, inferred_module_name):
        if module.required != None and len(module.required) > 0:
            if inferred_module_name in module.required:
                return True
        return False
    
    def __module_in_allowed(self, module, inferred_module_name):
        if module.allowed != None and len(module.allowed) > 0:
            if inferred_module_name in module.allowed:
                return True
        return False


    def __forbidden_modules_beign_used(self):
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
                file_dont_use_a_module = False
                for module_required in module.required:

                    use_count = 0

                    if file_dont_use_a_module:
                        return

                    for file in module.files:
                        if not self.__file_access_module(file, module_required):
                            file_dont_use_a_module = True
                        else:
                            use_count += 1
                    
                    if file_dont_use_a_module:
                        origin_module = module.name
                        self.matrix.edit_cell_status(origin_module, module_required, MatrixCellStatusEnum.ABSCENCE)
                        self.matrix.edit_cell_content(origin_module, module_required, use_count)

                  
                    # origin_module = module.name

                    # if not self.__module_use_module(origin_module, module_required):
                    #     self.matrix.edit_cell_status(origin_module, module_required, MatrixCellStatusEnum.ABSCENCE)
                    #     self.matrix.edit_cell_content(origin_module, module_required, 0)
    
    def __file_access_module(self, file, module):
        if "__init__" in file:
            return True
        
        if file not in self.__file_inferences_dict.keys():
            return False
             
        inferences = self.__file_inferences_dict[file]
        for inference in inferences:
            if inference.inferred_module_name == module:
                return True
        return False
    
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
    
    
    
    def __calculate_modules_usage(self):
        for inference in self.inferences:
            key = (inference.origin_module, inference.inferred_module_name)
            if key in self.__modules_usage.keys():
                self.__modules_usage[key] += 1
            else:
                self.__modules_usage[key] = 1

import sys
import os
import glob
from Models.module import Module
from Enums.module_definition_error_enum import ModuleDefinitionErrorEnum
from Enums.module_definition_enum import ModuleDefinitionEnum


class ModuleDefinitionLoader(object):

    @staticmethod
    def get_module_definitions(file_content, project_root_folder, report_input_warnings):
        module_definitions = []
        for module in file_content:
            try:
                ModuleDefinitionLoader.__check_for_errors(file_content, module)
            except Exception as e:
                print(f"An exception was raised for {module} : {str(e)}")
                sys.exit(1)

            module = ModuleDefinitionLoader.__create_module(file_content, module, project_root_folder, report_input_warnings)
            module_definitions.append(module)
        module_definitions = ModuleDefinitionLoader.__assign_restriction_files(module_definitions)
        return module_definitions
    
    @staticmethod
    def __assign_restriction_files(module_definitions):
        modified_modules = []

        module_cache = ModuleDefinitionLoader.__create_module_by_name_cache(module_definitions)

        for module in module_definitions:
            if module.allowed != None:
                module.allowed_file_paths = ModuleDefinitionLoader.__get_set_of_paths_from_module(module.allowed, module_cache)
            
            if module.forbidden != None:
                module.forbidden_file_paths = ModuleDefinitionLoader.__get_set_of_paths_from_module(module.forbidden, module_cache)
            
            if module.required != None:
                module.required_file_file_paths = ModuleDefinitionLoader.__get_set_of_paths_from_module(module.required, module_cache)
            
            modified_modules.append(module)
            
        return modified_modules

    @staticmethod
    def __get_set_of_paths_from_module(list_of_modules, module_cache):
        set_of_paths = set()
        for module in list_of_modules:
            module_searched = module_cache[module]
            for path in module_searched.files:
                paths = set(glob.glob(path))
                set_of_paths = set_of_paths.union(paths)
        return set_of_paths
    
    @staticmethod
    def __create_module_by_name_cache(module_definitions):
        cache = {}
        for module in module_definitions:
            cache[module.name] = module
        return cache


    @staticmethod
    def __try_get_value_from_module(file_content, module, key, project_root_folder = ""):
        if key == ModuleDefinitionEnum.FILES_KEYWORD.value:
            return ModuleDefinitionLoader.__process_file_paths(file_content, module, key, project_root_folder)
        try:
            return file_content[module][key]
        except KeyError:
            return None
    
    @staticmethod
    def __process_file_paths(file_content, module, key, project_root_folder):
        current_path = project_root_folder
        if key in file_content[module].keys():
            files = file_content[module][key]
            complete_paths = []
            for file_path in files:
                if file_path[:2] == ".\\":
                    file_path = file_path[2:]
                complete_path = os.path.join(current_path,file_path)
                if "*" in complete_path:
                    all_paths = glob.glob(complete_path)
                    complete_paths.extend(all_paths)
                elif os.path.isfile(complete_path):
                    complete_paths.append(complete_path)
                else :
                    raise Exception(ModuleDefinitionErrorEnum.FILE_DOESNT_EXIST.value + ": " + complete_path)
            return complete_paths
        return []
    
    @staticmethod
    def __create_module(file_content, module, project_root_folder, report_input_warnings = False):
        name = module
        package = ModuleDefinitionLoader.__try_get_value_from_module(file_content, module, ModuleDefinitionEnum.PACKAGE_KEYWORD.value)
        # ModuleDefinitionLoader.__check_if_keyword_is_missing(module, package, ModuleDefinitionEnum.PACKAGE_KEYWORD.value, report_input_warnings)

        files = ModuleDefinitionLoader.__try_get_value_from_module(file_content, module, ModuleDefinitionEnum.FILES_KEYWORD.value, project_root_folder)
        # ModuleDefinitionLoader.__check_if_keyword_is_missing(module, files, ModuleDefinitionEnum.FILES_KEYWORD.value, report_input_warnings)

        allowed = ModuleDefinitionLoader.__try_get_value_from_module(file_content, module, ModuleDefinitionEnum.ALLOWED_KEYWORD.value)
        ModuleDefinitionLoader.__check_if_keyword_is_missing(module, allowed, ModuleDefinitionEnum.ALLOWED_KEYWORD.value, report_input_warnings)

        forbidden = ModuleDefinitionLoader.__try_get_value_from_module(file_content, module, ModuleDefinitionEnum.FORBIDDEN_KEYWORD.value)
        ModuleDefinitionLoader.__check_if_keyword_is_missing(module, forbidden, ModuleDefinitionEnum.FORBIDDEN_KEYWORD.value, report_input_warnings)

        if allowed == None and forbidden == None:
            ModuleDefinitionLoader.__check_if_keyword_is_missing(module, forbidden, ModuleDefinitionEnum.FORBIDDEN_KEYWORD.value, report_input_warnings)
            ModuleDefinitionLoader.__check_if_keyword_is_missing(module, allowed, ModuleDefinitionEnum.ALLOWED_KEYWORD.value, report_input_warnings)
        
        required = ModuleDefinitionLoader.__try_get_value_from_module(file_content, module, ModuleDefinitionEnum.REQUIRED_KEYWORD.value)
        ModuleDefinitionLoader.__check_if_keyword_is_missing(module, required, ModuleDefinitionEnum.REQUIRED_KEYWORD.value, report_input_warnings)


        return Module(name, package, files, allowed, forbidden, required)

    @staticmethod
    def __check_if_keyword_is_missing(module_name, module_value, keyword, report_input_warnings):
        if report_input_warnings and module_value == None:
            print(f"Warning: Module {module_name} does not have a {keyword} definition")

    @staticmethod
    def __check_for_errors(file_content, current_key):

        module_restrictions = file_content[current_key]

        if ModuleDefinitionEnum.FILES_KEYWORD.value in module_restrictions and ModuleDefinitionEnum.PACKAGE_KEYWORD.value in module_restrictions:
            raise Exception(ModuleDefinitionErrorEnum.FILES_AND_PACKAGE_USED.value)

        if ModuleDefinitionEnum.FILES_KEYWORD.value not in module_restrictions and ModuleDefinitionEnum.PACKAGE_KEYWORD.value not in module_restrictions:
            raise Exception(ModuleDefinitionErrorEnum.FILES_AND_PACKAGE_NOT_DEFINED.value)

        if ModuleDefinitionEnum.ALLOWED_KEYWORD.value in module_restrictions and ModuleDefinitionEnum.FORBIDDEN_KEYWORD.value in module_restrictions:
            raise Exception(ModuleDefinitionErrorEnum.ALLOWED_AND_FORBIDDEN_DEFINED.value)

        if ModuleDefinitionEnum.PACKAGE_KEYWORD.value in module_restrictions and len(module_restrictions) > 1:
            raise Exception(ModuleDefinitionErrorEnum.PACKAGE_WITH_RESTRICTIONS.value)

        
            
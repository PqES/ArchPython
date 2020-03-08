import sys
from Models.module import Module
from Enums.module_definition_error_enum import ModuleDefinitionErrorEnum
from Enums.module_definition_enum import ModuleDefinitionEnum


class ModuleDefinitionLoader(object):

    @staticmethod
    def get_module_definitions(file_content):
        module_definitions = []
        for module in file_content:
            try:
                ModuleDefinitionLoader.__check_for_errors(file_content, module)
            except Exception as e:
                print(f"An exception was raised for {module} : {str(e)}")
                sys.exit(1)

            module = ModuleDefinitionLoader.__create_module(file_content, module)
            module_definitions.append(module)
        return module_definitions

    @staticmethod
    def __try_get_value_from_module(file_content, module, key):
        try:
            return file_content[module][key]
        except KeyError:
            return None

    
    @staticmethod
    def __create_module(file_content, module):
        name = module
        package = ModuleDefinitionLoader.__try_get_value_from_module(file_content, module, ModuleDefinitionEnum.PACKAGE_KEYWORD.value)
        files = ModuleDefinitionLoader.__try_get_value_from_module(file_content, module, ModuleDefinitionEnum.FILES_KEYWORD.value)
        allowed = ModuleDefinitionLoader.__try_get_value_from_module(file_content, module, ModuleDefinitionEnum.ALLOWED_KEYWORD.value)
        forbidden = ModuleDefinitionLoader.__try_get_value_from_module(file_content, module, ModuleDefinitionEnum.FORBIDDEN_KEYWORD.value)
        required = ModuleDefinitionLoader.__try_get_value_from_module(file_content, module, ModuleDefinitionEnum.REQUIRED_KEYWORD.value)
        return Module(name, package, files, allowed, forbidden, required)



    
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

        
            
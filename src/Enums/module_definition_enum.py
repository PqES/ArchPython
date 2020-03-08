from enum import Enum

class ModuleDefinitionEnum(Enum):

    PACKAGE_KEYWORD = "package"
    FILES_KEYWORD = "files"
    REQUIRED_KEYWORD = "required"
    ALLOWED_KEYWORD = "allowed"
    FORBIDDEN_KEYWORD = "forbidden"
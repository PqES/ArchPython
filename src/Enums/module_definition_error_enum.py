from enum import Enum

class ModuleDefinitionErrorEnum(Enum):

    FILES_AND_PACKAGE_NOT_DEFINED = "Both files and package wasn't defined"
    FILES_AND_PACKAGE_USED = "Can't use files and package at same time"
    ALLOWED_AND_FORBIDDEN_DEFINED = "Can't define allowed and forbidden for the same module"
    PACKAGE_WITH_RESTRICTIONS = "A package can't have restrictions"

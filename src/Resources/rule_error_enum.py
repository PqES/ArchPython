from enum import Enum

class RuleErrorEnum(Enum):

    NAME_MODULE_NONE = "Name and Module cannot be None at same time"
    NAME_MODULE_USED = "Can't use Name and Module at same time"

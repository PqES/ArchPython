from Resources.rule_error_enum import RuleErrorEnum
from Models.restrictions import Restrictions


class Rule:

    def __init__(self, name : str, restrictions : list, files=None ,module=None):
        
        if files == None and module == None:
            raise Exception(RuleErrorEnum.NAME_MODULE_NONE.value)

        if module != None and files != None:
            raise Exception(RuleErrorEnum.NAME_MODULE_USED.value)

        self.name = name
        self.restrictions = Restrictions(restrictions)
        self.files = files if module == None else None
        self.module = module if files == None else None


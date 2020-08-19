from enum import Enum

class ProblemsEnum(Enum):

    FORBIDDEN_RESTRICTION_BROKEN = {
        "Code" : "FORBIDDEN_RESTRICTION_BROKEN",
        "Message" : "A forbidden restriction was used"
    }

    ALLOWED_RESTRICTION_BROKEN = {
        "Code" : "ALLOWED_RESTRICTION_BROKEN",
        "Message" : "A restriction not explicitly allowed and not explicitly required was used"
    }

    REQUIRED_RESTRICTION_BROKEN = {
        "Code" : "REQUIRED_RESTRICTION_BROKEN",
        "Message" : "A mandatory restriction was not used"
    }

    WARNING = {
        "Code" : "WARNING",
        "Message" : "Module {} does not use the allowed module {}"
    }


    DIVERGENCE = {
        "Code" : "DIVERGENCE",
        "Message" : "Module {} cannot depend on module {}."
    }

    ABSENCE = {
        "Code" : "ABSENCE",
        "Message" : "Module {} does not implement the required module {}."
    }

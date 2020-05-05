from enum import Enum

class EdgeStatusEnum(Enum):

    ALLOWED = {
        "Code" : "Allowed",
        "Color" : "black",
        "Dashes": False,
        'Width' : 1
    }

    FORBIDDEN_OR_NOT_EXPLICITY_ALLOWED = {
        "Code" : "ForbiddenOrNotExplicityAllowed",
        "Color" : "orange",
        "Dashes": True,
        'Width' : 1
    }
    
    REQUIRED_NOT_USED = {
        "Code" : "RequiredNotUsed",
        "Color" : "red",
        "Dashes": True,
        'Width' : 1
    }

    ALLOWED_NOT_USED = {
        "Code" : "AllowedNotUsed",
        "Color" : "#bfbfbf",
        "Dashes": False,
        'Width' : 1
    }

    UNDEFINED = {
        "Code" : "AllowedNotUsed",
        "Color" : "pink",
        "Dashes": False,
        'Width' : 1
    }


    #Seta grossa
    MODULE_REQUIRED = {
        "Code" : "Required",
        "Color" : "black", #Preto claro
        "Dashes": False,
        'Width' : 4
    }

    #Seta fina
    MODULE_ALLOWED = {
        "Code" : "Allowed",
        "Color" : "#2e2e2e",
        "Dashes": False,
        'Width' : 0.8
    }


    ######################

    #Compatibility, should remove soon
    ERROR_RESTRICTION = {
        "Code" : "Error Restriction",
        "Color" : "red",
        'Width' : 1
    }

    WARNING_RESTRICTION = {
        "Code" : "Error Restriction",
        "Color" : "#bad10a",
        'Width' : 1
    }

    FORBIDDEN = {
        "Code" : "forbidden",
        "Color" : "red",
        'Width' : 1
    }




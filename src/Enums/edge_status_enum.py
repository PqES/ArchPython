from enum import Enum

class EdgeStatusEnum(Enum):

    ALLOWED = {
        "Code" : "Allowed",
        "Color" : "black",
        "Dashes": False
    }

    FORBIDDEN = {
        "Code" : "Forbidden",
        "Color" : "orange",
        "Dashes": True
    }

    
    REQUIRED_NOT_USED = {
        "Code" : "RequiredNotUsed",
        "Color" : "red",
        "Dashes": True
    }

    ALLOWED_NOT_USED = {
        "Code" : "AllowedNotUsed",
        "Color" : "gray",
        "Dashes": False
    }

    UNDEFINED = {
        "Code" : "AllowedNotUsed",
        "Color" : "pink",
        "Dashes": False
    }

    #Compatibility, should remove soon
    REQUIRED = {
        "Code" : "Required",
        "Color" : "blue",
        "Dashes": False
    }

    ERROR_RESTRICTION = {
        "Code" : "Error Restriction",
        "Color" : "red"
    }

    WARNING_RESTRICTION = {
        "Code" : "Error Restriction",
        "Color" : "#bad10a"
    }




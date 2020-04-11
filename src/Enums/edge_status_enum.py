from enum import Enum

class EdgeStatusEnum(Enum):

    ALLOWED = {
        "Code" : "Allowed",
        "Color" : "green"
    }

    FORBIDDEN = {
        "Code" : "Forbidden",
        "Color" : "red"
    }

    REQUIRED = {
        "Code" : "Required",
        "Color" : "blue"
    }

    ERROR_RESTRICTION = {
        "Code" : "Error Restriction",
        "Color" : "red"
    }

    WARNING_RESTRICTION = {
        "Code" : "Error Restriction",
        "Color" : "#bad10a"
    }


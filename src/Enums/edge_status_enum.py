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
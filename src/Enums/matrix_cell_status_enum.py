from enum import Enum

class MatrixCellStatusEnum(Enum):

    ALLOWED = {
        "Code" : "Allowed",
        "Color" : "green"
    }

    ERROR_RESTRICTION = {
        "Code" : "Error Restriction",
        "Color" : "red"
    }

    WARNING_RESTRICTION = {
        "Code" : "Error Restriction",
        "Color" : "yellow"
    }

    EMPTY = {
        "Code" : "empty",
        "Color" : "white"
    }


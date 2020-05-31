from enum import Enum

class MatrixCellStatusEnum(Enum):

    ABSCENCE = {
        "Code" : "Abscence",
        "Color" : "red"
    }

    DIVERGENCE = {
        "Code" : "Divergence",
        "Color" : "orange"
    }

    WARNING = {
        "Code" : "Warning",
        "Color" : "#b3b3b3"
    }

    ALLOWED = {
        "Code" : "ALLOWED",
        "Color" : "#eaeaea"
    }

    EMPTY = {
        "Code" : "empty",
        "Color" : "white"
    }


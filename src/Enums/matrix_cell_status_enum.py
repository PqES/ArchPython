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
        "Color" : "gray"
    }


    EMPTY = {
        "Code" : "empty",
        "Color" : "white"
    }


from enum import Enum

from Enums.edge_status_enum import EdgeStatusEnum
from Enums.matrix_cell_status_enum import MatrixCellStatusEnum

class ConformityStatusEnum(Enum):

    ALLOWED = {
        "Code" : "ALLOWED",
        "MatrixEnum" : MatrixCellStatusEnum.ALLOWED.value,
        "GraphEnum" : EdgeStatusEnum.ALLOWED.value,
    }

    DIVERGENCE = {
        "Code" : "DIVERGENCE",
        "MatrixEnum" : MatrixCellStatusEnum.DIVERGENCE.value,
        "GraphEnum" : EdgeStatusEnum.FORBIDDEN_OR_NOT_EXPLICITY_ALLOWED.value,
    }

    ABSCENSE = {
        "Code" : "ABSCENSE",
        "MatrixEnum" : MatrixCellStatusEnum.ABSCENCE.value,
        "GraphEnum" : EdgeStatusEnum.REQUIRED_NOT_USED.value,
    }

    WARNING = {
        "Code" : "WARNING",
        "MatrixEnum" : MatrixCellStatusEnum.WARNING.value,
        "GraphEnum" : EdgeStatusEnum.ALLOWED_NOT_USED.value,
    }

 




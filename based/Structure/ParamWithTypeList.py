from typing import NamedTuple

from based.Structure.Node import Node
from based.Structure.ReturnType import ReturnType
from based.Structure.Variable import Variable

class VariableTypePair(NamedTuple):
    var: Variable
    type: ReturnType
    def __repr__(self) -> str:
        return f'{self.type} {self.var.name}'

class ParamWithTypeList(Node):
    def __init__(self, variables: list[VariableTypePair]):
        self.variables = variables

    def __str__(self) -> str:
        res = ", ".join([str(var) for var in self.variables])
        return res

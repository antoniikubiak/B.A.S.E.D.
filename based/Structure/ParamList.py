from typing import NamedTuple, override

from based.Structure.Node import Node
from based.Structure.ReturnType import ReturnType
from based.Structure.Expressions.Variable import Variable

class VariableTypePair(NamedTuple):
    var: Variable
    type: ReturnType
    def __str__(self) -> str:
        return f'{self.type} {self.var.name}'

class ParamWithTypeList(Node):
    def __init__(self, variables: list[VariableTypePair]):
        self.variables = variables

    @override
    def __str__(self) -> str:
        res = ", ".join([str(var) for var in self.variables])
        return res

    def __len__(self) -> int:
        return len(self.variables)

    def __getitem__(self, idx: int) -> VariableTypePair:
        return self.variables[idx]

class ParamWithoutTypeList(Node):
    def __init__(self, variables: list[Variable]):
        self.variables = variables

    def __len__(self) -> int:
        return len(self.variables)

    @override
    def __str__(self) -> str:
        res = ", ".join([str(var) for var in self.variables])
        return res

    def __getitem__(self, idx: int) -> Variable:
        return self.variables[idx]

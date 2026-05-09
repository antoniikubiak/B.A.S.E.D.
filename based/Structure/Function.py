from based.Structure.Expression import Expression
from based.Structure.Node import Node
from based.Structure.ParamWithTypeList import ParamWithTypeList
from based.Structure.ReturnType import ReturnType


class Function(Node):
    def __init__(self, name: str, params: ParamWithTypeList, returns: ReturnType, body: Expression):
        self.name = name
        self.params = params
        self.returns = returns
        self.body = body
    def __repr__(self) -> str:
        return f'{self.returns} {self.name}({self.params}) := {self.body}'

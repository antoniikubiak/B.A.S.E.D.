from based.Structure.Expression import Expression
from based.Structure.Node import Node
from based.Structure.ParamWithTypeList import ParamWithTypeList
from based.Structure.ReturnType import ReturnType


class Function(Node):
    """
    Represents a function definition, including its signature and body.
    """
    def __init__(self, name: str, params: ParamWithTypeList, returns: ReturnType, body: Expression):
        """
        Initializes a Function object.
        :param name: Identifier for the function.
        :param params: List of typed parameters.
        :param returns: The expected return type.
        :param body: The expression evaluating the function's logic.
        """
        self.name = name
        self.params = params
        self.returns = returns
        self.body = body
    def __repr__(self) -> str:
        return f'{self.returns} {self.name}({self.params}) := {self.body}'

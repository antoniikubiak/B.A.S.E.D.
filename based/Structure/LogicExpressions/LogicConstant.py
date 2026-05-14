from typing import override

from based.Structure.Constant import Constant
from based.Structure.LogicExpressions.LogicExpression import LogicExpression


class LogicConstant(LogicExpression, Constant):
    def __init__(self, value: str | bool, *args, **kwargs) -> None:
        super().__init__(value, *args, **kwargs)
        if isinstance(self.value, bool):
            self.value = self.value
        if isinstance(self.value, str):
            if value == 'true':
                self.value = True
            elif value == 'false':
                self.value = False
            else:
                raise TypeError(f"Logic constant cannot be initialized with value of type {type(value)}")

    @override
    def simplify(self) -> LogicExpression:
        return self

    @override
    def __invert__(self) -> LogicExpression:
        return LogicConstant.create(not self.value)

    @override
    def __and__(self, other: LogicExpression) -> LogicExpression:
        if self.value:
            return other
        return self

    @override
    def __or__(self, other: LogicExpression) -> LogicExpression:
        if self.value:
            return self
        return other

    @override
    def __eq__(self, other: LogicExpression) -> bool:
        if isinstance(other, LogicConstant):
            return self.value == other.value
        return False

    def __repr__(self) -> str:
        return "true" if self.value else "false"

from typing import override

from based.Structure.Constant import Constant
from based.Structure.Expressions.SortPriority import SortPriority
from based.Structure.LogicExpressions.LogicExpression import LogicExpression


class LogicConstant(LogicExpression, Constant):
    @override
    def evaluate(self, var: 'Variable', val: 'EvaluableConstant') -> LogicExpression:
        return self

    def __hash__(self) -> int:
        return hash(self.value)

    def sort_key(self) -> tuple[SortPriority, str | int, tuple]:
        return SortPriority.CONSTANT, "CONST", (self.value, )

    def __init__(self, value: str | bool, *args, **kwargs) -> None:
        super().__init__(value, *args, **kwargs)
        if isinstance(value, bool):
            self.value = value
        elif isinstance(value, str):
            if value == 'true':
                self.value = True
            elif value == 'false':
                self.value = False
            else:
                raise TypeError(f"Logic constant cannot be initialized with value string '{value}'")
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

    @override
    def __str__(self) -> str:
        return "1" if self.value else "0"

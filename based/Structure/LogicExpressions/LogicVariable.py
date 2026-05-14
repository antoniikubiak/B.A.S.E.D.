from typing import override

from based.Structure.Expressions.SortPriority import SortPriority
from based.Structure.LogicExpressions.LogicExpression import LogicExpression


class LogicVariable(LogicExpression):
    def __invert__(self) -> LogicExpression:
        pass

    def __and__(self, other: LogicExpression) -> LogicExpression:
        pass

    def __or__(self, other: LogicExpression) -> LogicExpression:
        pass

    @override
    def sort_key(self) -> tuple[SortPriority, str, tuple]:
        return SortPriority.VARIABLE, self.name, ()

    @override
    def __hash__(self) -> int:
        return hash(self.name)

    @override
    def __eq__(self, other: LogicExpression) -> bool:
        if isinstance(other, LogicVariable):
            return self.name == other.name
        return False

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    @override
    def simplify(self) -> LogicExpression:
        return self

    def __repr__(self) -> str:
        return self.name

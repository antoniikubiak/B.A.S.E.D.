from typing import override

from based.Structure.Expressions.SortPriority import SortPriority
from based.Structure.LogicExpressions.LogicExpression import LogicExpression
from based.Structure.LogicExpressions.LogicInversion import LogicInversion
from based.Structure.LogicExpressions.LogicOperation import LogicAnd, LogicOr


class LogicVariable(LogicExpression):
    def __invert__(self) -> LogicExpression:
        return LogicInversion.create(self)

    def __and__(self, other: LogicExpression) -> LogicExpression:
        return LogicAnd.create(self, other)

    def __or__(self, other: LogicExpression) -> LogicExpression:
        return LogicOr.create(self, other)

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

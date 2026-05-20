from typing import override

from based.Structure.Expressions.SortPriority import SortPriority
from based.Structure.LogicExpressions.LogicExpression import LogicExpression


class LogicInversion(LogicExpression):
    def evaluate(self, var: 'Variable', val: 'EvaluableConstant') -> LogicExpression:
        return LogicInversion.create(self.expr.evaluate(var, val))

    def __init__(self, expr: LogicExpression, *args, **kwargs) -> None:
        super().__init__(expr, *args, **kwargs)
        self.expr = expr

    @override
    def simplify(self) -> LogicExpression:
        from based.Structure.LogicExpressions.LogicVariable import LogicVariable
        if isinstance(self.expr, LogicVariable):
            return self
        return ~self.expr

    @override
    def __invert__(self) -> LogicExpression:
        return self.expr

    @override
    def __and__(self, other: LogicExpression) -> LogicExpression:
        pass

    @override
    def __or__(self, other: LogicExpression) -> LogicExpression:
        pass

    @override
    def __eq__(self, other: LogicExpression) -> bool:
        if isinstance(other, LogicInversion):
            return self.expr == other.expr
        return False

    @override
    def __hash__(self) -> int:
        return hash(self.expr)

    @override
    def sort_key(self) -> tuple[SortPriority, str | int, tuple]:
        return SortPriority.FUNCTION, "INV", (self.expr.sort_key())

    @override
    def __str__(self) -> str:
        return f"~{self.expr}"

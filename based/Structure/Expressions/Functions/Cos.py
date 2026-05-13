from typing import override
from based.Structure.Expressions.Expression import Expression
from based.Structure.Expressions.Constant import IntegerConstant, Constant

from based.Structure.Expressions.SortPriority import SortPriority

class Cos(Expression):
    @override
    def _simplify(self) -> Expression:
        if isinstance(self.args[0], Constant):
            if self.args[0] == IntegerConstant.create(0):
                return IntegerConstant.create(1)
        return self

    @override
    def sort_key(self) -> tuple[SortPriority, str, tuple]:
        return SortPriority.FUNCTION, "COS", self.args[0].sort_key()

    @override
    def diff(self, var: 'Variable') -> Expression:
        from based.Structure.Expressions.Functions.Sin import Sin

        return -Sin.create(self.args[0])*self.args[0].diff(var)

    @override
    def __eq__(self, other: Expression) -> bool:
        return isinstance(other, Cos) and self.args[0] == other.args[0]

    @override
    def __hash__(self) -> int:
        return hash((type(self), self.args[0]))

    @override
    def __neg__(self) -> Expression:
        from based.Structure.Expressions.Constant import IntegerConstant
        return self * IntegerConstant.create(-1)

    def __repr__(self):
        return f"cos({self.args[0]})"

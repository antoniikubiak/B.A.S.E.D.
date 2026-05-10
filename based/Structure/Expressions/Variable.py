from typing import override

from based.Structure.Expressions.Constant import IntegerConstant
from based.Structure.Expressions.Expression import Expression
from based.Structure.Expressions.Operations.Multiplication import Multiplication
from based.Structure.Expressions.SortPriority import SortPriority


class Variable(Expression):
    @override
    def sort_key(self) -> tuple[SortPriority, str, tuple[Expression, ...]]:
        return SortPriority.VARIABLE, self.name, ()

    @override
    def __hash__(self) -> int:
        return hash(self.name)

    @override
    def __eq__(self, other: Expression) -> bool:
        if isinstance(other, Variable):
            return self.name == other.name
        return False

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    @override
    def __neg__(self) -> Expression:
        return Multiplication.create(IntegerConstant(-1), self)

    @override
    def _simplify(self) -> Expression:
        return self

    def __repr__(self) -> str:
        return self.name

    @override
    def diff(self, var: str) -> Expression:
        if self.name == var:
            return IntegerConstant.create(1)
        return IntegerConstant.create(0)

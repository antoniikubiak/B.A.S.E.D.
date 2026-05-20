from typing import override

from based.Structure.Expressions.EvaluableConstant import IntegerConstant
from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from based.Structure.Expressions.Operations.Multiplication import Multiplication
from based.Structure.Expressions.SortPriority import SortPriority


class Variable(EvaluableExpression):
    def evaluate(self, var: Variable, val: 'EvaluableConstant') -> EvaluableExpression:
        if self == var:
            return val
        return self

    @override
    def sort_key(self) -> tuple[SortPriority, str, tuple[EvaluableExpression, ...]]:
        return SortPriority.VARIABLE, self.name, ()

    @override
    def __hash__(self) -> int:
        return hash(self.name)

    @override
    def __eq__(self, other: EvaluableExpression) -> bool:
        if isinstance(other, Variable):
            return self.name == other.name
        return False

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    @override
    def __neg__(self) -> EvaluableExpression:
        return Multiplication.create(IntegerConstant.create(-1), self)

    @override
    def simplify(self) -> EvaluableExpression:
        return self

    @override
    def __str__(self) -> str:
        return self.name

    @override
    def diff(self, var: 'Variable') -> EvaluableExpression:
        if self.name == var.name:
            return IntegerConstant.create(1)
        return IntegerConstant.create(0)

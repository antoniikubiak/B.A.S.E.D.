from copy import copy
from typing import override

from based.Structure.Constant import IntegerConstant, Constant
from based.Structure.CommutativeOperation import CommutativeOperation
from based.Structure.Expression import Expression
from based.Structure.SortPriority import SortPriority


class Multiplication(CommutativeOperation):
    @override
    def sort_key(self) -> tuple[SortPriority, str | int, tuple[Expression, ...]]:
        return SortPriority.OPERATION, "MUL", self.args

    @override
    @staticmethod
    def operate_on_constants(left: Constant, right: Constant) -> Constant:
        return left * right

    @override
    @staticmethod
    def is_identity(element: Constant) -> bool:
        return element == Multiplication.identity()

    @override
    @staticmethod
    def is_absorbing(element: Constant) -> bool:
        return element == IntegerConstant.create(0)

    @override
    @staticmethod
    def identity() -> Constant:
        return IntegerConstant.create(1)

    def __repr__(self):
        return " * ".join(str(x) for x in self.args)

    @override
    def __mul__(self, other: Expression) -> Expression:
        if isinstance(other, Multiplication):
            return Multiplication.create(*(list(self.args) + list(other.args)))
        return Multiplication.create(*(list(self.args) + [other]))

    @override
    def __truediv__(self, other: Expression) -> Expression:
        if isinstance(other, Multiplication):
            return Multiplication.create(*(list(self.args) + list(~x for x in other.args)))
        return Multiplication.create(*(list(self.args) + [~other]))

    @override
    def __neg__(self) -> Expression:
        return self * IntegerConstant.create(-1)

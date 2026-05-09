from typing import override

from based.Structure.Constant import Constant, IntegerConstant
from based.Structure.Expression import Expression
from based.Structure.Multiplication import Multiplication
from based.Structure.NonCommutativeOperation import NonCommutativeOperation
from based.Structure.SortPriority import SortPriority


class Exponentiation (NonCommutativeOperation):
    @override
    @staticmethod
    def is_distributive_over(operation: type) -> bool:
        return operation == Multiplication

    @override
    def get_parts(self) -> tuple[Expression, Expression]:
        return self.left, self.right

    @override
    def sort_key(self) -> tuple[SortPriority, str | int, tuple]:
        return SortPriority.OPERATION, "EXP", (self.left.sort_key(), self.right.sort_key())

    @override
    def __neg__(self) -> Expression:
        return Multiplication.create(IntegerConstant.create(-1), self)

    @override
    @staticmethod
    def identity() -> Constant:
        return IntegerConstant.create(1)

    @override
    @staticmethod
    def operate_on_constants(left: Constant, right: Constant) -> Expression:
        return left ** right

    @override
    @staticmethod
    def is_identity(element: Constant) -> bool:
        return element == IntegerConstant.create(1)

    @override
    @staticmethod
    def is_absorbing(element: Constant) -> bool:
        return element == IntegerConstant.create(0)

    @override
    def __invert__(self) -> Expression:
        return Exponentiation.create(self.left, -self.right)

    def __repr__(self) -> str:
        return f"{self.left}^{self.right}"

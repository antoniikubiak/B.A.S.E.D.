from typing import override

from based.Structure.Constant import Constant, IntegerConstant
from based.Structure.Expression import Expression
from based.Structure.Multiplication import Multiplication
from based.Structure.NonCommutativeOperation import NonCommutativeOperation
from based.Structure.SortPriority import SortPriority


class Exponentiation (NonCommutativeOperation):
    @override
    def sort_key(self) -> tuple[SortPriority, str | int, tuple[Expression, ...]]:
        return SortPriority.OPERATION, "EXP", (self.left, self.right)

    @override
    def __neg__(self) -> Expression:
        return Multiplication.create(IntegerConstant.create(-1), self)

    @override
    @staticmethod
    def identity() -> Constant:
        return IntegerConstant.create(1)

    @override
    @staticmethod
    def operate_on_constants(left: Constant, right: Constant) -> Constant:
        return left ** right

    @override
    @staticmethod
    def is_identity(element: Constant) -> bool:
        return element == IntegerConstant.create(1)

    @override
    @staticmethod
    def is_absorbing(element: Constant) -> bool:
        return element == IntegerConstant.create(0)

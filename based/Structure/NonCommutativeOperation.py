from abc import ABC
from typing import override

from based.Structure.Constant import Constant
from based.Structure.Expression import Expression
from based.Structure.Operation import Operation


class NonCommutativeOperation(Operation, ABC):
    left: Expression
    right: Expression
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    @override
    def __hash__(self) -> int:
        return hash((type(self), self.left, self.right))

    @override
    def __eq__(self, other: Expression) -> bool:
        if isinstance(other, self.__class__):
            return self.left == other.left and self.right == other.right
        return False

    @override
    def _simplify(self) -> Expression:
        self.left._simplify()
        self.right._simplify()
        if isinstance(self.right, Constant):
            if self.__class__.is_absorbing(self.right):
                return self.__class__.identity()
            if self.__class__.is_identity(self.right):
                return self.left

        if isinstance(self.left, Constant):
            if self.__class__.is_identity(self.left):
                return self.__class__.identity()

        if isinstance(self.left, Constant) and isinstance(self.right, Constant):
            return self.__class__.operate_on_constants(self.left, self.right)

        return self

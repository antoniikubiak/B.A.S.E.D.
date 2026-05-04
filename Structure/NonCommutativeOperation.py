from abc import abstractmethod, ABC
from typing import override

from Structure.Constant import Constant
from Structure.Expression import Expression
from Structure.Operation import Operation


class NonCommutativeOperation(Operation, ABC):
    left: Expression
    right: Expression
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    @override
    def simplify(self) -> Expression:
        self.left.simplify()
        self.right.simplify()
        if isinstance(self.right, Constant):
            if self.__class__.is_absorbing(self.right):
                return self.__class__.identity()

        if isinstance(self.left, Constant):
            if self.__class__.is_identity(self.left):
                return self.__class__.identity()

        if isinstance(self.left, Constant) and isinstance(self.right, Constant):
            return self.__class__.operate_on_constants(self.left, self.right)

        return self

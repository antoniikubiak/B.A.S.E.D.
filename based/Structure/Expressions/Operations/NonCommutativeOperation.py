from abc import ABC
from typing import override

from based.Structure.Expressions.Constant import Constant
from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from based.Structure.Expressions.Operations.Operation import Operation


class NonCommutativeOperation(Operation, ABC):
    """
    Abstract base for operations where the order of arguments matters (e.g., exponentiation).
    """
    left: EvaluableExpression
    right: EvaluableExpression
    def __init__(self, left: EvaluableExpression, right: EvaluableExpression, *args, **kwargs) -> None:
        """
        Initializes a binary non-commutative operation.
        :param left: The primary operand (e.g., the base).
        :param right: The secondary operand (e.g., the exponent).
        """
        super().__init__(*args, **kwargs)
        self.left = left
        self.right = right

    @override
    def __hash__(self) -> int:
        return hash((type(self), self.left, self.right))

    @override
    def __eq__(self, other: EvaluableExpression) -> bool:
        if isinstance(other, self.__class__):
            return self.left == other.left and self.right == other.right
        return False

    @override
    def _simplify(self) -> EvaluableExpression:
        """
        Simplifies the operation based on identity and absorbing elements.
        :return: A simplified `Expression`.
        """
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

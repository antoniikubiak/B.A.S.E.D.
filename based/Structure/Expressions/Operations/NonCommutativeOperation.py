from abc import ABC, abstractmethod
from typing import override

from based.Structure.Expressions.EvaluableConstant import EvaluableConstant
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

    @staticmethod
    @abstractmethod
    def _get_lower_order_operation() -> type[Operation]:
        pass

    @override
    def simplify(self) -> EvaluableExpression:
        """
        Simplifies the operation based on identity and absorbing elements.
        :return: A simplified `Expression`.
        """
        if isinstance(self.right, EvaluableConstant):
            if self.__class__.absorbing_element() == self.right:
                return self.__class__.identity()
            if self.__class__.identity() == self.right:
                return self.left

        if isinstance(self.left, EvaluableConstant):
            if self.__class__.identity() == self.left:
                return self.__class__.identity()

        if isinstance(self.left, EvaluableConstant) and isinstance(self.right, EvaluableConstant):
            return self.__class__._operate_on_constants(self.left, self.right)

        if isinstance(self.left, self.__class__):
            return self.__class__.create(self.left.left, self.__class__._get_lower_order_operation().create(self.left.right, self.right))

        return self

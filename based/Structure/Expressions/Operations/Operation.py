from abc import abstractmethod

from based.Structure.Expressions.EvaluableConstant import EvaluableConstant
from based.Structure.Expressions.EvaluableExpression import EvaluableExpression


class Operation(EvaluableExpression):
    """
    Abstract base for all mathematical operations.
    """
    @staticmethod
    @abstractmethod
    def identity() -> EvaluableConstant:
        pass

    @staticmethod
    @abstractmethod
    def absorbing_element() -> EvaluableConstant:
        pass

    @staticmethod
    @abstractmethod
    def _operate_on_constants(left: EvaluableConstant, right: EvaluableConstant) -> EvaluableConstant:
        pass

    @staticmethod
    @abstractmethod
    def is_distributive_over(operation: type) -> bool:
        """
        Checks if `cls` distributes over the given `operation` type.
        :param operation: The operation type to check.
        :return: Boolean indicating whether `cls` distributes over the given `operation` type.
        """
        pass

    @abstractmethod
    def get_parts(self) -> tuple[EvaluableExpression, EvaluableExpression]:
        """
        Method used in gathering like terms when simplifying operation.
        :return: Tuple consisting of: base-like object and exponent-like object.
        """
        pass

from abc import abstractmethod

from based.Structure.Expressions.Constant import Constant
from based.Structure.Expressions.EvaluableExpression import EvaluableExpression


class Operation(EvaluableExpression):
    """
    Abstract base for all mathematical operations.
    """
    @staticmethod
    @abstractmethod
    def identity() -> Constant:
        pass

    @staticmethod
    @abstractmethod
    def operate_on_constants(left: Constant, right: Constant) -> Constant:
        pass

    @staticmethod
    @abstractmethod
    def is_identity(element: Constant) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def is_absorbing(element: Constant) -> bool:
        """
        Checks whether `element` is absorbing ('consumes' whole expression).
        :param element: Element to be checked.
        :return: True if `element` is absorbing, else False.
        """
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

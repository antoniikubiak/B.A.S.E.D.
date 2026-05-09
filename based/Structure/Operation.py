from abc import abstractmethod

from based.Structure.Constant import Constant
from based.Structure.Expression import Expression


class Operation(Expression):
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
        pass

    @staticmethod
    @abstractmethod
    def is_distributive_over(operation: type) -> bool:
        pass

    @abstractmethod
    def get_parts(self) -> tuple[Expression, Expression]:
        """
        Method used in gathering like terms when simplifying operation.
        :return: Tuple consisting of: base-like object and exponent-like object.
        """
        pass

from abc import abstractmethod

from Structure.Constant import Constant
from Structure.Expression import Expression


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



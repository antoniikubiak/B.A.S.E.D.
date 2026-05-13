from abc import abstractmethod, ABC

from based.Structure import SimplifiableExpression


class LogicExpression(SimplifiableExpression, ABC):
    """
    Represents a node that can be eventually evaluated to represent a truth value.
    """

    @abstractmethod
    def __invert__(self) -> LogicExpression:
        """Method representing logical ``not``."""

    @abstractmethod
    def __and__(self, other: LogicExpression) -> LogicExpression:
        pass

    @abstractmethod
    def __or__(self, other: LogicExpression) -> LogicExpression:
        pass

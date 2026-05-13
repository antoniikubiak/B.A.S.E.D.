from abc import abstractmethod

from based.Structure.Expressions.SortPriority import SortPriority
from based.Structure.Node import Node


class SimplifiableExpression(Node):
    _CREATE_KEY = object()
    """Sentinel blocking creation with `Expression(*args)` syntax so that objects can only be created with `.create()` method."""

    def __init__(self, *args, create_key=None):
        if create_key is not self._CREATE_KEY:
            raise RuntimeError(
                f"Direct instantiation of {self.__class__.__name__} is forbidden. "
                f"Use {self.__class__.__name__}.create() instead."
            )
        self.args = args

    @classmethod
    def create(cls, *args) -> SimplifiableExpression:
        """
        Creates a new Expression object. Should be always used when generating new instances of an object.
        :param args: Positional arguments required by the specific `Expression` subclass.
        :return: An instance that has been immediately processed through the simplification.
        """
        instance = cls(*args, create_key=cls._CREATE_KEY)
        return instance._simplify()

    @abstractmethod
    def _simplify(self) -> SimplifiableExpression:
        """
        Internal method to reduce the expression to its simplest algebraic form.
        :return: A simplified Expression instance.
        """
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass

    @abstractmethod
    def __eq__(self, other: SimplifiableExpression) -> bool:
        pass

    @abstractmethod
    def sort_key(self) -> tuple[SortPriority, str | int, tuple]:
        """
        Generates a key for canonical ordering.
        :return: A tuple used to compare and sort nodes within commutative operations.
        """
        pass

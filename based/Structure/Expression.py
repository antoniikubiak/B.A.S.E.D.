from abc import abstractmethod

from based.Structure.SortPriority import SortPriority
from based.Structure.Node import Node


class Expression(Node):
    """
    Represents a node that can be eventually evaluated to produce a value.
    """
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
    def create(cls, *args) -> Expression:
        """
        Creates a new Expression object. Should be always used when generating new instances of an object.
        :param args: Positional arguments required by the specific `Expression` subclass.
        :return: An instance that has been immediately processed through the simplification.
        """
        instance = cls(*args, create_key=cls._CREATE_KEY)
        return instance._simplify()

    @abstractmethod
    def _simplify(self) -> Expression:
        """
        Internal method to reduce the expression to its simplest algebraic form.
        :return: A simplified Expression instance.
        """
        pass

    @abstractmethod
    def sort_key(self) -> tuple[SortPriority, str | int, tuple]:
        """
        Generates a key for canonical ordering.
        :return: A tuple used to compare and sort nodes within commutative operations.
        """
        pass

    @abstractmethod
    def __neg__(self) -> Expression:
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass

    @abstractmethod
    def __eq__(self, other: Expression) -> bool:
        pass

    def normalize(self) -> Expression:
        """
        Extracts the symbolic part of the term, stripping away constant coefficients.
        :return: The normalized symbolic `Expression`.
        """
        return self

    def constant_term(self) -> 'Constant':
        """
        Extracts the numeric coefficient of the expression.
        :return: The `Constant` representing the coefficient, defaulting to 1.
        """
        from based.Structure.Constant import IntegerConstant
        return IntegerConstant.create(1)

    def __invert__(self) -> Expression:
        from based.Structure.Exponentiation import Exponentiation
        from based.Structure.Constant import IntegerConstant
        return Exponentiation.create(self, IntegerConstant.create(-1))

    def __add__(self, other: Expression) -> Expression:
        from based.Structure.Addition import Addition
        return Addition.create(self, other)

    def __sub__(self, other: Expression) -> Expression:
        from based.Structure.Addition import Addition
        return Addition.create(self, -other)

    def __mul__(self, other: Expression) -> Expression:
        from based.Structure.Multiplication import Multiplication
        return Multiplication.create(self, other)

    def __truediv__(self, other: Expression) -> Expression:
        from based.Structure.Multiplication import Multiplication
        return Multiplication.create(self, ~other)

    @abstractmethod
    def diff(self, var: str) -> 'Expression':
        pass
from abc import abstractmethod

from based.Structure.SortPriority import SortPriority
from based.Structure.Node import Node


class Expression(Node):
    @classmethod
    def create(cls, *args) -> Expression:
        instance = cls(*args)
        return instance._simplify()

    @abstractmethod
    def _simplify(self) -> Expression:
        pass

    @abstractmethod
    def sort_key(self) -> tuple[SortPriority, str | int, tuple[Expression, ...]]:
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
        return self

    def constant_term(self) -> 'Constant':
        from based.Structure.Constant import IntegerConstant
        return IntegerConstant.create(1)

    def __invert__(self) -> Expression:
        from based.Structure.Exponentiation import Exponentiation
        from based.Structure.Constant import IntegerConstant
        return Exponentiation.create(self, IntegerConstant(-1))

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

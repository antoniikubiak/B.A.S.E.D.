from abc import abstractmethod
from functools import total_ordering
from typing import override, Any

from based.Structure.Constant import Constant
from based.Structure.Epsilon import eps
from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from based.Structure.Expressions.SortPriority import SortPriority

@total_ordering
class EvaluableConstant[T: (int, float)](EvaluableExpression, Constant):
    """
    Represents a literal numeric value within an expression.
    """
    def __init__(self, value: Any, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.value: T = self._cast(value)

    @abstractmethod
    def _cast(self, value: Any) -> T:
        """
        Converts a raw numeric value into a type of `Constant` subclass.
        :param value: a value to be converted into a type of `Constant` subclass.
        :return: `value` wrapped in type `T` appropriate for a subclass of `Constant`.
        """
        pass

    @override
    def simplify(self) -> EvaluableExpression:
        return self

    @override
    def sort_key(self) -> tuple[SortPriority, int, tuple[EvaluableExpression, ...]]:
        return SortPriority.CONSTANT, self.value, ()

    @override
    def __hash__(self) -> int:
        return hash(self.value)

    @override
    def __invert__(self) -> EvaluableConstant:
        if self.value == 0:
            raise ZeroDivisionError("Cannot invert zero constant")
        return self._wrap(1 / self.value)

    @override
    def normalize(self) -> EvaluableConstant:
        return IntegerConstant.create(1)

    @override
    def constant_term(self) -> EvaluableConstant:
        return self

    def is_zero(self) -> bool:
        """Checks if the constant value is effectively zero within epsilon bounds."""
        return abs(self.value) < eps

    def _wrap(self, result: Any) -> EvaluableConstant:
        """
        Wraps a raw numeric result into the appropriate `Constant` subclass.
        :param result: A value to be converted into a `Constant`.
        :return: `Constant` generated from `result`
        """
        if isinstance(result, float):
            return FloatConstant.create(result)
        return IntegerConstant.create(result)

    @override
    def diff(self, var: 'Variable') -> EvaluableExpression:
        return IntegerConstant.create(0)

    @override
    def __add__(self, other: Any) -> EvaluableExpression:
        from based.Structure.Expressions.Operations.Addition import Addition
        if isinstance(other, EvaluableConstant):
            return self._wrap(self.value + other.value)
        if isinstance(other, EvaluableExpression):
            return Addition.create(self, other)
        return NotImplemented

    @override
    def __sub__(self, other: Any) -> EvaluableExpression:
        from based.Structure.Expressions.Operations.Addition import Addition
        if isinstance(other, EvaluableConstant):
            return self._wrap(self.value - other.value)
        if isinstance(other, EvaluableExpression):
            return Addition.create(self, -other)
        return NotImplemented

    @override
    def __mul__(self, other: Any) -> EvaluableExpression:
        from based.Structure.Expressions.Operations.Multiplication import Multiplication
        if isinstance(other, EvaluableConstant):
            return self._wrap(self.value * other.value)
        if isinstance(other, EvaluableExpression):
            return Multiplication.create(self, other)
        return NotImplemented

    @override
    def __truediv__(self, other: Any) -> EvaluableExpression:
        from based.Structure.Expressions.Operations.Multiplication import Multiplication
        if isinstance(other, EvaluableConstant):
            return self._wrap(self.value / other.value)
        if isinstance(other, EvaluableExpression):
            return Multiplication.create(self, ~other)
        return NotImplemented

    def __pow__(self, other: Any) -> EvaluableExpression:
        from based.Structure.Expressions.Operations.Exponentiation import Exponentiation
        if isinstance(other, EvaluableConstant):
            return self._wrap(self.value ** other.value)
        if isinstance(other, EvaluableExpression):
            return Exponentiation.create(self, other)
        return NotImplemented

    @override
    def __neg__(self) -> EvaluableConstant:
        return self._wrap(-self.value)

    def __pos__(self) -> EvaluableConstant:
        return self._wrap(self.value)

    @override
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, EvaluableConstant):
            return abs(self.value - other.value) < eps
        return False

    def __le__(self, other: Any) -> bool:
        if isinstance(other, EvaluableConstant):
            return self.value <= other.value
        return NotImplemented

    @override
    def __str__(self):
        return str(self.value)

    @override
    def evaluate(self, var: 'Variable', val: EvaluableConstant) -> EvaluableExpression:
        return self

class IntegerConstant(EvaluableConstant[int]):
    @override
    def _cast(self, value: Any) -> int:
        return int(value)

class FloatConstant(EvaluableConstant[float]):
    @override
    def _cast(self, value: Any) -> float:
        return float(value)

from abc import abstractmethod
from typing import override, Any

from based.Structure.Epsilon import eps
from based.Structure.Expression import Expression
from based.Structure.SortPriority import SortPriority


class Constant[T: (int, float)](Expression):
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
    def _simplify(self) -> Expression:
        return self

    @override
    def sort_key(self) -> tuple[SortPriority, int, tuple[Expression, ...]]:
        return SortPriority.CONSTANT, self.value, ()

    @override
    def __hash__(self) -> int:
        return hash(self.value)

    @override
    def __invert__(self) -> Constant:
        if self.value == 0:
            raise ZeroDivisionError("Cannot invert zero constant")
        return self._wrap(1 / self.value)

    @override
    def normalize(self) -> Constant:
        return IntegerConstant.create(1)

    @override
    def constant_term(self) -> Constant:
        return self

    def is_zero(self) -> bool:
        """Checks if the constant value is effectively zero within epsilon bounds."""
        return abs(self.value) < eps

    def _wrap(self, result: Any) -> Constant:
        """
        Wraps a raw numeric result into the appropriate `Constant` subclass.
        :param result: A value to be converted into a `Constant`.
        :return: `Constant` generated from `result`
        """
        if isinstance(result, float):
            return FloatConstant.create(result)
        return IntegerConstant.create(result)

    @override
    def __add__(self, other: Any) -> Expression:
        from based.Structure.Addition import Addition
        if isinstance(other, Constant):
            return self._wrap(self.value + other.value)
        if isinstance(other, Expression):
            return Addition.create(self, other)
        return NotImplemented

    @override
    def __sub__(self, other: Any) -> Expression:
        from based.Structure.Addition import Addition
        if isinstance(other, Constant):
            return self._wrap(self.value - other.value)
        if isinstance(other, Expression):
            return Addition.create(self, -other)
        return NotImplemented

    @override
    def __mul__(self, other: Any) -> Expression:
        from based.Structure.Multiplication import Multiplication
        if isinstance(other, Constant):
            return self._wrap(self.value * other.value)
        if isinstance(other, Expression):
            return Multiplication.create(self, other)
        return NotImplemented

    @override
    def __truediv__(self, other: Any) -> Expression:
        from based.Structure.Multiplication import Multiplication
        if isinstance(other, Constant):
            return self._wrap(self.value / other.value)
        if isinstance(other, Expression):
            return Multiplication.create(self, ~other)
        return NotImplemented

    def __pow__(self, other: Any) -> Expression:
        from based.Structure.Exponentiation import Exponentiation
        if isinstance(other, Constant):
            return self._wrap(self.value ** other.value)
        if isinstance(other, Expression):
            return Exponentiation.create(self, other)
        return NotImplemented

    @override
    def __neg__(self) -> Constant:
        return self._wrap(-self.value)

    def __pos__(self) -> Constant:
        return self._wrap(self.value)

    @override
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Constant):
            return abs(self.value - other.value) < eps
        return False

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __repr__(self):
        return str(self.value)

class IntegerConstant(Constant[int]):
    @override
    def _cast(self, value: Any) -> int:
        return int(value)

class FloatConstant(Constant[float]):
    @override
    def _cast(self, value: Any) -> float:
        return float(value)

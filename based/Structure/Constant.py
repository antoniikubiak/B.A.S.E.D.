from abc import abstractmethod
from typing import override, Any
from based.Structure.Epsilon import eps
from based.Structure.Expression import Expression

class Constant[T: (int, float)](Expression):
    def __init__(self, value: Any) -> None:
        self.value: T = self._cast(value)

    @abstractmethod
    def _cast(self, value: Any) -> T:
        pass

    @override
    def simplify(self) -> Expression:
        return self

    def is_zero(self) -> bool:
        return abs(self.value) < eps

    def _wrap(self, result: Any) -> Constant:
        if isinstance(result, float):
            return FloatConstant(result)
        return IntegerConstant(result)

    def __add__(self, other: Any) -> Constant:
        if isinstance(other, Constant):
            return self._wrap(self.value + other.value)
        return NotImplemented

    def __mul__(self, other: Any) -> Constant:
        if isinstance(other, Constant):
            return self._wrap(self.value * other.value)
        return NotImplemented

    def __pow__(self, other: Any) -> Constant:
        if isinstance(other, Constant):
            return self._wrap(self.value ** other.value)
        return NotImplemented

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Constant):
            return abs(self.value - other.value) < eps
        return False

    def __repr__(self):
        return str(self.value)

class IntegerConstant(Constant[int]):
    def _cast(self, value: Any) -> int:
        return int(value)

class FloatConstant(Constant[float]):
    def _cast(self, value: Any) -> float:
        return float(value)
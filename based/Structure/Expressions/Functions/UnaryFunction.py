from abc import ABC, abstractmethod
from based.Structure.Expressions.Expression import Expression
from typing import override
from based.Structure.Expressions.Constant import Constant


class UnaryFunction(Expression, ABC):
    def __init__(self, arg: Expression, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arg = arg

    @abstractmethod
    def get_derivative_formula(self) -> Expression:
        pass

    @override
    def diff(self, var: 'Variable') -> Expression:
        return self.get_derivative_formula() * self.arg.diff(var)

    @override
    def _simplify(self) -> Expression:
        simplified_arg = self.arg._simplify()

        if isinstance(simplified_arg, Constant):
            return self.evaluate_numeric(simplified_arg.value)

        if simplified_arg is self.arg or simplified_arg == self.arg:
            return self

        return self.__class__.create(simplified_arg)

    @abstractmethod
    def evaluate_numeric(self, value: float) -> Constant:
        pass

    @override
    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.arg == other.arg
        return False

    @override
    def __hash__(self) -> int:
        return hash((self.__class__, self.arg))

    @override
    def __neg__(self) -> Expression:
        from based.Structure.Expressions.Constant import IntegerConstant
        return IntegerConstant.create(-1) * self
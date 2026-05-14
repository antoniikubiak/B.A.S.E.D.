from abc import ABC, abstractmethod
from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from typing import override
from based.Structure.Expressions.EvaluableConstant import EvaluableConstant
from based.Structure.Expressions.Variable import Variable


class UnaryFunction(EvaluableExpression, ABC):
    def __init__(self, arg: EvaluableExpression, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arg = arg

    @abstractmethod
    def get_derivative_formula(self) -> EvaluableExpression:
        pass

    @override
    def diff(self, var: Variable) -> EvaluableExpression:
        return self.get_derivative_formula() * self.arg.diff(var)

    @override
    def simplify(self) -> EvaluableExpression:
        simplified_arg = self.arg.simplify()

        if isinstance(simplified_arg, EvaluableConstant):
            return self.evaluate_numeric(simplified_arg.value)

        if simplified_arg is self.arg or simplified_arg == self.arg:
            return self

        return self.__class__.create(simplified_arg)

    @abstractmethod
    def evaluate_numeric(self, value: float) -> EvaluableConstant:
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
    def __neg__(self) -> EvaluableExpression:
        from based.Structure.Expressions.EvaluableConstant import IntegerConstant
        return IntegerConstant.create(-1) * self

from abc import ABC, abstractmethod
from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from typing import override
from based.Structure.Expressions.EvaluableConstant import EvaluableConstant, IntegerConstant
from based.Structure.Expressions.Variable import Variable


class CallableFunction(EvaluableExpression, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.args = args

    @abstractmethod
    def get_derivative_formula(self, position: int) -> EvaluableExpression:
        pass

    @override
    def diff(self, var: Variable) -> EvaluableExpression:
        return sum((self.get_derivative_formula(i) * arg.diff(var) for i, arg in enumerate(self.args)), IntegerConstant.create(0))

    @override
    def simplify(self) -> EvaluableExpression:
        simplified_args = [a.simplify() for a in self.args]

        if all(isinstance(arg, EvaluableConstant) for arg in simplified_args):
            return self.evaluate_numeric(simplified_args)

        self.args = tuple(x for x in simplified_args)
        return self

    @abstractmethod
    def evaluate_numeric(self, value: list[float]) -> EvaluableConstant:
        pass

    @override
    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.args == other.args
        return False

    @override
    def __hash__(self) -> int:
        return hash((self.__class__, self.args))

    @override
    def __neg__(self) -> EvaluableExpression:
        from based.Structure.Expressions.EvaluableConstant import IntegerConstant
        return IntegerConstant.create(-1) * self

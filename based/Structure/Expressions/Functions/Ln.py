from typing import override
import math

from based.Structure.Expressions.EvaluableConstant import EvaluableConstant
from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from based.Structure.Expressions.Functions.CallableFunction import CallableFunction
from based.Structure.Expressions.Variable import Variable


class Ln(CallableFunction):
    @override
    def evaluate(self, var: Variable, val: EvaluableConstant) -> EvaluableExpression:
        return Ln.create(self.args[0].evaluate(var, val))

    @override
    def get_derivative_formula(self, position: int) -> EvaluableExpression:
        from based.Structure.Expressions.EvaluableConstant import IntegerConstant
        if position != 0:
            raise ValueError(f"Cannot differentiate cos function at argument {position}, since it accepts only 1 argument.")
        return IntegerConstant.create(1) / self.args[0]

    @override
    def evaluate_numeric(self, value: list[float]) -> EvaluableConstant:
        from based.Structure.Expressions.EvaluableConstant import FloatConstant
        raw_value = value[0]
        if raw_value <= 0:
            raise ValueError("Logarithm of non-positive number")
        return FloatConstant.create(math.log(raw_value))

    @override
    def sort_key(self):
        from based.Structure.Expressions.SortPriority import SortPriority
        return SortPriority.FUNCTION, "LN", (self.args[0].sort_key(),)

    @override
    def __str__(self):
        return f"ln({self.args[0]})"

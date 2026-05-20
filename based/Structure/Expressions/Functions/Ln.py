from typing import override
import math

from based.Structure.Expressions.EvaluableConstant import EvaluableConstant
from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from based.Structure.Expressions.Functions.UnaryFunction import UnaryFunction
from based.Structure.Expressions.Variable import Variable


class Ln(UnaryFunction):
    @override
    def evaluate(self, var: Variable, val: EvaluableConstant) -> EvaluableExpression:
        return Ln.create(self.arg.evaluate(var, val))

    @override
    def get_derivative_formula(self):
        from based.Structure.Expressions.EvaluableConstant import IntegerConstant
        return IntegerConstant.create(1) / self.arg

    @override
    def evaluate_numeric(self, value: float):
        from based.Structure.Expressions.EvaluableConstant import FloatConstant
        if value <= 0:
            raise ValueError("Logarithm of non-positive number")
        return FloatConstant.create(math.log(value))

    @override
    def sort_key(self):
        from based.Structure.Expressions.SortPriority import SortPriority
        return SortPriority.FUNCTION, "LN", (self.arg.sort_key(),)

    @override
    def __str__(self):
        return f"ln({self.arg})"

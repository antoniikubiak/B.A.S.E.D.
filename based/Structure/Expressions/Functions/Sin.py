from typing import override
import math

from based.Structure.Expressions.EvaluableConstant import EvaluableConstant
from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from based.Structure.Expressions.Functions.UnaryFunction import UnaryFunction
from based.Structure.Expressions.Variable import Variable


class Sin(UnaryFunction):
    @override
    def evaluate(self, var: Variable, val: EvaluableConstant) -> EvaluableExpression:
        return Sin.create(self.arg.evaluate(var, val))

    @override
    def get_derivative_formula(self):
        from based.Structure.Expressions.Functions.Cos import Cos
        return Cos.create(self.arg)

    @override
    def evaluate_numeric(self, value: float):
        from based.Structure.Expressions.EvaluableConstant import FloatConstant
        return FloatConstant.create(math.sin(value))

    @override
    def sort_key(self):
        from based.Structure.Expressions.SortPriority import SortPriority
        return SortPriority.FUNCTION, "SIN", (self.arg.sort_key(),)

    @override
    def __str__(self):
        return f"sin({self.arg})"

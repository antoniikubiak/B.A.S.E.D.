from typing import override
import math
from based.Structure.Expressions.Functions.UnaryFunction import UnaryFunction

class Sin(UnaryFunction):
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

    def __repr__(self):
        return f"sin({self.arg})"

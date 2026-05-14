from typing import override
import math
from based.Structure.Expressions.Functions.UnaryFunction import UnaryFunction

class Cos(UnaryFunction):
    @override
    def get_derivative_formula(self):
        from based.Structure.Expressions.Functions.Sin import Sin

        return -Sin.create(self.arg)

    @override
    def evaluate_numeric(self, value: float):
        from based.Structure.Expressions.EvaluableConstant import FloatConstant
        return FloatConstant.create(math.cos(value))

    @override
    def sort_key(self):
        from based.Structure.Expressions.SortPriority import SortPriority
        return SortPriority.FUNCTION, "COS", (self.arg.sort_key(),)

    def __repr__(self):
        return f"cos({self.arg})"

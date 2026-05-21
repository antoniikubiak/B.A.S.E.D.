from typing import override
import math

from based.Structure.Expressions.EvaluableConstant import EvaluableConstant
from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from based.Structure.Expressions.Functions.CallableFunction import CallableFunction
from based.Structure.Expressions.Variable import Variable


class Cos(CallableFunction):
    @override
    def evaluate(self, var: Variable, val: EvaluableConstant) -> EvaluableExpression:
        return Cos.create(self.args[0].evaluate(var, val))

    @override
    def get_derivative_formula(self, position: int) -> EvaluableExpression:
        from based.Structure.Expressions.Functions.Sin import Sin
        if position == 0:
            return -Sin.create(*self.args)
        else:
            raise ValueError(f"Cannot differentiate cos function at argument {position}, since it accepts only 1 argument.")

    @override
    def evaluate_numeric(self, value: float):
        from based.Structure.Expressions.EvaluableConstant import FloatConstant
        return FloatConstant.create(math.cos(value))

    @override
    def sort_key(self):
        from based.Structure.Expressions.SortPriority import SortPriority
        return SortPriority.FUNCTION, "COS", (self.args[0].sort_key(),)

    @override
    def __str__(self):
        return f"cos({self.args[0]})"

from typing import override
import math

from based.Structure.Expressions.EvaluableConstant import EvaluableConstant
from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from based.Structure.Expressions.Functions.CallableFunction import CallableFunction
from based.Structure.Expressions.Variable import Variable


class Sin(CallableFunction):
    @override
    def evaluate(self, var: Variable, val: EvaluableConstant) -> EvaluableExpression:
        return Sin.create(self.args[0].evaluate(var, val))

    @override
    def get_derivative_formula(self, position: int):
        from based.Structure.Expressions.Functions.Cos import Cos
        if position == 0:
            return Cos.create(*self.args)
        else:
            raise ValueError(f"Cannot differentiate cos function at argument {position}, since it accepts only 1 argument.")

    @override
    def evaluate_numeric(self, value: list[float]) -> EvaluableConstant:
        from based.Structure.Expressions.EvaluableConstant import FloatConstant
        return FloatConstant.create(math.sin(value[0]))

    @override
    def sort_key(self):
        from based.Structure.Expressions.SortPriority import SortPriority
        return SortPriority.FUNCTION, "SIN", (self.args[0].sort_key(),)

    @override
    def __str__(self):
        return f"sin({self.args[0]})"

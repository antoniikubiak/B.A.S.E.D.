from typing import override
import math

from based.Structure.Expressions.EvaluableConstant import EvaluableConstant
from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from based.Structure.Expressions.Functions.CallableFunction import CallableFunction
from based.Structure.Expressions.Variable import Variable


class Tan(CallableFunction):
    @override
    def __str__(self) -> str:
        return f"tan({self.args[0]})"

    @override
    def evaluate(self, var: Variable, val: EvaluableConstant) -> EvaluableExpression:
        return Tan.create(self.args[0].evaluate(var, val))

    @override
    def get_derivative_formula(self, position: int):
        from based.Structure.Expressions.Functions.Cos import Cos
        from based.Structure.Expressions.Operations.Exponentiation import Exponentiation
        from based.Structure.Expressions.EvaluableConstant import IntegerConstant

        if position != 0:
            raise ValueError(f"Cannot differentiate cos function at argument {position}, since it accepts only 1 argument.")

        cos_node = Cos.create(self.args[0])
        minus_two = IntegerConstant.create(-2)

        return Exponentiation.create(cos_node, minus_two)

    @override
    def evaluate_numeric(self, value: float):
        from based.Structure.Expressions.EvaluableConstant import FloatConstant
        return FloatConstant.create(math.tan(value))

    @override
    def sort_key(self):
        from based.Structure.Expressions.SortPriority import SortPriority
        return SortPriority.FUNCTION, "TAN", (self.args[0].sort_key(),)

    def __repr__(self):
        return f"tan({self.args[0]})"

from typing import override
import math

from based.Structure.Expressions.EvaluableConstant import EvaluableConstant
from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from based.Structure.Expressions.Functions.UnaryFunction import UnaryFunction
from based.Structure.Expressions.Variable import Variable


class Tan(UnaryFunction):
    @override
    def __str__(self) -> str:
        return f"tan({self.arg})"

    @override
    def evaluate(self, var: Variable, val: EvaluableConstant) -> EvaluableExpression:
        return Tan.create(self.arg.evaluate(var, val))

    @override
    def get_derivative_formula(self):
        from based.Structure.Expressions.Functions.Cos import Cos
        from based.Structure.Expressions.Operations.Exponentiation import Exponentiation
        from based.Structure.Expressions.EvaluableConstant import IntegerConstant

        cos_node = Cos.create(self.arg)
        minus_two = IntegerConstant.create(-2)

        return Exponentiation.create(cos_node, minus_two)

    @override
    def evaluate_numeric(self, value: float):
        from based.Structure.Expressions.EvaluableConstant import FloatConstant
        return FloatConstant.create(math.tan(value))

    @override
    def sort_key(self):
        from based.Structure.Expressions.SortPriority import SortPriority
        return SortPriority.FUNCTION, "TAN", (self.arg.sort_key(),)

    def __repr__(self):
        return f"tan({self.arg})"

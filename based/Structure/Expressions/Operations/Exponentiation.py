from typing import override

from based.Structure.Expressions.EvaluableConstant import EvaluableConstant, IntegerConstant
from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from based.Structure.Expressions.Operations.Multiplication import Multiplication
from based.Structure.Expressions.Operations.NonCommutativeOperation import NonCommutativeOperation
from based.Structure.Expressions.Operations.Operation import Operation
from based.Structure.Expressions.SortPriority import SortPriority


class Exponentiation(NonCommutativeOperation):
    @override
    def evaluate(self, var: 'Variable', val: EvaluableConstant) -> EvaluableExpression:
        return Exponentiation.create(self.left.evaluate(var, val), self.right.evaluate(var, val))

    @override
    @staticmethod
    def _get_lower_order_operation() -> type[Operation]:
        return Multiplication

    @override
    @staticmethod
    def is_distributive_over(operation: type) -> bool:
        return operation == Multiplication

    @override
    def get_parts(self) -> tuple[EvaluableExpression, EvaluableExpression]:
        return self.left, self.right

    @override
    def sort_key(self) -> tuple[SortPriority, str | int, tuple]:
        return SortPriority.OPERATION, "EXP", (self.left.sort_key(), self.right.sort_key())

    @override
    def __neg__(self) -> EvaluableExpression:
        return Multiplication.create(IntegerConstant.create(-1), self)

    @override
    @staticmethod
    def identity() -> EvaluableConstant:
        return IntegerConstant.create(1)

    @override
    @staticmethod
    def absorbing_element() -> EvaluableConstant:
        return IntegerConstant.create(0)

    @override
    @staticmethod
    def _operate_on_constants(left: EvaluableConstant, right: EvaluableConstant) -> EvaluableExpression:
        return left ** right


    @override
    def __invert__(self) -> EvaluableExpression:
        """
        Computes the multiplicative inverse by negating the exponent.
        :return: A new Exponentiation object representing $base^{-exponent}$.
        """
        return Exponentiation.create(self.left, -self.right)

    @override
    def __str__(self) -> str:
        if isinstance(self.right, IntegerConstant):
            return " * ".join([str(self.left)] * self.right.value)
        return f"pow({self.left}, {self.right})"

    def __init__(self, base, exponent, **kwargs):
        super().__init__(base, exponent, **kwargs)

    @override
    def diff(self, var: 'Variable') -> EvaluableExpression:
        from based.Structure.Expressions.Functions.Ln import Ln

        f = self.left
        g = self.right
        term_a = g.diff(var) * Ln.create(f)
        term_b = (g * f.diff(var)) / f

        return self * (term_a + term_b)

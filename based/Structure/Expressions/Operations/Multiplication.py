from typing import override

from based.Structure.Expressions.EvaluableConstant import IntegerConstant, EvaluableConstant
from based.Structure.Expressions.Operations.CommutativeOperation import CommutativeOperation
from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from based.Structure.Expressions.Operations.Operation import Operation
from based.Structure.Expressions.SortPriority import SortPriority


class Multiplication(CommutativeOperation):
    @override
    def evaluate(self, var: 'Variable', val: EvaluableConstant) -> EvaluableExpression:
        return Multiplication.create(*(arg.evaluate(var, val) for arg in self.args))

    @override
    @staticmethod
    def is_idempotent() -> bool:
        return False

    @override
    @staticmethod
    def get_higher_order_operation() -> type[Operation]:
        from based.Structure.Expressions.Operations.Exponentiation import Exponentiation
        return Exponentiation

    @override
    @staticmethod
    def is_distributive_over(operation: type) -> bool:
        from based.Structure.Expressions.Operations.Addition import Addition
        return operation == Addition

    @override
    def get_parts(self) -> tuple[EvaluableExpression, EvaluableExpression]:
        if isinstance(self.args[0], EvaluableConstant):
            return Multiplication.create(*self.args[1:]), self.args[0]
        return self, Multiplication.identity()

    @override
    def normalize(self) -> EvaluableExpression:
        if isinstance(self.args[0], EvaluableConstant):
            return Multiplication.create(*self.args[1:])
        return self

    @override
    def constant_term(self) -> EvaluableConstant:
        first_arg = self.args[0]
        if isinstance(first_arg, EvaluableConstant):
            return first_arg
        return IntegerConstant.create(1)

    @override
    def sort_key(self) -> tuple[SortPriority, str | int, tuple]:
        return SortPriority.OPERATION, "MUL", tuple(arg.sort_key() for arg in self.args)

    @override
    @staticmethod
    def _operate_on_constants(left: EvaluableConstant, right: EvaluableConstant) -> EvaluableExpression:
        return left * right

    @override
    @staticmethod
    def identity() -> EvaluableConstant:
        return IntegerConstant.create(1)

    @override
    @staticmethod
    def absorbing_element() -> EvaluableConstant:
        return IntegerConstant.create(0)

    @override
    def diff(self, var: 'Variable') -> EvaluableExpression:
        #(fgh)' = f'gh + fg'h + fgh' and the same for more vars

        from based.Structure.Expressions.Operations.Addition import Addition

        derivatives = []

        for i in range(len(self.args)):
            current_args = list(self.args)
            current_args[i] = self.args[i].diff(var)

            new_mult = Multiplication.create(*current_args)
            derivatives.append(new_mult)

        return Addition.create(*derivatives)

    @override
    def __str__(self):
        return " * ".join(str(x) for x in self.args)

    @override
    def __mul__(self, other: EvaluableExpression) -> EvaluableExpression:
        if isinstance(other, Multiplication):
            return Multiplication.create(*(list(self.args) + list(other.args)))
        return Multiplication.create(*(list(self.args) + [other]))

    @override
    def __truediv__(self, other: EvaluableExpression) -> EvaluableExpression:
        if isinstance(other, Multiplication):
            return Multiplication.create(*(list(self.args) + list(~x for x in other.args)))
        return Multiplication.create(*(list(self.args) + [~other]))

    @override
    def __neg__(self) -> EvaluableExpression:
        return self * IntegerConstant.create(-1)

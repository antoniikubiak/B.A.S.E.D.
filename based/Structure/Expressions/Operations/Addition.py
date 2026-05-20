from typing import override

from based.Structure.Expressions.Operations.CommutativeOperation import CommutativeOperation
from based.Structure.Expressions.EvaluableConstant import EvaluableConstant, IntegerConstant
from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from based.Structure.Expressions.Operations.Operation import Operation
from based.Structure.Expressions.SortPriority import SortPriority


class Addition(CommutativeOperation):
    @override
    def evaluate(self, var: 'Variable', val: EvaluableConstant) -> EvaluableExpression:
        return Addition.create(*(arg.evaluate(var, val) for arg in self.args))


    @override
    @staticmethod
    def absorbing_element() -> EvaluableConstant | None:
        return None

    @override
    @staticmethod
    def identity() -> EvaluableConstant:
        return IntegerConstant.create(0)

    @override
    @staticmethod
    def is_idempotent() -> bool:
        return False

    @override
    @staticmethod
    def get_higher_order_operation() -> type[Operation]:
        from based.Structure.Expressions.Operations.Multiplication import Multiplication
        return Multiplication

    def get_leading_constant(self) -> EvaluableConstant:
        first_arg = self.args[0]

        if isinstance(first_arg, EvaluableConstant):
            return first_arg
        return Addition.identity()

    @override
    @staticmethod
    def is_distributive_over(operation: type) -> bool:
        return False

    @override
    def get_parts(self) -> tuple[EvaluableExpression, EvaluableExpression]:
        return Addition.identity(), self

    @override
    def sort_key(self) -> tuple[SortPriority, str | int, tuple]:
        return SortPriority.OPERATION, "ADD", tuple(arg.sort_key() for arg in self.args)

    @override
    @staticmethod
    def _operate_on_constants(left: EvaluableConstant, right: EvaluableConstant) -> EvaluableExpression:
        return left + right

    @override
    def diff(self, var: 'Variable') -> EvaluableExpression:
        return Addition.create(*(arg.diff(var) for arg in self.args))

    @override
    def __str__(self):
        return " + ".join(str(x) for x in self.args)

    @override
    def __add__(self, other: EvaluableExpression) -> EvaluableExpression:
        if isinstance(other, Addition):
            return Addition.create(*(list(self.args) + list(other.args)))
        return Addition.create(*(list(self.args) + [other]))

    @override
    def __sub__(self, other: EvaluableExpression) -> EvaluableExpression:
        if isinstance(other, Addition):
            return Addition.create(*(list(self.args) + list(-x for x in other.args)))
        return Addition.create(*(list(self.args) + [-other]))

    @override
    def __neg__(self) -> EvaluableExpression:
        return Addition.create(*(-x for x in self.args))

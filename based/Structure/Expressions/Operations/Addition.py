from typing import override

from based.Structure.Expressions.Operations.CommutativeOperation import CommutativeOperation
from based.Structure.Expressions.Constant import Constant, IntegerConstant
from based.Structure.Expressions.Expression import Expression
from based.Structure.Expressions.Operations.Operation import Operation
from based.Structure.Expressions.SortPriority import SortPriority


class Addition (CommutativeOperation):
    @override
    @staticmethod
    def get_higher_order_operation() -> type[Operation]:
        from based.Structure.Expressions.Operations.Multiplication import Multiplication
        return Multiplication

    @override
    @staticmethod
    def is_distributive_over(operation: type) -> bool:
        return False

    @override
    def get_parts(self) -> tuple[Expression, Expression]:
        return Addition.identity(), self

    @override
    def sort_key(self) -> tuple[SortPriority, str | int, tuple]:
        return SortPriority.OPERATION, "ADD", tuple(arg.sort_key() for arg in self.args)

    @override
    @staticmethod
    def is_absorbing(element: Constant) -> bool:
        return False

    @override
    @staticmethod
    def identity() -> Constant:
        return IntegerConstant.create(0)

    @override
    @staticmethod
    def operate_on_constants(left: Constant, right: Constant) -> Expression:
        return left + right

    @override
    @staticmethod
    def is_identity(element: Constant) -> bool:
        return element == Addition.identity()

    @override
    def diff(self, var: 'Variable') -> Expression:
        return Addition.create(*(arg.diff(var) for arg in self.args))

    def __repr__(self):
        return " + ".join(str(x) for x in self.args)

    @override
    def __add__(self, other: Expression) -> Expression:
        if isinstance(other, Addition):
            return Addition.create(*(list(self.args) + list(other.args)))
        return Addition.create(*(list(self.args) + [other]))

    @override
    def __sub__(self, other: Expression) -> Expression:
        if isinstance(other, Addition):
            return Addition.create(*(list(self.args) + list(-x for x in other.args)))
        return Addition.create(*(list(self.args) + [-other]))

    @override
    def __neg__(self) -> Expression:
        return Addition.create(*(-x for x in self.args))

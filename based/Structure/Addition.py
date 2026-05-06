from copy import copy
from typing import override

from based.Structure.CommutativeOperation import CommutativeOperation
from based.Structure.Constant import Constant, IntegerConstant
from based.Structure.Expression import Expression
from based.Structure.SortPriority import SortPriority


class Addition (CommutativeOperation):
    @override
    def sort_key(self) -> tuple[SortPriority, str | int, tuple[Expression, ...]]:
        return SortPriority.OPERATION, "ADD", self.args

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
    def operate_on_constants(left: Constant, right: Constant) -> Constant:
        return left + right

    @override
    @staticmethod
    def is_identity(element: Constant) -> bool:
        return element == Addition.identity()

    def __repr__(self):
        return " + ".join(str(x) for x in self.args)

    def __add__(self, other: Expression) -> Expression:
        if isinstance(other, Addition):
            return Addition.create(*(list(self.args) + list(other.args)))
        return Addition.create(*(list(self.args) + [other]))

    def __sub__(self, other: Expression) -> Expression:
        if isinstance(other, Addition):
            return Addition.create(*(list(self.args) + list(-x for x in other.args)))
        return Addition.create(*(list(self.args) + [-other]))

    def __neg__(self) -> Expression:
        return Addition.create(*(-x for x in self.args))

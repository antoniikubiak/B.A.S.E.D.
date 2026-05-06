from copy import copy
from typing import override

from based.Structure.CommutativeOperation import CommutativeOperation
from based.Structure.Constant import Constant, IntegerConstant
from based.Structure.Expression import Expression
from based.Structure.Multiplication import Multiplication


class Addition (CommutativeOperation):
    @override
    @staticmethod
    def is_absorbing(element: Constant) -> bool:
        return False

    @override
    @staticmethod
    def identity() -> Constant:
        return IntegerConstant(0)

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
        res = copy(self)
        res.args.append(other)
        return res.simplify()

    def __sub__(self, other: Expression) -> Expression:
        res = copy(self)
        res.args.append(-other)
        return res.simplify()

    def __mul__(self, other: Expression) -> Expression:
        return Multiplication([self, other]).simplify()

    def __truediv__(self, other: Expression) -> Expression:
        pass

    def __neg__(self) -> Expression:
        res = copy(self)
        res.args = [-x for x in res.args]
        return res.simplify()


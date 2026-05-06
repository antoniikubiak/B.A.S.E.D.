from copy import copy

from based.Structure.Addition import Addition
from based.Structure.Constant import IntegerConstant, Constant
from based.Structure.CommutativeOperation import CommutativeOperation
from based.Structure.Expression import Expression


class Multiplication(CommutativeOperation):
    @staticmethod
    def operate_on_constants(left: Constant, right: Constant) -> Constant:
        return left * right

    @staticmethod
    def is_identity(element: Constant) -> bool:
        return element == Multiplication.identity()

    @staticmethod
    def is_absorbing(element: Constant) -> bool:
        return element == 0.0

    @staticmethod
    def identity() -> Constant:
        return IntegerConstant(1)

    def __repr__(self):
        return " * ".join(str(x) for x in self.args)

    def __add__(self, other: Expression) -> Expression:
        return Addition([self, other]).simplify()

    def __sub__(self, other: Expression) -> Expression:
        return Addition([self, -other]).simplify()

    def __mul__(self, other: Expression) -> Expression:
        res = copy(self)
        res.args.append(other)
        return res.simplify()

    def __truediv__(self, other: Expression) -> Expression:
        res = copy(self)
        res.args.append(other.__invert__())
        return res.simplify()

    def __neg__(self) -> Expression:
        return self * IntegerConstant(-1)


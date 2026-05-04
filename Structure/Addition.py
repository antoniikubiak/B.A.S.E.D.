from typing import override

from Structure.CommutativeOperation import CommutativeOperation
from Structure.Constant import Constant, IntegerConstant


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

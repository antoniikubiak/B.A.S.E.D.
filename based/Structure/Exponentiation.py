from based.Structure.Constant import Constant, IntegerConstant
from based.Structure.NonCommutativeOperation import NonCommutativeOperation


class Exponentiation (NonCommutativeOperation):
    @staticmethod
    def identity() -> Constant:
        return IntegerConstant(1)

    @staticmethod
    def operate_on_constants(left: Constant, right: Constant) -> Constant:
        return left ** right

    @staticmethod
    def is_identity(element: Constant) -> bool:
        return element == IntegerConstant(1)

    @staticmethod
    def is_absorbing(element: Constant) -> bool:
        return element == IntegerConstant(0)
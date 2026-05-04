
from based.Structure.Constant import IntegerConstant, Constant
from based.Structure.CommutativeOperation import CommutativeOperation


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


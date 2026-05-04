from lark import Transformer

from based.Structure.Addition import Addition
from based.Structure.Constant import FloatConstant, IntegerConstant
from based.Structure.Exponentiation import Exponentiation
from based.Structure.Expression import Expression
from based.Structure.Multiplication import Multiplication
from based.Structure.Variable import Variable


class TreeTransformer(Transformer):
    def float_num(self, items: list[str]) -> FloatConstant:
        return FloatConstant(items[0])

    def int_num(self, items: list[str]) -> IntegerConstant:
        return IntegerConstant(items[0])

    def variable(self, items: list[str]) -> Variable:
        return Variable(items[0])

    def power(self, items: list[Expression]) -> Exponentiation | Expression:
        if len(items) == 1:
            return items[0]
        return Exponentiation(items[0], items[1]).simplify()

    def prod(self, items: list[Expression]) -> Expression:
        return Multiplication(items).simplify()

    def add(self, items: list[Expression]) -> Expression:
        return Addition(items).simplify()
from typing import override

from based.Structure.Expressions.Constant import IntegerConstant, Constant
from based.Structure.Expressions.Operations.CommutativeOperation import CommutativeOperation
from based.Structure.Expressions.Expression import Expression
from based.Structure.Expressions.Operations.Operation import Operation
from based.Structure.Expressions.SortPriority import SortPriority


class Multiplication(CommutativeOperation):
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
    def get_parts(self) -> tuple[Expression, Expression]:
        if isinstance(self.args[0], Constant):
            return Multiplication.create(*self.args[1:]), self.args[0]
        return self, Multiplication.identity()

    @override
    def normalize(self) -> Expression:
        if isinstance(self.args[0], Constant):
            return Multiplication.create(*self.args[1:])
        return self

    @override
    def constant_term(self) -> Constant:
        if isinstance(self.args[0], Constant):
            return self.args[0]
        return IntegerConstant.create(1)

    @override
    def sort_key(self) -> tuple[SortPriority, str | int, tuple]:
        return SortPriority.OPERATION, "MUL", tuple(arg.sort_key() for arg in self.args)

    @override
    @staticmethod
    def operate_on_constants(left: Constant, right: Constant) -> Expression:
        return left * right

    @override
    @staticmethod
    def is_identity(element: Constant) -> bool:
        return element == Multiplication.identity()

    @override
    @staticmethod
    def is_absorbing(element: Constant) -> bool:
        return element == IntegerConstant.create(0)

    @override
    @staticmethod
    def identity() -> Constant:
        return IntegerConstant.create(1)

    @override
    def diff(self, var: str) -> Expression:
        #(fgh)' = f'gh + fg'h + fgh' and the same for more vars

        from based.Structure.Expressions.Operations.Addition import Addition

        derivatives = []

        for i in range(len(self.args)):
            current_args = list(self.args)
            current_args[i] = self.args[i].diff(var)

            new_mult = Multiplication.create(*current_args)
            derivatives.append(new_mult)

        return Addition.create(*derivatives)

    def __repr__(self):
        return " * ".join(str(x) for x in self.args)

    @override
    def __mul__(self, other: Expression) -> Expression:
        if isinstance(other, Multiplication):
            return Multiplication.create(*(list(self.args) + list(other.args)))
        return Multiplication.create(*(list(self.args) + [other]))

    @override
    def __truediv__(self, other: Expression) -> Expression:
        if isinstance(other, Multiplication):
            return Multiplication.create(*(list(self.args) + list(~x for x in other.args)))
        return Multiplication.create(*(list(self.args) + [~other]))

    @override
    def __neg__(self) -> Expression:
        return self * IntegerConstant.create(-1)

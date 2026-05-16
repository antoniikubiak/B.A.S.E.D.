from abc import abstractmethod
from typing import Any, Self

from based.Structure.SimplifiableExpression import SimplifiableExpression


class EvaluableExpression(SimplifiableExpression):
    """
    Represents a node that can be eventually evaluated to produce a value.
    """

    @abstractmethod
    def __neg__(self) -> EvaluableExpression:
        pass

    def normalize(self) -> EvaluableExpression:
        """
        Extracts the symbolic part of the term, stripping away constant coefficients.
        :return: The normalized symbolic `Expression`.
        """
        return self

    def constant_term(self) -> 'Constant':
        """
        Extracts the numeric coefficient of the expression.
        :return: The `Constant` representing the coefficient, defaulting to 1.
        """
        from based.Structure.Expressions.EvaluableConstant import IntegerConstant
        return IntegerConstant.create(1)

    def __invert__(self) -> EvaluableExpression:
        from based.Structure.Expressions.Operations.Exponentiation import Exponentiation
        from based.Structure.Expressions.EvaluableConstant import IntegerConstant
        return Exponentiation.create(self, IntegerConstant.create(-1))

    def __add__(self, other: EvaluableExpression) -> EvaluableExpression:
        from based.Structure.Expressions.Operations.Addition import Addition
        return Addition.create(self, other)

    def __sub__(self, other: EvaluableExpression) -> EvaluableExpression:
        from based.Structure.Expressions.Operations.Addition import Addition
        return Addition.create(self, -other)

    def __mul__(self, other: EvaluableExpression) -> EvaluableExpression:
        from based.Structure.Expressions.Operations.Multiplication import Multiplication
        return Multiplication.create(self, other)

    def __truediv__(self, other: EvaluableExpression) -> EvaluableExpression:
        from based.Structure.Expressions.Operations.Multiplication import Multiplication
        return Multiplication.create(self, ~other)

    @abstractmethod
    def diff(self, var: 'Variable') -> EvaluableExpression:
        pass

    def substitute(self, var: 'Variable', new_expr: 'EvaluableExpression') -> EvaluableExpression | SimplifiableExpression:
        from based.Structure.Expressions.Variable import Variable

        if isinstance(self, Variable) and self.name == var.name:
            return new_expr

        if hasattr(self, 'args') and self.args:
            substituted_args = [arg.substitute(var, new_expr) for arg in self.args]

            if hasattr(self, 'create'):
                return self.create(*substituted_args)
            else:
                return type(self)(*substituted_args)

        return self

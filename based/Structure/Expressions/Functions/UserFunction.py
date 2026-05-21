from typing import override

from based.Structure.Expressions.EvaluableConstant import EvaluableConstant
from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from based.Structure.Expressions.Functions.CallableFunction import CallableFunction
from based.Structure.Expressions.SortPriority import SortPriority
from based.Structure.Expressions.Variable import Variable
from based.Structure.ParamList import ParamWithoutTypeList


class UserFunction(CallableFunction):
    @override
    def get_derivative_formula(self, position: int) -> EvaluableExpression:
        if position >= len(self.params) or position < 0:
            raise ValueError(f"Position {position} is out of range.")
        return self.body.diff(self.params.variables[position])


    def evaluate(self, var: 'Variable', val: 'EvaluableConstant') -> EvaluableExpression:
        return self.body.evaluate(var, val)

    def sort_key(self) -> tuple[SortPriority, str | int, tuple]:
        return SortPriority.OTHER, f"FUNC_CALL_{self.name}", self.body.sort_key()

    def __str__(self) -> str:
        return self.body.__str__()

    def __init__(self, identifier: str, body: EvaluableExpression, *args: Variable, **kwargs):
        super().__init__(identifier, body, *args, **kwargs)
        self.name = identifier
        self.body = body
        self.params = ParamWithoutTypeList([x for x in args])

    @override
    def simplify(self) -> EvaluableExpression:
        return self

    @override
    def evaluate_numeric(self, value: list[float]) -> EvaluableConstant:
        """Suppressed function. """

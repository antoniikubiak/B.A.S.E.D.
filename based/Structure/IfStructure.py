from typing import NamedTuple, Callable

from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from based.Structure.Expressions.SortPriority import SortPriority
from based.Structure.Expressions.Variable import Variable
from based.Structure.LogicExpressions.Condition import Condition
from based.Structure.SimplifiableExpression import SimplifiableExpression


class CondExprPair(NamedTuple):
    cond: Condition
    expr: EvaluableExpression

class IfStructure(EvaluableExpression):
    def __map_expressions(self, foo: Callable[[EvaluableExpression], EvaluableExpression]) -> IfStructure:
        pairs = [CondExprPair(c, foo(e)) for c, e in self.cases]
        return IfStructure.create(pairs, foo(self.default))

    def __neg__(self) -> EvaluableExpression:
        return self.__map_expressions(lambda e: -e)


    def diff(self, var: Variable) -> EvaluableExpression:
        """ Caution: the derivative should not be used in partitioning points, since there is no guarantee that function is differentiable there. """
        return self.__map_expressions(lambda e: e.diff(var))

    def simplify(self) -> SimplifiableExpression:
        return self

    def __hash__(self) -> int:
        return hash(('IF', self.cases, self.default))

    def __eq__(self, other: SimplifiableExpression) -> bool:
        if isinstance(other, IfStructure):
            return self.cases == other.cases and self.default == other.default
        return False

    def sort_key(self) -> tuple[SortPriority, str | int, tuple]:
        return SortPriority.IF_ELSE, "IF", (self.cases, self.default)

    def __init__(self, pairs: tuple[CondExprPair, ...], default: EvaluableExpression, *args, **kwargs):
        super().__init__(*pairs, default, *args, **kwargs)
        self.cases = pairs
        self.default = default

    def __repr__(self):
        res = ""
        for cond, expr in self.cases:
            res += f"if ({cond}) then {{ {expr} }} else \n"
        res += f"{{ {self.default} }}"
        return res

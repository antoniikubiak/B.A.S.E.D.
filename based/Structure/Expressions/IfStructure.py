from typing import NamedTuple, Callable, override

from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from based.Structure.Expressions.SortPriority import SortPriority
from based.Structure.Expressions.Variable import Variable
from based.Structure.LogicExpressions.LogicConstant import LogicConstant
from based.Structure.LogicExpressions.LogicExpression import LogicExpression
from based.Structure.SimplifiableExpression import SimplifiableExpression


class CondExprPair(NamedTuple):
    cond: LogicExpression
    expr: EvaluableExpression

class IfStructure(EvaluableExpression):
    def evaluate(self, var: 'Variable', val: 'EvaluableConstant') -> EvaluableExpression:
        return IfStructure.create(
            (CondExprPair(cond.evaluate(var, val), expr.evaluate(var, val)) for cond, expr in self.cases),
            self.default.evaluate(var, val)
        )

    @override
    def __str__(self) -> str:
        res = ""
        for cond, expr in self.cases:
            res += f"({cond}) ? ({expr}) : "

        res += f"({self.default})"
        return res

    def __map_expressions(self, foo: Callable[[EvaluableExpression], EvaluableExpression]) -> IfStructure:
        pairs = [CondExprPair(c, foo(e)) for c, e in self.cases]
        return IfStructure.create(pairs, foo(self.default))

    def __neg__(self) -> EvaluableExpression:
        return self.__map_expressions(lambda e: -e)


    @override
    def diff(self, var: Variable) -> EvaluableExpression:
        """ Caution: the derivative should not be used in partitioning points, since there is no guarantee that function is differentiable there. """
        return self.__map_expressions(lambda e: e.diff(var))

    @override
    def simplify(self) -> SimplifiableExpression:
        new_cases = []

        for c, e in self.cases:
            if not isinstance(c, LogicConstant):
                new_cases.append(CondExprPair(c, e))
            else:
                if c == LogicConstant.create(False):
                    continue
                if c == LogicConstant.create(True):
                    new_cases.append(CondExprPair(c, e))
                    break

        if len(new_cases) == 0:
            return self.default

        if new_cases[-1].cond == LogicConstant.create(True):
            self.cases = tuple(new_cases[:-1])
            self.default = new_cases[-1].expr
            return self

        self.cases = tuple(new_cases)
        return self

    def __hash__(self) -> int:
        return hash(('IF', self.cases, self.default))

    def __eq__(self, other: SimplifiableExpression) -> bool:
        if isinstance(other, IfStructure):
            return self.cases == other.cases and self.default == other.default
        return False

    @override
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

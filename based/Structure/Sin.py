from typing import override
from based.Structure.Expression import Expression
from based.Structure.Constant import IntegerConstant, FloatConstant
import math

from based.Structure.SortPriority import SortPriority


class Sin(Expression):
    @override
    def _simplify(self) -> Expression:
        arg = self.args[0]

        if isinstance(arg, IntegerConstant) or isinstance(arg, FloatConstant):
            val = arg.value
            if val == 0:
                return IntegerConstant.create(0)

        return self

    @override
    def sort_key(self):
        return (SortPriority.FUNCTION, "SIN", self.args[0].sort_key())

    @override
    def diff(self, var: str) -> Expression:
        from based.Structure.Cos import Cos
        # Wzór: sin(u)' = cos(u) * u'
        return Cos.create(self.args[0]) * self.args[0].diff(var)

    @override
    def __eq__(self, other: Expression) -> bool:
        return isinstance(other, Sin) and self.args[0] == other.args[0]

    @override
    def __hash__(self) -> int:
        return hash((type(self), self.args[0]))

    @override
    def __neg__(self) -> Expression:
        from based.Structure.Constant import IntegerConstant
        return self * IntegerConstant.create(-1)

    def __repr__(self):
        return f"sin({self.args[0]})"

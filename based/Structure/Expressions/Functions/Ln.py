from typing import override

from based.Structure.Expressions.Expression import Expression
from based.Structure.Expressions.SortPriority import SortPriority


class Ln(Expression):
    """
    Logarytm naturalny: ln(arg)
    """
    def __init__(self, arg: Expression, **kwargs):
        super().__init__(arg, **kwargs)
        self.args = [arg]

    @classmethod
    def create(cls, arg: 'Expression') -> Expression:
        instance = cls(arg, create_key=cls._CREATE_KEY)
        return instance._simplify()

    @override
    def _simplify(self) -> Expression:
        from based.Structure.Expressions.Constant import IntegerConstant, FloatConstant
        arg = self.args[0]
        if isinstance(arg, (IntegerConstant, FloatConstant)) and arg.value == 1:
            return IntegerConstant.create(0)
        return self

    @override
    def diff(self, var: 'Variable') -> Expression:
        f = self.args[0]
        return f.diff(var) / f

    def __str__(self) -> str:
        return f"ln({self.args[0]})"

    def __eq__(self, other):
        if not isinstance(other, Ln):
            return False
        return self.args[0] == other.args[0]

    def __hash__(self):
        return hash(("Ln", self.args[0]))

    def __neg__(self):
        from based.Structure.Expressions.Constant import IntegerConstant
        return IntegerConstant.create(-1) * self

    @override
    def sort_key(self) -> tuple[SortPriority, str, tuple]:
        return SortPriority.FUNCTION, "LN", self.args[0].sort_key()

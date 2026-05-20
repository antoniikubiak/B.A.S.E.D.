from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from based.Structure.Expressions.SortPriority import SortPriority
from based.Structure.FunctionRegistry import FunctionRegistry


class UserFunctionCall(EvaluableExpression):
    def evaluate(self, var: 'Variable', val: 'EvaluableConstant') -> EvaluableExpression:
        self.args = tuple(a.evaluate(var, val) for a in self.args)

    def __init__(self, name: str, arg: EvaluableExpression, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.args = (arg,)


    def simplify(self) -> EvaluableExpression:
        return self

    def diff(self, var: 'Variable') -> EvaluableExpression:
        registry = FunctionRegistry()
        func_def = registry.get(self.name)

        if not func_def:
            raise ValueError(f"Funkcja {self.name} nie jest zdefiniowana!")

        body = func_def.body

        internal_var = func_def.params.variables[0].var

        inner_diff = self.args[0].diff(var)

        body_diff = body.diff(internal_var)

        substituted_body_diff = body_diff.evaluate(internal_var, self.args[0])

        return substituted_body_diff * inner_diff

    def __neg__(self) -> EvaluableExpression:
        from based.Structure.Expressions.EvaluableConstant import IntegerConstant
        return IntegerConstant.create(-1) * self

    def __str__(self) -> str:
        return f"{self.name}({self.args[0]})"

    def __eq__(self, other):
        if not isinstance(other, UserFunctionCall):
            return False
        return self.name == other.name and self.args == other.args

    def __hash__(self):
        return hash((self.name, self.args[0]))

    def sort_key(self):
        return SortPriority.OTHER, self.name, tuple(arg.sort_key() for arg in self.args)

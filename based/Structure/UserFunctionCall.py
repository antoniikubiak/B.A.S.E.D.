from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from based.Structure.FunctionRegistry import FunctionRegistry


class UserFunctionCall(EvaluableExpression):
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

        substituted_body_diff = body_diff.substitute(internal_var, self.args[0])

        return substituted_body_diff * inner_diff

    def __neg__(self) -> EvaluableExpression:
        from based.Structure.Expressions.EvaluableConstant import IntegerConstant
        return IntegerConstant.create(-1) * self

    def __str__(self) -> str:
        return f"{self.name}({self.args[0]})"

    def __eq__(self, other):
        if not isinstance(other, UserFunctionCall):
            return False
        return self.name == other.name and self.args[0] == other.args[0]

    def __hash__(self):
        return hash((self.name, self.args[0]))

    @property
    def sort_key(self):
        return f"UserFunc:{self.name}:{self.args[0].sort_key if hasattr(self.args[0], 'sort_key') else str(self.args[0])}"

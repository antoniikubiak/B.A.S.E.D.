from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from based.Structure.Expressions.Functions.UserFunction import UserFunction
from based.Structure.Expressions.SortPriority import SortPriority
from based.Structure.FunctionRegistry import FunctionRegistry


class UserFunctionCall(EvaluableExpression):
    def evaluate(self, var: 'Variable', val: 'EvaluableConstant') -> EvaluableExpression:
        self.args = tuple(a.evaluate(var, val) for a in self.args)
        return self

    def __init__(self, name: str, *args: EvaluableExpression, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.name = name
        self.args = args

    def simplify(self) -> EvaluableExpression:
        registry = FunctionRegistry()
        func_def = registry.get(self.name)
        if isinstance(func_def, UserFunction):
            inlined_expr = func_def.body
            for i, arg in enumerate(self.args):
                inlined_expr = inlined_expr.evaluate(func_def.params[i], arg)
            return inlined_expr
        return self

    def diff(self, var: 'Variable') -> EvaluableExpression:
        registry = FunctionRegistry()
        func_def = registry.get(self.name)

        if not func_def:
            raise ValueError(f"Funkcja {self.name} nie jest zdefiniowana!")

        return func_def.diff(var)

    def __neg__(self) -> EvaluableExpression:
        from based.Structure.Expressions.EvaluableConstant import IntegerConstant
        return IntegerConstant.create(-1) * self

    def __str__(self) -> str:
        registry = FunctionRegistry()
        func_def = registry.get(self.name)

        if isinstance(func_def, UserFunction):
            import copy
            inlined_expr = copy.deepcopy(func_def.body)

            for param_var, actual_arg in zip(func_def.params.variables, self.args):
                inlined_expr = inlined_expr.evaluate(param_var, actual_arg)
            return str(inlined_expr)

        arguments_str = ", ".join(str(a) for a in self.args)
        return f"{self.name}({arguments_str})"

    def __eq__(self, other):
        if not isinstance(other, UserFunctionCall):
            return False
        return self.name == other.name and self.args == other.args

    def __hash__(self):
        return hash((self.name, self.args))

    def sort_key(self):
        return SortPriority.OTHER, self.name, tuple(arg.sort_key() for arg in self.args)

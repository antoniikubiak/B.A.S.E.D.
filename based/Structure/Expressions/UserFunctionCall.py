from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from based.Structure.Expressions.Functions.UserFunction import UserFunction
from based.Structure.Expressions.SortPriority import SortPriority
from based.Structure.FunctionDefinition import FunctionDefinition
from based.Structure.FunctionRegistry import FunctionRegistry

_inlining_stack = set()

class UserFunctionCall(EvaluableExpression):
    def evaluate(self, var: 'Variable', val: 'EvaluableConstant') -> EvaluableExpression:
        evaluated_args = tuple(a.evaluate(var, val) for a in self.args)
        result = UserFunctionCall.__new__(UserFunctionCall)
        result.name = self.name
        result.args = evaluated_args
        return result

    def __init__(self, name: str, *args: EvaluableExpression, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.name = name
        self.args = args

    def simplify(self) -> EvaluableExpression:
        simplified_args = tuple(arg.simplify() for arg in self.args)

        registry = FunctionRegistry()
        func_def = registry.get(self.name)

        if func_def is None:
            self.args = simplified_args
            return self

        if isinstance(func_def, FunctionDefinition) or getattr(func_def, "is_compiled", False):
            self.args = simplified_args
            return self

        if self.name in _inlining_stack:
            self.args = simplified_args
            return self

        _inlining_stack.add(self.name)
        try:
            inlined_expr = func_def.body
            for i, arg in enumerate(simplified_args):
                inlined_expr = inlined_expr.evaluate(func_def.params[i], arg)

            return inlined_expr.simplify()

        finally:
            _inlining_stack.remove(self.name)

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

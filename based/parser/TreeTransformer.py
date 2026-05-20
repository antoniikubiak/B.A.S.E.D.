from lark import Transformer

from based.Structure.Expressions.Functions.Ln import Ln
from based.Structure.Expressions.IfStructure import IfStructure, CondExprPair
from based.Structure.Expressions.EvaluableConstant import FloatConstant, IntegerConstant
from based.Structure.Expressions.Operations.Exponentiation import Exponentiation
from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from based.Structure.FunctionDefinition import FunctionDefinition
from based.Structure.LogicExpressions.Condition import Condition
from based.Structure.LogicExpressions.LogicConstant import LogicConstant
from based.Structure.LogicExpressions.LogicOperation import LogicOr, LogicAnd
from based.Structure.ParamWithTypeList import ParamWithTypeList, VariableTypePair
from based.Structure.ReturnType import ReturnType
from based.Structure.Expressions.Variable import Variable
from based.Structure.Expressions.Functions.Sin import Sin
from based.Structure.Expressions.Functions.Cos import Cos
from based.Structure.Expressions.Functions.Tan import Tan


class TreeTransformer(Transformer):
    """
    Transformer to convert the Lark parse tree into B.A.S.E.D. Expression objects.
    """
    def float_num(self, items: list[str]) -> FloatConstant:
        return FloatConstant.create(items[0])

    def int_num(self, items: list[str]) -> IntegerConstant:
        return IntegerConstant.create(items[0])

    def variable(self, items: list[str]) -> Variable:
        return Variable.create(items[0])

    def power(self, items: list[EvaluableExpression]) -> Exponentiation | EvaluableExpression:
        if len(items) == 1:
            return items[0]
        return Exponentiation.create(items[0], items[1])

    def prod(self, items: list[EvaluableExpression]) -> EvaluableExpression:
        from lark import Tree
        def ensure_expr(item):
            if isinstance(item, Tree):
                return item.children[0]
            return item

        res = ensure_expr(items[0])
        for sign, item in zip(items[1::2], items[2::2]):
            actual_item = ensure_expr(item)
            if sign == '*':
                res *= actual_item
            else:
                res /= actual_item
        return res

    def add(self, items: list[EvaluableExpression]) -> EvaluableExpression:
        from lark import Tree
        def ensure_expr(item):
            if isinstance(item, Tree):
                return item.children[0]
            return item

        res = items[0]
        for sign, item in zip(items[1::2], items[2::2]):
            # actual_item = ensure_expr(item)

            if sign == '+':
                res += item
            else:
                res -= item
        return res

    def generate_target(self, items: list[EvaluableExpression | str | ParamWithTypeList]) -> FunctionDefinition:
        if len(items) == 4:
            expression = items[0]
            name = items[1]
            params = items[2]
            return_type = items[3]
        elif len(items) == 3:
            expression = items[0]
            name = items[1]
            params = None
            return_type = items[2]
        else:
            raise TypeError()
        match return_type:
            case 'int':
                return_type = ReturnType.INT
            case 'float':
                return_type = ReturnType.FLOAT
            case 'double':
                return_type = ReturnType.DOUBLE
            case _:
                raise TypeError()

        from based.Structure.FunctionRegistry import FunctionRegistry
        FunctionRegistry().register(FunctionDefinition(name, params, return_type, expression))

        return FunctionDefinition(name, params, return_type, expression)

    def start(self, items):
        return items

    def generate_param_with_type_list(self, items: list[str]) -> ParamWithTypeList:
        vars_list = []
        return_type = ReturnType.DOUBLE
        for var_type, var_name in zip(items[0::2], items[1::2]):
            match var_type:
                case 'int':
                    return_type = ReturnType.INT
                case 'float':
                    return_type = ReturnType.FLOAT
                case 'double':
                    return_type = ReturnType.DOUBLE
                case _:
                    raise TypeError()
            vars_list.append(VariableTypePair(Variable.create(var_name), return_type))
        return ParamWithTypeList(vars_list)

    def function_call(self, items):
        name = str(items[0])
        from lark import Tree
        arg = items[1]

        while isinstance(arg, Tree):
            arg = arg.children[0]

        if name == "sin":
            return Sin.create(arg)
        elif name == "cos":
            return Cos.create(arg)
        elif name == "ln":
            return Ln.create(arg)
        elif name == "tan":
            return Tan.create(arg)
        else:
            #funkcja użytkownika
            from based.Structure.Expressions.UserFunctionCall import UserFunctionCall
            return UserFunctionCall.create(name, arg)

    def if_struct(self, items: list) -> IfStructure:
        default = items[-1]
        items = items[:-1]
        pairs = tuple(CondExprPair(c, e) for c, e in zip(items[::2], items[1::2]))
        return IfStructure.create(pairs, default)

    def logic_or(self, items: list) -> LogicOr:
        return LogicOr.create(*items)

    def logic_and(self, items: list) -> LogicAnd:
        return LogicAnd.create(*items)

    def bool_const(self, items: list) -> LogicConstant:
        return LogicConstant.create(items[0])

    def cond_op(self, items: list) -> Condition:
        return Condition.create(*items)

    def shorthand(self, items):
        shorthand_type = str(items[0])
        idx_name = str(items[1])
        start = int(items[3])
        end = int(items[5])
        expression_template = items[6]

        from based.Structure.Expressions.Variable import Variable
        idx_var = Variable.create(idx_name)

        generated_expressions = []

        for val in range(start, end + 1):
            from based.Structure.Expressions.EvaluableConstant import IntegerConstant
            current_val_node = IntegerConstant.create(val)

            generated_expressions.append(expression_template.evaluate(idx_var, current_val_node))

        if shorthand_type == "sum":
            from based.Structure.Expressions.Operations.Addition import Addition
            return Addition.create(*generated_expressions)
        elif shorthand_type == "prod":
            from based.Structure.Expressions.Operations.Multiplication import Multiplication
            return Multiplication.create(*generated_expressions)

    def negate(self, items: list):
        return -items[0]

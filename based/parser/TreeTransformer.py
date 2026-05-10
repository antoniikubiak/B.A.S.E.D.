from lark import Transformer

from based.Structure.Constant import FloatConstant, IntegerConstant
from based.Structure.Exponentiation import Exponentiation
from based.Structure.Expression import Expression
from based.Structure.FunctionDefinition import FunctionDefinition
from based.Structure.ParamWithTypeList import ParamWithTypeList, VariableTypePair
from based.Structure.ReturnType import ReturnType
from based.Structure.Variable import Variable


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

    def power(self, items: list[Expression]) -> Exponentiation | Expression:
        if len(items) == 1:
            return items[0]
        return Exponentiation.create(items[0], items[1])

    def prod(self, items: list[Expression]) -> Expression:
        res = items[0]
        for sign, item in zip(items[1::2], items[2::2]):
            if sign == '*':
                res *= item
            else:
                res /= item
        return res

    def add(self, items: list[Expression]) -> Expression:
        res = items[0]
        for sign, item in zip(items[1::2], items[2::2]):
            if sign == '+':
                res += item
            else:
                res -= item
        return res

    def generate_target(self, items: list[Expression | str | ParamWithTypeList]) -> FunctionDefinition:
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

        return FunctionDefinition(name, params, return_type, expression)

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

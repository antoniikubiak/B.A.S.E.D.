from enum import Enum
from typing import override

from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from based.Structure.Expressions.EvaluableConstant import IntegerConstant, EvaluableConstant
from based.Structure.Expressions.Operations.Addition import Addition
from based.Structure.Expressions.SortPriority import SortPriority
from based.Structure.LogicExpressions.LogicConstant import LogicConstant
from based.Structure.LogicExpressions.LogicExpression import LogicExpression

class RelationType(Enum):
    LEQ = "<="
    LT = "<"
    EQ = "=="
    NEQ = "!="
    GT = ">"
    GEQ = ">="

    def __str__(self) -> str:
        return self.value

class Condition(LogicExpression):
    def __init__(self, left_expr: EvaluableExpression, rel_op: str | RelationType, right_expr: EvaluableExpression, *args, **kwargs) -> None:
        super().__init__(left_expr, rel_op, right_expr, *args, **kwargs)
        is_rel_op_good = (isinstance(rel_op, str) and rel_op in {"==", "!=", "<", "<=", ">", ">="}) or isinstance(rel_op, RelationType)
        if not is_rel_op_good:
            raise TypeError(f"Relation operator {rel_op} is not supported.")
        self.left_expr = left_expr
        self.rel_op = RelationType(rel_op) if isinstance(rel_op, str) else rel_op
        self.right_expr = right_expr

    @override
    def simplify(self) -> LogicExpression:
        left = self.left_expr - self.right_expr
        right = IntegerConstant.create(0)

        if isinstance(left, EvaluableConstant):
            match self.rel_op:
                case RelationType.LEQ:
                    return LogicConstant.create(left <= right)
                case RelationType.LT:
                    return LogicConstant.create(left < right)
                case RelationType.EQ:
                    return LogicConstant.create(left == right)
                case RelationType.NEQ:
                    return LogicConstant.create(left != right)
                case RelationType.GT:
                    return LogicConstant.create(left > right)
                case RelationType.GEQ:
                    return LogicConstant.create(left >= right)

        if isinstance(left, Addition):
            constant = left.get_leading_constant()
            left -= constant
            right -= constant

        constant = left.constant_term()
        left = left.normalize()
        if constant != IntegerConstant.create(0):
            right /= constant

        self.left_expr = left
        self.right_expr = right
        return self

    @override
    def __invert__(self) -> LogicExpression:
        new_rel_op = RelationType.EQ
        match self.rel_op:
            case RelationType.LEQ:
                new_rel_op = RelationType.GT
            case RelationType.LT:
                new_rel_op = RelationType.GEQ
            case RelationType.EQ:
                new_rel_op = RelationType.NEQ
            case RelationType.NEQ:
                new_rel_op = RelationType.EQ
            case RelationType.GT:
                new_rel_op = RelationType.LEQ
            case RelationType.GEQ:
                new_rel_op = RelationType.LT
            case _:
                raise ValueError(f"Relation operator {self.rel_op} is not supported.")
        return Condition.create(self.left_expr, new_rel_op, self.right_expr)

    @override
    def __and__(self, other: LogicExpression) -> LogicExpression:
        pass

    @override
    def __or__(self, other: LogicExpression) -> LogicExpression:
        pass

    @override
    def __eq__(self, other: LogicExpression) -> bool:
        if isinstance(other, Condition):
            return self.rel_op == other.rel_op and self.right_expr == other.right_expr and self.left_expr == other.left_expr
        return False

    @override
    def __hash__(self) -> int:
        return hash((self.rel_op, self.left_expr, self.right_expr))

    @override
    def sort_key(self) -> tuple[SortPriority, str | int, tuple]:
        return SortPriority.FUNCTION, "COND", (self.rel_op.value, self.left_expr.sort_key(), self.right_expr.sort_key())

    def __repr__(self) -> str:
        return f"{self.left_expr} {str(self.rel_op)} {self.right_expr}"

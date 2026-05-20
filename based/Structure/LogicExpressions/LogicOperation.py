from abc import ABC, abstractmethod
from typing import override

from based.Structure.Expressions.CommutativeMixin import CommutativeMixin
from based.Structure.Expressions.SortPriority import SortPriority
from based.Structure.LogicExpressions.LogicConstant import LogicConstant
from based.Structure.LogicExpressions.LogicExpression import LogicExpression
from based.Structure.SimplifiableExpression import SimplifiableExpression


class LogicOperation(CommutativeMixin[LogicExpression], LogicExpression, ABC):
    args: tuple[LogicExpression, ...]

    def __init__(self, *args: LogicExpression, **kwargs) -> None:
        """
        Initializes a commutative operation with multiple arguments.
        :param args: A variable number of `Expression` objects.
        """
        super().__init__(*args, **kwargs)
        self.args = tuple(args)

    @override
    @staticmethod
    def is_idempotent() -> bool:
        return True

    @override
    def _convert_args_to_normal_form(self) -> None:
        for arg in self.args:
            if ~arg in self.args:
                self.args = (self.__class__.absorbing_element(), )
                return

    @override
    def __hash__(self) -> int:
        return hash((self.__class__.__name__, self.args))

    @override
    def __eq__(self, other: SimplifiableExpression) -> bool:
        if isinstance(other, self.__class__):
            return self.args == other.args
        return False

    @override
    def sort_key(self) -> tuple[SortPriority, str | int, tuple]:
        return SortPriority.OPERATION, self.__class__.__name__, tuple(a.sort_key() for a in self.args)

    @override
    def evaluate(self, var: 'Variable', val: 'EvaluableConstant') -> LogicExpression:
        return self.__class__.create(*(arg.evaluate(var, val) for arg in self.args))


class LogicAnd(LogicOperation):
    @override
    @staticmethod
    def identity() -> LogicExpression:
        return LogicConstant.create(True)

    @override
    @staticmethod
    def absorbing_element() -> LogicExpression:
        return LogicConstant.create(False)

    @override
    @staticmethod
    def _operate_on_constants(left: LogicExpression, right: LogicExpression) -> LogicExpression:
        return left & right

    def __invert__(self) -> LogicExpression:
        return LogicOr.create(*(~p for p in self.args))

    def __and__(self, other: LogicExpression) -> LogicExpression:
        if isinstance(other, LogicAnd):
            return LogicAnd.create(*self.args, *other.args)
        return LogicAnd.create(*self.args, other)

    def __or__(self, other: LogicExpression) -> LogicExpression:
        return LogicOr.create(self, other)

    def __repr__(self) -> str:
        return " & ".join(str(a) for a in self.args)

    @override
    def __str__(self) -> str:
        return " && ".join(str(a) for a in self.args)


class LogicOr(LogicOperation):
    @override
    @staticmethod
    def identity() -> LogicExpression:
        return LogicConstant.create(False)

    @override
    @staticmethod
    def absorbing_element() -> LogicExpression:
        return LogicConstant.create(True)

    @override
    @staticmethod
    def _operate_on_constants(left: LogicExpression, right: LogicExpression) -> LogicExpression:
        return left | right

    def __invert__(self) -> LogicExpression:
        return LogicAnd.create(*(~p for p in self.args))

    def __and__(self, other: LogicExpression) -> LogicExpression:
        return LogicAnd.create(self, other)

    def __or__(self, other: LogicExpression) -> LogicExpression:
        if isinstance(other, LogicOr):
            return LogicOr.create(*self.args, *other.args)
        return LogicOr.create(*self.args, other)

    @override
    def __str__(self) -> str:
        return " || ".join(str(a) for a in self.args)

    def __repr__(self) -> str:
        return " | ".join(str(a) for a in self.args)

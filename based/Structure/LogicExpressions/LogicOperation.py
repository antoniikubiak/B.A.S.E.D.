from abc import ABC, abstractmethod
from typing import override

from based.Structure.Expressions.CommutativeMixin import CommutativeMixin
from based.Structure.LogicExpressions.LogicConstant import LogicConstant
from based.Structure.LogicExpressions.LogicExpression import LogicExpression


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


class LogicAnd(LogicOperation):
    @override
    @staticmethod
    def identity() -> LogicExpression:
        return LogicConstant(True)

    @override
    @staticmethod
    def absorbing_element() -> LogicExpression:
        return LogicConstant(False)

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


class LogicOr(LogicOperation):
    @override
    @staticmethod
    def identity() -> LogicExpression:
        return LogicConstant(False)

    @override
    @staticmethod
    def absorbing_element() -> LogicExpression:
        return LogicConstant(True)

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

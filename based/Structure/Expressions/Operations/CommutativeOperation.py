from abc import ABC, abstractmethod
from typing import override

from based.Structure.Expressions.CommutativeMixin import CommutativeMixin
from based.Structure.Expressions.EvaluableConstant import EvaluableConstant, IntegerConstant
from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from based.Structure.Expressions.Operations.Operation import Operation


class CommutativeOperation(CommutativeMixin[EvaluableExpression], Operation):
    """
    Abstract base for operations where the order of arguments does not matter.
    Manages n-ary argument lists and ensures a unique canonical representation.
    """
    args: tuple[EvaluableExpression, ...]

    def __init__(self, *args: EvaluableExpression, **kwargs) -> None:
        """
        Initializes a commutative operation with multiple arguments.
        :param args: A variable number of `Expression` objects.
        """
        super().__init__(*args, **kwargs)
        self.args = tuple(args)

    @staticmethod
    @abstractmethod
    def get_higher_order_operation() -> type[Operation]:
        """
        Identifies the operation used for gathering terms (e.g., `Addition` returns `Multiplication`).
        :return: The `type` of the higher-order `Operation`.
        """
        pass

    @override
    def __hash__(self) -> int:
        return hash((type(self), self.args))

    @override
    def __eq__(self, other: EvaluableExpression) -> bool:
        if isinstance(other, self.__class__):
            return self.args == other.args
        return False

    @override
    def _convert_args_to_normal_form(self) -> None:
        """
        Groups identical symbolic terms and converts them into higher-order operations.
        :return: None
        """
        term_counts = {}
        for arg in self.args:
            term = arg
            count_change = IntegerConstant.create(1)

            if isinstance(arg, Operation):
                if arg.is_distributive_over(self.__class__):
                    term, count_change = arg.get_parts()
            elif isinstance(arg, EvaluableConstant):
                term = arg
                count_change = IntegerConstant.create(1)

            term_counts[term] = term_counts.get(term, IntegerConstant.create(0)) + count_change

        new_args = []
        for term, count in term_counts.items():
            if count == IntegerConstant.create(1):
                new_args.append(term)
            else:
                new_args.append(self.__class__.get_higher_order_operation().create(term, count))

        self.args = tuple(new_args)

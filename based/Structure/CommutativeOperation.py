from abc import ABC
from typing import override

from based.Structure.Constant import Constant
from based.Structure.Expression import Expression
from based.Structure.Operation import Operation


class CommutativeOperation(Operation, ABC):
    args: tuple[Expression, ...]

    def __init__(self, *args: Expression) -> None:
        self.args = tuple(args)

    @override
    def __hash__(self) -> int:
        return hash((type(self), self.args))

    @override
    def __eq__(self, other: Expression) -> bool:
        if isinstance(other, self.__class__):
            return self.args == other.args
        return False

    def __flatten(self) -> None:
        new_args = list(self.args)
        for arg in self.args:
                if isinstance(arg, self.__class__):
                    new_args += arg.args
                    new_args.remove(arg)
        self.args = tuple(new_args)

    def __fold_constants(self) -> None:
        constant = self.__class__.identity()
        new_args = list(self.args)
        for arg in self.args:
            if isinstance(arg, Constant):
                if self.__class__.is_absorbing(arg):
                    self.args = (arg, )
                    return
                constant = self.__class__.operate_on_constants(constant, arg)
                new_args.remove(arg)

        if not(self.__class__.is_identity(constant)):
            new_args.append(constant)

        self.args = tuple(new_args)

    @override
    def _simplify(self) -> Expression:
        simplified_args = [arg._simplify() for arg in self.args]
        self.args = tuple(simplified_args)

        self.__flatten()
        self.__fold_constants()

        self.args = tuple(sorted(self.args, key=lambda x: x.sort_key()))

        if len(self.args) == 1:
            return self.args[0]

        if len(self.args) == 0:
            return self.__class__.identity()

        return self

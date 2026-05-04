from abc import ABC
from typing import override

from based.Structure.Constant import Constant
from based.Structure.Expression import Expression
from based.Structure.Operation import Operation


class CommutativeOperation(Operation, ABC):
    args: list[Expression]
    def __init__(self, args: list[Expression]) -> None:
        self.args = args


    def flatten(self) -> None:
        new_args = self.args.copy()
        for arg in self.args:
                if isinstance(arg, self.__class__):
                    new_args += arg.args
                    new_args.remove(arg)
        self.args = new_args

    def fold_constants(self) -> None:
        constant = self.__class__.identity()
        new_args = self.args.copy()
        for arg in self.args:
            if isinstance(arg, Constant):
                if self.__class__.is_absorbing(arg):
                    self.args = [arg]
                    return
                constant = self.__class__.operate_on_constants(constant, arg)
                new_args.remove(arg)

        if not(self.__class__.is_identity(constant)):
            new_args.append(constant)

        self.args = new_args

    @override
    def simplify(self) -> Expression:
        for i in range(len(self.args)):
            self.args[i] = self.args[i].simplify()

        self.flatten()
        self.fold_constants()

        if len(self.args) == 1:
            return self.args[0]
        return self




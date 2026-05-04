from typing import override

from based.Structure.Expression import Expression


class Variable(Expression):
    def __init__(self, name):
        self.name = name

    @override
    def simplify(self) -> None:
        pass
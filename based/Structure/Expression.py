from abc import abstractmethod

from based.Structure.Node import Node


class Expression(Node):
    @abstractmethod
    def simplify(self) -> Expression:
        pass
    @abstractmethod
    def __neg__(self) -> Expression:
        pass
    @abstractmethod
    def __invert__(self) -> Expression:
        pass
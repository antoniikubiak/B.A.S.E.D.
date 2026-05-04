from abc import abstractmethod

from based.Structure.Node import Node


class Expression(Node):
    @abstractmethod
    def simplify(self) -> Expression:
        pass
from abc import ABC, abstractmethod

from Structure.Node import Node


class Expression(Node):
    @abstractmethod
    def simplify(self) -> Expression:
        pass
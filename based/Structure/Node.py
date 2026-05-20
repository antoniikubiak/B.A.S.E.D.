from abc import ABC, abstractmethod


class Node(ABC):
    """
    Basic node of tree structure of B.A.S.E.D. code.
    """
    @abstractmethod
    def __str__(self) -> str:
        pass

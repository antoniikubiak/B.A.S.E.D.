from enum import Enum
from functools import total_ordering


@total_ordering
class SortPriority(Enum):
    CONSTANT = 1
    VARIABLE = 2
    FUNCTION = 3
    OPERATION = 4
    SHORTHAND = 5
    IF_ELSE = 6
    OTHER = 7

    def __le__(self, other: SortPriority) -> bool:
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __eq__(self, other: SortPriority) -> bool:
        if self.__class__ is other.__class__:
            return self.value == other.value
        return False

from enum import Enum

class ReturnType(Enum):
    INT = 0
    FLOAT = 1
    DOUBLE = 2

    def __str__(self) -> str:
        return self.name.lower()

from based.Structure.Constant import FloatConstant
import math

class EulerNumber(FloatConstant):
    def __init__(self, create_key=None):
        super().__init__(math.e, create_key=create_key)

    def __str__(self) -> str:
        return "e"

    def __repr__(self) -> str:
        return "EulerNumber()"
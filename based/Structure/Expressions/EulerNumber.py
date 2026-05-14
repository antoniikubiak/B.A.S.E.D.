from based.Structure.Expressions.EvaluableConstant import FloatConstant
import math

class EulerNumber(FloatConstant):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(math.e, **kwargs)

    def __str__(self) -> str:
        return "e"

    def __repr__(self) -> str:
        return "EulerNumber()"

import pytest
from based.Structure.Expressions.EvaluableConstant import IntegerConstant, FloatConstant
from based.Structure.Expressions.Operations.Addition import Addition
from based.Structure.Expressions.Variable import Variable

@pytest.mark.parametrize("cls, args", [
    (IntegerConstant, (5,)),
    (FloatConstant, (5.5,)),
    (Variable, ("x",)),
    (Addition, (IntegerConstant.create(1), IntegerConstant.create(2))),
])
def test_forbidden_instantiation(cls, args):
    with pytest.raises(RuntimeError, match=f"Direct instantiation of {cls.__name__} is forbidden"):
        cls(*args)

import pytest

from based.Structure.Expressions.EvaluableConstant import IntegerConstant
from based.Structure.Expressions.Operations.Addition import Addition
from based.Structure.Expressions.Operations.Exponentiation import Exponentiation
from based.Structure.Expressions.Operations.Multiplication import Multiplication
from based.Structure.Expressions.Variable import Variable

x = Variable.create("x")
y = Variable.create("y")
z = Variable.create("z")
zero = IntegerConstant.create(0)
one = IntegerConstant.create(1)
two = IntegerConstant.create(2)
three = IntegerConstant.create(3)
four = IntegerConstant.create(4)

@pytest.mark.parametrize("input_expr, expected", [
    (Addition.create(x, zero), x),
    (Addition.create(one, x, two), Addition.create(x, three)),
    (Addition.create(x, x, y), Addition.create(y, Multiplication.create(x, two))),
    (Addition.create(x, Addition.create(y, z)), Addition.create(x, y, z)),
    (Addition.create(x, -x), zero),
    (Addition.create(x, one), Addition.create(one, x)),
    (Addition.create(one, two), IntegerConstant.create(3)),

    (Multiplication.create(x, one), x),
    (Multiplication.create(x, zero, y), zero),
    (Multiplication.create(x, two), Multiplication.create(two, x)),
    (Multiplication.create(two, x, three), Multiplication.create(x, IntegerConstant.create(6))),
    (Multiplication.create(x, x, y), Multiplication.create(y, Exponentiation.create(x, two))),
    (Multiplication.create(x, Multiplication.create(y, z)), Multiplication.create(x, y, z)),

    (Exponentiation.create(x, zero), one),
    (Exponentiation.create(x, one), x),
    (Exponentiation.create(one, x), one),
    (Exponentiation.create(two, three), IntegerConstant.create(8)),

    (Multiplication.create(Addition.create(x, x), Multiplication.create(y, ~y)), Multiplication.create(x, two)),
    (Addition.create(x, y, x, y), Addition.create(Multiplication.create(x, two), Multiplication.create(y, two))),
    (Exponentiation.create(Exponentiation.create(x, two), two), Exponentiation.create(x, four)),

    (Addition.create(x, x), Multiplication.create(two, x)),
    (Multiplication.create(x, x), Exponentiation.create(x, two)),
], )
def test_deep_simplification(input_expr, expected):
    assert input_expr == expected

@pytest.mark.parametrize("operation, expected_type, expected_args_count", [
    (x + y, Addition, 2),
    ((x + y) + x, Addition, 2),
    (x - y, Addition, 2),
    (-(x + y), Addition, 2),
    (x - x, IntegerConstant, 0),
    (Addition.create() + x, Variable, 0)
], )
def test_addition_dunder_methods(operation, expected_type, expected_args_count):
    assert isinstance(operation, expected_type)

    if isinstance(operation, Addition):
        assert len(operation.args) == expected_args_count

@pytest.mark.parametrize("operation, expected_type, expected_args_count", [
    (x * y, Multiplication, 2),
    ((x * y) * x, Multiplication, 2),
    (x / y, Multiplication, 2),
    (-x, Multiplication, 2),
    (x * one, Variable, 0),
    (x * zero, IntegerConstant, 0),
],)
def test_multiplication_dunder_logic(operation, expected_type, expected_args_count):
    assert isinstance(operation, expected_type)
    if isinstance(operation, Multiplication):
        assert len(operation.args) == expected_args_count

@pytest.mark.parametrize("expr, expected_constant", [
    (Addition.create(two, x), two),
    (Addition.create(x, y), zero),
    (x + y + one, one),
], )
def test_get_leading_constant(expr, expected_constant):
    if isinstance(expr, Addition):
        assert expr.get_leading_constant() == expected_constant

@pytest.mark.parametrize("expression, expected_type, expected_val", [
    (two * x + three * x, Multiplication, IntegerConstant.create(5)),
    (Addition.create(x, Multiplication.create(x, two)), Multiplication, three),
    (Multiplication.create(x, two) - x, Variable, x),
    (x + x + x, Multiplication, three),
], )
def test_algebraic_gathering(expression, expected_type, expected_val):
    assert isinstance(expression, expected_type)

    if expected_type == Multiplication:
        constants = [a for a in expression.args if isinstance(a, IntegerConstant)]
        assert len(constants) == 1
        assert constants[0] == expected_val
        assert x in expression.args

    elif expected_type == Variable:
        assert expression == expected_val

def test_exponentiation_inversion():
    expr = Exponentiation.create(x, two)
    inv_expr = ~expr
    assert isinstance(inv_expr, Exponentiation)
    assert inv_expr.right == (two * IntegerConstant.create(-1))

@pytest.mark.parametrize("expression, var, expected", [
    (x, x, one),
    (Variable.create("y"), x, zero),
    (IntegerConstant.create(5), x, zero),
    (Addition.create(x, IntegerConstant.create(5)), x, one),
    (Multiplication.create(two, x), x, two),
], )
def test_differentiation(expression, var, expected):
    assert expression.diff(var) == expected

@pytest.mark.parametrize("expression, var, expected", [
    (x * y, x, y),
    (x * x, x, x * two),
    (one / x, x, -(one / Exponentiation.create(x, two))),
], )
def test_multi_op_differentiation(expression, var, expected):
    assert expression.diff(var) == expected

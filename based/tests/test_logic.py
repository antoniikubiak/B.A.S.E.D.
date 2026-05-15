import pytest
from based.Structure.Expressions.EvaluableConstant import IntegerConstant
from based.Structure.Expressions.Operations.Multiplication import Multiplication
from based.Structure.Expressions.Variable import Variable
from based.Structure.LogicExpressions.LogicConstant import LogicConstant
from based.Structure.LogicExpressions.LogicVariable import LogicVariable
from based.Structure.LogicExpressions.LogicOperation import LogicAnd, LogicOr
from based.Structure.LogicExpressions.LogicInversion import LogicInversion
from based.Structure.LogicExpressions.Condition import Condition, RelationType

x = Variable.create("x")
y = Variable.create("y")
a = LogicVariable.create("a")
b = LogicVariable.create("b")
l_true = LogicConstant.create(True)
l_false = LogicConstant.create(False)

@pytest.mark.parametrize("input_expr, expected", [
    (~l_true, l_false),
    (~l_false, l_true),
    (l_true & l_true, l_true),
    (l_true & l_false, l_false),
    (l_true | l_false, l_true),
    (l_false | l_false, l_false),
],)
def test_logic_constant_operations(input_expr, expected):
    assert input_expr == expected

@pytest.mark.parametrize("input_expr, expected", [
    (a & l_true, a),
    (a & l_false, l_false),
    (a | l_false, a),
    (a | l_true, l_true),
    (a & a, a),
    (a & ~a, l_false),
    (a | ~a, l_true),
    (~(a & b), LogicOr.create(~a, ~b)),
    (~(a | b), LogicAnd.create(~a, ~b)),
    (LogicInversion.create(LogicInversion.create(a)), a),
], )
def test_logic_simplification(input_expr, expected):
    assert input_expr == expected

@pytest.mark.parametrize("left, rel, right, expected_left, expected_rel, expected_right", [
    (x + IntegerConstant.create(5), "==", IntegerConstant.create(5), x, RelationType.EQ, IntegerConstant.create(0)),
    (Multiplication.create(x, IntegerConstant.create(2)), ">", IntegerConstant.create(4), x, RelationType.GT, IntegerConstant.create(2)),
], )
def test_condition_simplification_logic(left, rel, right, expected_left, expected_rel, expected_right):
    cond = Condition.create(left, rel, right)
    assert cond.left_expr == expected_left
    assert cond.rel_op == expected_rel
    assert cond.right_expr == expected_right

@pytest.mark.parametrize("left, rel, right, expected_const", [
    (IntegerConstant.create(10), ">", IntegerConstant.create(5), True),
    (IntegerConstant.create(10), "<", IntegerConstant.create(5), False),
    (IntegerConstant.create(5), "==", IntegerConstant.create(5), True),
], )
def test_condition_to_constant(left, rel, right, expected_const):
    cond = Condition.create(left, rel, right).simplify()
    assert isinstance(cond, LogicConstant)
    assert cond.value == expected_const

@pytest.mark.parametrize("operation, expected_type", [
    (a & b, LogicAnd),
    (a | b, LogicOr),
    (~a, LogicInversion),
    ((a & b) | a, LogicOr),
],)
def test_logic_dunder_types(operation, expected_type):
    assert isinstance(operation, expected_type)

@pytest.mark.parametrize("initial_rel, expected_inverted_rel", [
    (RelationType.LT,  RelationType.GEQ),
    (RelationType.LEQ, RelationType.GT),
    (RelationType.EQ,  RelationType.NEQ),
    (RelationType.NEQ, RelationType.EQ),
    (RelationType.GT,  RelationType.LEQ),
    (RelationType.GEQ, RelationType.LT),
], )
def test_condition_inversion(initial_rel, expected_inverted_rel):
    cond = Condition.create(x, initial_rel, y)
    inverted = ~cond

    assert isinstance(inverted, Condition)
    assert inverted.rel_op == expected_inverted_rel
    assert inverted == Condition.create(x, expected_inverted_rel, y)

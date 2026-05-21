import pytest
from based.parser.BasedCompiler import BasedCompiler

def clean_code(code: str) -> str:
    """Helper to remove excess whitespace and clean up strings for easier assertions."""
    return " ".join(code.split())

def test_basic_compilation_no_optimization():
    """Ensures regular functions compile correctly without generating any unexpected temp variables."""
    code = """
    f3(x) := x + 2;
    > x + y as calculate(double x, int y) -> double;
    """
    result = BasedCompiler.compile(code)

    assert "double calculate(double x, int y)" in result
    assert "return" in result
    assert "tmp_" not in result  # No duplicate expressions, so no temp variables should exist

def test_newton_sqrt_preserves_lazy_conditionals():
    """
    Verifies that the conditional expressions in Newton's square root implementation
    remain unoptimized and clean, without dragging lazy branch expressions into global variables.
    """
    code = """
    newton_step(x, S) := 0.5 * (x + S / x);
    > if iterations == 0 then guess else quick_sqrt(newton_step(guess, S), S, iterations - 1) as quick_sqrt(double guess, double S, int iterations) -> double;
    """
    result = BasedCompiler.compile(code)
    cleaned = clean_code(result)

    assert "tmp_" not in result
    assert "?" in cleaned and ":" in cleaned

def test_cse_extraction_on_duplicates():
    """
    Verifies that true duplicate math expressions (like repeated displacement calls)
    are caught and cleanly extracted into exactly one temp variable.
    """
    code = """
    displacement(t, v0, a) := 0.0 + v0 * t + 0.5 * a * t ^ 2;
    > (0.5 * 15.0 * (displacement(time, vx, ax) ^ 2)) + (15.0 * 9.81 * displacement(time, vx, ax)) as total_energy(double time, double vx, double ax) -> double;
    """
    result = BasedCompiler.compile(code)

    assert "double tmp_0 =" in result

    assert "double tmp_1 =" not in result

@pytest.mark.parametrize("invalid_code", [
    "",
    "> as broken() -> int;",
    "> f() as foo() -> int;",
    "> x as foo() -> int;",
])
def test_compiler_syntax_errors(invalid_code):
    """Ensures the Lark parser catches raw syntax anomalies gracefully."""
    with pytest.raises(Exception):
        BasedCompiler.compile(invalid_code)

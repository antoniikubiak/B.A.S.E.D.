from lark import Lark

from based.parser.BasedCompiler import BasedCompiler
from based.parser.ScopeVisitor import ScopeVisitor
from based.parser.TreeTransformer import TreeTransformer

parser = Lark.open('../based/parser/grammar.lark', parser='lalr')

# tree = parser.parse('''
# >x*y+x*y^2+y^2*x+2^4 as foo_3(int x, int y) -> double;
# ''')


code1 = '''
f3(x) := x + 2;
> - x ^ x + y as f1(double x, int y) -> double;
> f1(sin(x), y) as f2(double x) -> double;
> diff(x, 1, sum(n from 1 to 10 : x^n)) as f3() -> int;
> 42.0 as get_answer() -> int;
> x + y as calculate(double x, int y) -> double;
> if x > 0 then 1.0 elif x == 0 then 0.0 else -1.0 as sign_check(float x) -> float;

> (x + 0) * 1 + (y * 0) ^ 2 as complex_math(int x, double y) -> float;

> if (true or (x > 5 and false)) then 
    if complex_math(x, y) == x then 
        (x * 5 - x * 3) / 2 
    else 
        diff(x, 1, x ^ 3)
  elif x != x then 
    sum(i from 1 to 10: i)
  else 
    42.0 
  as optimize_me(double x, double y) -> double;
'''

code2 = """
f1(x) := x;
> f1(x) as f(int x) -> int;
"""
code3 = """> diff(x, 1, ln(x)) as f(int x) -> double;"""

code4 = """
displacement(t, v0, a) := 0.0 + v0 * t + 0.5 * a * t ^ 2;
hypot(x, y) := (x ^ 2 + y ^ 2) ^ 0.5;

> hypot(displacement(time, vx, ax), displacement(time, vy, ay)) as compute_radial_distance(double time, double vx, double ax, double vy, double ay) -> double;
> 2 * compute_radial_distance(time, vx, ax, vy, ay) as double_compute(double time, double vx, double ax, double vy, double ay) -> double;
"""

code_newton_sqrt = """
newton_step(x, S) := 0.5 * (x + S / x);

> if iterations == 0 then guess else quick_sqrt(newton_step(guess, S), S, iterations - 1) as quick_sqrt(double guess, double S, int iterations) -> double;

> if val < 0.0 then 0.0 elif val == 0.0 then 0.0 else quick_sqrt(val / 2.0, val, 8) as newton_sqrt(double val) -> double;
"""

code_cse_test = """
displacement(t, v0, a) := v0 * t + 0.5 * a * t ^ 2;

> (0.5 * 15.0 * (displacement(time, vx, ax) ^ 2)) + (15.0 * 9.81 * displacement(time, vx, ax)) 
  as total_energy(double time, double vx, double ax) -> double;
"""

test = """
exp_taylor(x) := sum(i from 0 to 5 : (x ^ i) / fact(i));

> if n <= 1 then 1.0 else n * fact(n - 1) as fact(int n) -> int;
> exp_taylor(val) as compile_exp(double val) -> double;
"""

print(BasedCompiler.compile(test))

from lark import Lark

from based.parser.TreeTransformer import TreeTransformer

parser = Lark.open('grammar.lark', parser='lalr')

# tree = parser.parse('''
# >x*y+x*y^2+y^2*x+2^4 as foo_3(int x, int y) -> double;
# ''')

tree = parser.parse('''
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
''')

tree = TreeTransformer().transform(tree)
for x in tree:
    print(str(x))
# print(tree)

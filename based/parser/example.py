from lark import Lark

parser = Lark.open('grammar.lark', parser='lalr')
print(parser.parse("""
f(x) := x^2;
> if true then if false then 10 else -10 else f(x) as foo(int x) -> double;
> sum(n from 1 to 10 : n+1 + f(1)) as foo() -> int;
""").pretty())

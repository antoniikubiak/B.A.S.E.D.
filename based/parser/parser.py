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
> sum(n from 1 to 10 : x^n) as f3() -> int;
''')

# print(tree.pretty())
tree = TreeTransformer().transform(tree)
for x in tree:
    print(str(x))
# print(tree)

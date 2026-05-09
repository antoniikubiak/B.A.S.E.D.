from lark import Lark

from based.parser.TreeTransformer import TreeTransformer

parser = Lark.open('grammar.lark', parser='lalr')

tree = parser.parse('''
>x*y+x*y^2+y^2*x as foo_3(int x, int y) -> double;
''')
print(tree.pretty())
tree = TreeTransformer().transform(tree)
print(tree.pretty())

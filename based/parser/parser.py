from lark import Lark

from based.parser.TreeTransformer import TreeTransformer

parser = Lark.open('grammar.lark', parser='lalr')

tree = parser.parse('''
>2+2*2^2 as foo_3() -> double;
''')
print(tree.pretty())
tree = TreeTransformer().transform(tree)
print(tree.pretty())
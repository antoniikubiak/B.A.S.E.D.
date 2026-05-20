from lark import Lark

from based.parser.ScopeVisitor import ScopeVisitor
from based.parser.TreeTransformer import TreeTransformer


class BasedCompiler:
    @staticmethod
    def compile(code: str) -> str:
        parser = Lark.open('grammar.lark', parser='lalr')
        tree = parser.parse(code)
        ScopeVisitor().visit(tree)
        tree = TreeTransformer().transform(tree)
        return str(tree)

from lark import Lark, UnexpectedInput

from based.parser.ScopeVisitor import ScopeVisitor
from based.parser.TreeTransformer import TreeTransformer


class BasedCompiler:
    @staticmethod
    def compile(code: str) -> str:
        parser = Lark.open('grammar.lark', parser='lalr', propagate_positions=True)
        try:
            tree = parser.parse(code)
        except UnexpectedInput as e:
            print(f"Parsing failed!")
            print(f"Line: {e.line}")
            print(f"Column: {e.column}")
            print(f"Character offset: {e.pos_in_stream}")

            print("\nContext:")
            print(e.get_context(code))

        ScopeVisitor().visit(tree)
        tree = TreeTransformer().transform(tree)
        return "".join((str(x) for x in tree))

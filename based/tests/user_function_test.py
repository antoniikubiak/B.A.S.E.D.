from lark import Lark
from based.Structure.Expressions.Variable import Variable
from based.parser.TreeTransformer import TreeTransformer
from based.Structure.FunctionRegistry import FunctionRegistry

# 1. Wczytujemy parser
parser = Lark.open('../parser/grammar.lark', parser='lalr')


def run_session_test(code_block, var_to_diff=Variable.create("x")):
    print(f"--- TEST ---")

    FunctionRegistry().clear()

    raw_tree = parser.parse(code_block)

    transformed_items = TreeTransformer().transform(raw_tree)

    main_target = transformed_items[-1]

    expr = main_target.body
    print(f"Wyrażenie końcowe po transformacji: {expr}")

    derivation = expr.diff(var_to_diff)

    print(f"Pochodna końcowa po '{var_to_diff}': {derivation}")
    print("=" * 30)


if __name__ == "__main__":
    sesja_wielofunkcyjna = """
        > x * x + y as f1(double x, int y) -> double;
        > f1(sin(x), y) as f2(double x) -> double;
        """

    run_session_test(sesja_wielofunkcyjna)

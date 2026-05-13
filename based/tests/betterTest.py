from lark import Lark

from based.Structure.Expressions.Variable import Variable
from based.parser.TreeTransformer import TreeTransformer

# 1. Definiujemy gramatykę (wczytujemy z pliku)
parser = Lark.open('../parser/grammar.lark', parser='lalr')

# 2. Twój kod wejściowy - tutaj wpisujemy co chcemy zróżniczkować
# Używamy nowej składni: diff(funkcja, rzad, zmienna)
input_code = """
> x * sin(x) as test_func(double x) -> double;
"""


def run_test(code, var_to_diff=Variable.create("x")):
    print(f"--- TEST: {code.strip()} ---")

    # KROK A: Parsowanie (Tekst -> Surowe drzewo Larka)
    raw_tree = parser.parse(code)

    # KROK B: Transformacja (Drzewo Larka -> Twoje obiekty Expression)
    # transformer.transform zwraca listę obiektów (wyników reguł 'target')
    transformed_items = TreeTransformer().transform(raw_tree)

    # Wyciągamy definicję funkcji (pierwszy element z listy)
    func_definition = transformed_items[0]

    # KROK C: Pobieramy wyrażenie ze środka definicji
    expr = func_definition.body
    print(f"Wyrażenie po transformacji: {expr}")

    # KROK D: Różniczkowanie!
    derivation = expr.diff(var_to_diff)

    print(f"Pochodna po '{var_to_diff}': {derivation}")
    print("-" * 30)


if __name__ == "__main__":
    # Test 1: Iloczyn z trygonometrią
    run_test("> x * sin(x) as f1(double x) -> double;")

    # Test 2: Funkcja złożona (Chain Rule) - wymaga sprawnego Sin i Exponentiation
    run_test("> sin(x^2) as f2(double x) -> double;")

    # Test 3: Coś trudniejszego
    run_test("> sin(x) * cos(x) as f3(double x) -> double;")

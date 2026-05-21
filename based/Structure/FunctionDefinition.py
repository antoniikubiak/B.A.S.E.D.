from collections import Counter
from typing import override

from based.Structure.Expressions.EvaluableConstant import EvaluableConstant
from based.Structure.Expressions.EvaluableExpression import EvaluableExpression
from based.Structure.Expressions.Operations.Addition import Addition
from based.Structure.Expressions.Operations.Exponentiation import Exponentiation
from based.Structure.Expressions.Operations.Multiplication import Multiplication
from based.Structure.Expressions.Variable import Variable
from based.Structure.Node import Node
from based.Structure.ParamList import ParamWithTypeList
from based.Structure.ReturnType import ReturnType

def extract_subexpressions(node, counts: Counter, node_map: dict):
    """Recursively walks the AST, tracking node frequencies by their object ID."""
    if node is None:
        return

    # Base types never get extracted into variables
    if isinstance(node, (EvaluableConstant, Variable)):
        return

    # Check if this node is a math operation
    is_math_node = isinstance(node, (Addition, Multiplication, Exponentiation))

    if is_math_node:
        # We use str(node) as the structural signature to identify logical duplicates,
        # but we track the specific object IDs to see how many unique instances exist.
        sig = str(node)
        if sig not in counts:
            counts[sig] = set()
        counts[sig].add(id(node))
        node_map[sig] = node

    # Cleanly traverse down child elements depending on class shape
    if hasattr(node, 'args') and node.args:
        for arg in node.args:
            extract_subexpressions(arg, counts, node_map)
    elif hasattr(node, 'left') or hasattr(node, 'right'):
        if hasattr(node, 'left'): extract_subexpressions(node.left, counts, node_map)
        if hasattr(node, 'right'): extract_subexpressions(node.right, counts, node_map)

    if hasattr(node, 'pairs') and node.pairs:
        for pair in node.pairs:
            extract_subexpressions(pair.condition, counts, node_map)
            extract_subexpressions(pair.expression, counts, node_map)
    if hasattr(node, 'default') and node.default is not None:
        extract_subexpressions(node.default, counts, node_map)

def perform_cse(body: EvaluableExpression) -> tuple[list[tuple[str, str]], str]:
    """
    Identifies mathematical subexpressions and extracts them safely,
    preventing over-extraction of nested sub-components.
    """
    counts = {}
    node_map = {}
    extract_subexpressions(body, counts, node_map)

    # Filter out equations unless they structurally appear more than once
    duplicates = [
        expr_str for expr_str, implicit_ids in counts.items()
        if len(implicit_ids) > 1
    ]

    # Sort from largest mathematical tree to smallest to preserve nested rules
    duplicates.sort(key=len, reverse=True)

    assignments = []
    body_str = str(body)
    var_counter = 0

    for node_str in duplicates:
        # Check how many times this string ACTUALLY appears in the current code state.
        # It searches the main body, plus any previously extracted temp variables.
        occurrences = body_str.count(node_str) + sum(expr.count(node_str) for _, expr in assignments)

        # If it was swallowed by a larger extracted chunk, occurrences will now be 1 (or 0).
        # We only extract if it still legitimately appears multiple times.
        if occurrences > 1:
            var_name = f"tmp_{var_counter}"
            var_counter += 1

            # Replace in the main block body
            body_str = body_str.replace(node_str, var_name)

            # Replace in downstream definitions
            for i in range(len(assignments)):
                assignments[i] = (assignments[i][0], assignments[i][1].replace(node_str, var_name))

            assignments.append((var_name, node_str))

    # Reverse to ensure dependencies are declared before they are used
    assignments.reverse()

    return assignments, body_str

class FunctionDefinition(Node):
    """
    Represents a function definition, including its signature and body.
    """

    @override
    def __str__(self) -> str:
        assignments, optimized_body_str = perform_cse(self.body)

        lines = []
        for var_name, expr_str in assignments:
            lines.append(f"    double {var_name} = {expr_str};")

        param_str = "" if self.params is None else str(self.params)

        c_code = f"{self.returns} {self.name}({param_str}) {{\n"
        if lines:
            c_code += "\n".join(lines) + "\n"
        c_code += f"    return {optimized_body_str};\n"
        c_code += "}\n"

        return c_code

    def __init__(self, name: str, params: ParamWithTypeList, returns: ReturnType, body: EvaluableExpression):
        """
        Initializes a Function object.
        :param name: Identifier for the function.
        :param params: List of typed parameters.
        :param returns: The expected return type.
        :param body: The expression evaluating the function's logic.
        """
        self.name = name
        self.params = params
        self.returns = returns
        self.body = body
    def __repr__(self) -> str:
        return f'{self.returns} {self.name}({"" if self.params is None else str(self.params)}) := {self.body}'

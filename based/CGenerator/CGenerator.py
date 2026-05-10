from based.Structure.FunctionDefinition import FunctionDefinition


class CGenerator:
    """
    Class that handles all C Code generation, including CSE.
    """
    def __init__(self):
        self.memory = {}
        self.statements = []
        self.temp_count = 0

    @staticmethod
    def generate_function_code(function: FunctionDefinition) -> str:
        res = f"{function.returns} {function.name} {function.params} {{ return {function.body}; }} }}"
        return res

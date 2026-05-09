from based.Structure.Function import Function


class CGenerator:
    def __init__(self):
        self.memory = {}
        self.statements = []
        self.temp_count = 0

    @staticmethod
    def generate_function_code(function: Function) -> str:
        res = f"{function.returns} {function.name} {function.params} {{ return {function.body}; }} }}"
        return res

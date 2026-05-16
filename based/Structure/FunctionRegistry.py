class FunctionRegistry:
    #obiekt trzymający funkcje stworzone przez użytkownika
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FunctionRegistry, cls).__new__(cls)
            cls._instance._functions = {}
        return cls._instance

    def register(self, func_definition):
        self._functions[func_definition.name] = func_definition

    def get(self, name):
        return self._functions.get(name)

    def clear(self):
        self._functions.clear()
class BasedError(Exception):
    pass

class DeclarationError(BasedError):
    pass

class SemanticError(BasedError):
    pass

class BasedSyntaxError(BasedError):
    pass

class FatalError(BasedError):
    pass

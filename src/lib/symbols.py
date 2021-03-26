class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type


class KeywordSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)


class VariableSymbol(Symbol):
    def __init__(self, name, type=None):
        super().__init__(name, type=type)

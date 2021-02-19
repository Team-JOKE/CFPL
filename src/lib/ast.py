from lib.token import Token, TokenType


class AST(object):
    pass


class VariableDeclarationBlock(AST):
    def __init__(self, declarations):
        self.declarations = declarations


class DataType(AST):
    def __init__(self, token: Token):
        self.token = token
        self.name = token.value


class Variable(AST):
    def __init__(self, token: Token, type_node: TokenType, value_node):
        self.token = token
        self.type_node = type_node
        self.value_node = value_node


class Assign(AST):
    def __init__(self, left: TokenType.IDENT, right):
        self.left = left
        self.right = right


class Constant(AST):
    def __init__(self, token: TokenType):
        self.token = token
        self.value = token.value

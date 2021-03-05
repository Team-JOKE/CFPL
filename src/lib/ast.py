from lib.token import Token, TokenType


class AST(object):
    pass


class VariableDeclarationBlock(AST):
    def __init__(self, declarations):
        self.declarations = declarations


# class ExecutableBlock(AST):
#    def __init__(self, executables):
#        self.executables = executables


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
    def __init__(self, left, token, right):
        self.left = left
        self.token = token
        self.right = right


class Constant(AST):
    def __init__(self, token: TokenType):
        self.token = token
        self.value = token.value


# ####### UNKNOWN ####### #


class Block(AST):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement


class Compound(AST):
    """Represents a 'START ... STOP' block"""

    def __init__(self):
        self.children = []


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Var(AST):
    """The Var node is constructed out of IDENT token."""

    def __init__(self, token):
        self.token = token
        self.value = token.value
        self.default_value = None


class Program(AST):
    def __init__(self, block):
        self.block = block


class NoOperation(AST):
    pass


class Output(Num):
    pass


class Input(Num):
    pass


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

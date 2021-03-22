from lib.token import Token, TokenType


class AST(object):
    pass


class DataType(AST):
    def __init__(self, value: TokenType):
        self.value = value


class VariableDeclarationBlock(AST):
    def __init__(self, declarations, type_node: DataType):
        self.declarations = declarations
        self.type_node = type_node


class Constant(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value
        self.type = token.type


class VariableDeclaration(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

class While(AST):
    def __init__(self,condition_node,compound_statement_node):
        self.condition_node=condition_node
        self.compound_statement_node=compound_statement_node

class If(AST):
    def __init__(self,condition_node,compound_statement_node):
        self.condition_node=condition_node
        self.compound_statement_node=compound_statement_node

class Cascading_If(AST):
    def __init__ (self, if_nodes):
        self.if_nodes = if_nodes


class Variable(AST):
    """The Var node is constructed out of IDENT token."""

    def __init__(self, token):
        self.token = token
        self.value = token.value


class Assign(AST):
    def __init__(self, left: Variable, right):
        self.left = left
        self.right = right


class AssignCollection(AST):
    def __init__(self, assign_nodes):
        self.assign_nodes = assign_nodes


# ####### UNKNOWN ####### #


class Block(AST):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement


class BinOp(AST):
    def __init__(self, left, op: Token, right):
        self.left = left
        self.op = op
        self.right = right


class Compound(AST):
    """Represents a 'START ... STOP' block"""

    def __init__(self):
        self.children = []


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


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

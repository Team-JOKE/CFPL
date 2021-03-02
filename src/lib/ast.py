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


class Constant(AST):
    def __init__(self, token: Token): 
        self.token = token
        self.value = token
        self.type = token.type
        
class VariableExpression(AST):
    def __init__(self, token: Token,type_node:DataType, value_node:Constant):
        self.token = token
        self.value=token.value
        self.type_node=type_node
        self.value_node=value_node



class Assign(AST):
    def __init__(self, left: TokenType.IDENT, right):
        self.left = left
        self.right = right


<<<<<<< Updated upstream
class Constant(AST):
    def __init__(self, token: TokenType):
        self.token = token
        self.value = token.value
=======
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

>>>>>>> Stashed changes

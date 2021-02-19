from lib.ast import Variable, VariableDeclarationBlock
from lib.token import TokenType


class Interpreter(object):
    def __init__(self, parser):
        self.parser = parser
        self.VARIABLES = {}

    def visit_variable_declaration_block(self, var_decl_node: VariableDeclarationBlock):
        for declaration in var_decl_node.declarations:
            self.visit_variable(declaration)

    def visit_variable(self, variable: Variable):
        # add to symbol table
        name = variable.token.value
        var_type = variable.type_node
        value = None

        if variable.value_node is not None:
            value = variable.value_node.value
        else:
            # default values for each data type
            DEFAULT_VALUES = {
                TokenType.BOOL: "FALSE",
                TokenType.INT: 0,
                TokenType.CHAR: "",
                TokenType.FLOAT: 0.0,
            }

            value = DEFAULT_VALUES.get(var_type)

        self.VARIABLES[name] = (var_type.name, value)

    def interpret(self):
        variable_declaration = self.parser.parse()
        self.visit_variable_declaration_block(variable_declaration)

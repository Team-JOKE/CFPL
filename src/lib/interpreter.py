from lib.ast import Compound, Input, Variable, VariableDeclarationBlock
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

    def input_values(self, variable: Variable):
        # input variables from user executable
        name = variable.token.value
        var_type = variable.type_node
        var = self.VARIABLES[name]
        if var[0] == "INT":
            value = int(input())
        elif var[0] == "FLOAT":
            value = float(input())
        elif var[0] == "CHAR":
            value = input()
        elif var[0] == "BOOL":
            value = bool(input())
        else:
            raise Exception(
                f"Invalid input. Received {variable.type} instead of {var_type}"
            )

        self.VARIABLES[name] = (var[0], value)

    def visit_executable_block(self, exec_node: Compound):
        nodes = exec_node.children
        for node in nodes:
            if isinstance(node, Input):
                variables = node.token.value
                for var in variables:
                    self.input_values(var)

    def interpret(self):
        variable_declaration = self.parser.parse_execute()
        self.visit_variable_declaration_block(variable_declaration.block.declarations)
        self.visit_executable_block(variable_declaration.block.compound_statement)

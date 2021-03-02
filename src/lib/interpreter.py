<<<<<<< Updated upstream
from lib.ast import Variable, VariableDeclarationBlock
=======
from lib.ast import *
>>>>>>> Stashed changes
from lib.token import TokenType
from lib.nodeVisitor import NodeVisitor


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.VARIABLES = {}

    def visit_VariableDeclarationBlock(self, var_decl_node: VariableDeclarationBlock):
        for declaration in var_decl_node.declarations:
            self.visit(declaration)

    def visit_VariableExpression(self, variable: VariableExpression):
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

<<<<<<< Updated upstream
    def interpret(self):
        variable_declaration = self.parser.parse()
        self.visit_variable_declaration_block(variable_declaration)
=======
    def input_values(self, variable: VariableExpression):
        #input variables from user executable
        name = variable.token.value
        var_type = variable.type_node
        var = self.VARIABLES[name]
        if(var[0] == "INT"):
            value = int(input())
        elif(var[0] == "FLOAT"):
            value = float(input())
        elif(var[0] == "CHAR"):
            value = input()
        elif(var[0] == "BOOL"):
            value = bool(input())
        else:
            raise Exception(f"Invalid input. Received {variable.type} instead of {value}")

        self.VARIABLES[name] = (var[0], value)


    def visit_Compound(self,exec_node: Compound):
        nodes = exec_node.children
        for node in nodes:
            self.visit(node)
    
    def visit_Input(self,input_node: Input):
        variables = input_node.token.value
        for var in variables:
            self.input_values(var)

    def visit_Program(self,program_node:Program):
        self.visit(program_node.block)

    def visit_Block(self,block_node:Block):
        self.visit(block_node.declarations)
        self.visit(block_node.compound_statement)

    def interpret(self):
        program = self.parser.parse_execute()
        self.visit(program)
>>>>>>> Stashed changes

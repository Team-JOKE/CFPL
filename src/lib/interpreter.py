from lib.ast import Variable, VariableDeclarationBlock, ExecutableBlock
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
        #input variables from user executable
        name = variable.value
        var_type = variable.type

        var = self.VARIABLES[name]
#        print(var[0] )
#        print(TokenType.INT )

        if(var[0] == "INT"):
            value = int(input())
        elif(var[0] == "FLOAT"):
            value = float(input())
        elif(var[0] == "CHAR"):
            value = input()
        elif(var[0] == "BOOL"):
            value = bool(input())
        else:
            raise Exception("Invalid input. Received {variable.type} instead of {value}")

        self.VARIABLES[name] = (var_type.name, value)
    def visit_executable_block(self,exec_node: ExecutableBlock):
        mult = False
        must_input = False

        for executable in exec_node.executables:
            if(executable.type == TokenType.INPUT):
                must_input = True
            elif(must_input):
                self.input_values(executable)
                must_input = False
            elif(mult):
                self.input_values(executable) # this does not work yet, it's for inputting with multiple variables
            elif(executable.type == TokenType.STOP):
                print("done")

    def interpret(self):
        variable_declaration = self.parser.parse()
        self.visit_variable_declaration_block(variable_declaration)
        var = self.VARIABLES
        execu = self.parser.parse_executable(var)
        self.visit_executable_block(execu)
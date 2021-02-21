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

    def input_mult_values(self, variable: Variable,input_var):
        #input variables from user executable
        name = variable.value
        var_type = variable.type
        var = self.VARIABLES[name]

        if(var[0] == "INT"):
            value = int(input_var)
        elif(var[0] == "FLOAT"):
            value = float(input_var)
        elif(var[0] == "CHAR"):
            value = input_var[0]
        elif(var[0] == "BOOL"):
            value = bool(input_var)
        else:
            raise Exception(f"Invalid input. Received {variable.type} instead of {value}")

        self.VARIABLES[name] = (var[0], value)
    def visit_executable_block(self,exec_node: ExecutableBlock):
        mult_input = False
        must_input = False
        values = None
        count = 0
        mult_count=0
        for executable in exec_node.executables:
            if(executable.type == TokenType.INPUT):
                must_input = True
            elif(executable.type == TokenType.MUL_INPUT):
                mult_input = True
                values = input()
                values = values.split(",")
                count = len(values)

            elif(must_input):
                self.input_values(executable)
                must_input = False
            elif(mult_input):
                if(mult_count < count):
                    self.input_mult_values(executable,values[mult_count])
                    mult_count+=1
                else:
                    mult_input = False
                    mult_count=0

            elif(executable.type == TokenType.STOP):
                print("done")

    def interpret(self):
        variable_declaration = self.parser.parse()
        self.visit_variable_declaration_block(variable_declaration)
        var = self.VARIABLES
        execu = self.parser.parse_executable(var)
        self.visit_executable_block(execu)
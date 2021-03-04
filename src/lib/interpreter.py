from lib.ast import Variable, VariableDeclarationBlock, Compound,Input,Output
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
        self.assign_var_value(var_type.name, value)

    def assign_var_value(self, name, value):
        if name in self.VARIABLES:
            if self.VARIABLES[name] == "INT":
                if not isinstance(value, int):
                    if isinstance(value, float):
                        value = int(value)
                    else:
                        try:
                            value = int(value)
                        except ValueError:
                            raise NameError('Value ' + repr(value) + ' could not assign to int variable ' + repr(name))
            elif self.VARIABLES[name] == "FLOAT":
                if not isinstance(value, float):
                    if isinstance(value, int):
                        value = float(value)
                    else:
                        try:
                            value = float(value)
                        except ValueError:
                            raise NameError('Value ' + repr(value) + ' could not assign to float variable ' + repr(name))
            elif self.VARIABLES[name] == "CHAR":
                if not isinstance(value, str):
                    raise NameError('Value ' + repr(value) + ' could not assign to char variable ' + repr(name))
            elif self.VARIABLES[name] == "BOOL":
                if value not in ["TRUE", "FALSE"]:
                    if isinstance(value, bool):
                        value = "TRUE" if value else "FALSE"
                    else:
                        raise NameError('Value ' + repr(value) + ' could not assign to boolean variable ' + repr(name))
            else:
                raise NameError('Unknown data type ' + self.VARIABLES[name])

        #else: # ignore for now
            #raise NameError(repr(name) + ' variable not defined.')
        return value

    def visit_input_values(self, variable: Variable):
        output = ''
        data_types = []
        for val in variable.token.value:
            data_types.append(self.VARIABLES[val.value])

        inputs = raw_input('please input ' + str(len(variable.token.value)) + ' values separated by comma [' + ', '.join(data_types) + '] >>> ')
        print(inputs)
        values = inputs.split(',')
        if len(values) != len(variable.token.value):
            raise NameError("Invalid inputs.")
        i = 0
        for val in variable.token.value:
            value = values[i]
            data_type = self.VARIABLES[val.value]
            if data_type == "INT":
                value = int(value)
            elif data_type == "FLOAT":
                value = int(value)                
            elif data_type == "CHAR":
                value = value[0] if len(value) > 0 else value
            elif data_type == "BOOL":
                if type(value) is bool:
                    value = 'TRUE' if value else 'FALSE'
                value = str(value)
                if value not in ['TRUE', 'FALSE']:
                    value = 'FALSE'
            else:
                value = str(value)
            self.assign_var_value(val.value, value)
            i = i + 1

        return variable.token.value

    def input_values(self, variable: Variable):
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
        
        self.assign_var_value(var[0], value)
        self.VARIABLES[name] = (var[0], value)

    def output_values(self, variable: Variable):
            #output variables from user executable
            name = variable.token.value
            var_type = variable.type_node
            data_type = self.VARIABLES[name]
            #for val in variable.token.value:
            #    if val == data_type: 
            #        name = val.value
            #        val =self.VARIABLES[name]
            #        data_type = self.VARIABLES[name]
            #        if data_type == "INT":
            #            val = int(val)
            #        elif data_type == "FLOAT":
            #            val = float(val)
            #            
            #        elif data_type == "CHAR":
            #            val = val[0] if len(val) > 0 else val
                        
            #        elif data_type == BOOL:
            #            if type(val) is bool:
            #                val = "TRUE" if val else "FALSE"
            #            val = str(val)
                       
            #            if val not in ["TRUE", "FALSE"]:
            #                val = "FALSE"
                            
            #        else:
            #           val = str(val)
                        
            #    else:
            return str(self.VARIABLES[name][1])

    def visit_executable_block(self,exec_node: Compound):
        nodes = exec_node.children
        for node in nodes:
            if(isinstance(node, Input)):
                variables = node.token.value
                for var in variables:
                    self.input_values(var)
            if(isinstance(node, Output)):
                variables = node.token.value
                s_out = ""
                for var in variables:
                    s_out += self.output_values(var)
                print(s_out)

    def interpret(self):
        variable_declaration = self.parser.parse_execute()
        self.visit_variable_declaration_block(variable_declaration.block.declarations)
        self.visit_executable_block(variable_declaration.block.compound_statement)

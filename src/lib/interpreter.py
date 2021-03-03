from lib.ast import *
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
            if var_type.name == "INT":
                value = int(variable.value_node.value)
            elif var_type.name == "FLOAT":
                value = float(variable.value_node.value)
            elif var_type.name == "CHAR":
                value = variable.value_node.value[1:len(variable.value_node.value)-1]
            else:
                if variable.value_node.value == "TRUE":
                    value=True
                else:
                    value=False
        else:
            # default values for each data type
            DEFAULT_VALUES = {
                TokenType.BOOL: "FALSE",
                TokenType.INT: 0,
                TokenType.CHAR: "",
                TokenType.FLOAT: 0.0,
            }

            value = DEFAULT_VALUES.get(var_type)
        
        self.VARIABLES[name] = [var_type.name, value]

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

        self.VARIABLES[name] = [var[0], value]


    def visit_Compound(self,exec_node: Compound):
        nodes = exec_node.children
        for node in nodes:
            self.visit(node)
    
    def visit_Var(self,var_node:Var):
        return self.VARIABLES[var_node.value][1]

    def visit_Constant(self,constant_node:Constant):
        print("constant value" + constant_node.value)
        if constant_node.type == TokenType.INT:
            return int(constant_node.value)
        elif constant_node.type == TokenType.FLOAT:
            return float (constant_node.value)
        elif constant_node.type == TokenType.CHAR:
            if len(constant_node.value)==2:
                return ''
            else:
                return constant_node.value[1]
        else:
            if constant_node.value == "TRUE":
                return True
            else:
                return False

    def visit_BinOp(self, bin_op_node:BinOp):
        print("visited bin_op" +str(self.visit(bin_op_node.left))+bin_op_node.op.value+str(self.visit(bin_op_node.right)))
        if bin_op_node.op.type == TokenType.PLUS:
            return self.visit(bin_op_node.left) + self.visit(bin_op_node.right)
        elif bin_op_node.op.type == TokenType.MINUS:
            return self.visit(bin_op_node.left) - self.visit(bin_op_node.right)
        elif bin_op_node.op.type == TokenType.MUL:
            return self.visit(bin_op_node.left) * self.visit(bin_op_node.right)
        # change later depending on datatypes
        elif bin_op_node.op.type == TokenType.DIV:
            return self.visit(bin_op_node.left) / self.visit(bin_op_node.right)
        elif bin_op_node.op.type == TokenType.MODULO:
            return self.visit(bin_op_node.left) % self.visit(bin_op_node.right)
        elif bin_op_node.op.type == TokenType.LESS_THAN:
            return bool(self.visit(bin_op_node.left) < self.visit(bin_op_node.right))
        elif bin_op_node.op.type == TokenType.LESS_THAN_EQUAL:
            return bool(self.visit(bin_op_node.left) <= self.visit(bin_op_node.right))
        elif bin_op_node.op.type == TokenType.GREATER_THAN:
            return bool(self.visit(bin_op_node.left) > self.visit(bin_op_node.right))
        elif bin_op_node.op.type == TokenType.GREATER_THAN_EQUAL:
            return bool(self.visit(bin_op_node.left) >= self.visit(bin_op_node.right))
        elif bin_op_node.op.type == TokenType.EQUAL_EQUAL:
            return bool(self.visit(bin_op_node.left) == self.visit(bin_op_node.right))
        elif bin_op_node.op.type == TokenType.NOT_EQUAL:
            return bool(self.visit(bin_op_node.left) != self.visit(bin_op_node.right))
        elif bin_op_node.op.type == TokenType.AND:
            return bool(self.visit(bin_op_node.left) and self.visit(bin_op_node.right))
        elif bin_op_node.op.type == TokenType.OR:
            return bool(self.visit(bin_op_node.left) or self.visit(bin_op_node.right))
        # elif bin_op_node.op == FLOAT_DIV:
        #     return float(self.visit(node.left)) / float(self.visit(node.right))

    def visit_Assign(self, assign_node:Assign):
        print("Assign Begin")
        print(assign_node.left.token)
        print("Assign End")
        self.VARIABLES[assign_node.left.value][1] = self.visit(assign_node.right)

    def visit_Input(self,input_node: Input):
        variables = input_node.token.value
        for var in variables:
            self.input_values(var)

    def visit_Program(self,program_node:Program):
        self.visit(program_node.block)

    def visit_Block(self,block_node:Block):
        self.visit(block_node.declarations)
        self.visit(block_node.compound_statement)

    def visit_AssignCollection(self,assign_collection_node:AssignCollection):
        for node in reversed(assign_collection_node.assign_nodes):
            self.visit(node)

    def interpret(self):
        program = self.parser.parse_execute()
        self.visit(program)

from lib import ast
from lib.nodeVisitor import NodeVisitor
from lib.token import TokenType


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.VARIABLES = {}

    def visit_VariableDeclarationBlock(
        self, var_decl_node: ast.VariableDeclarationBlock
    ):
        for declaration in var_decl_node.declarations:
            self.visit(declaration)
            if isinstance(declaration, ast.VariableDeclaration):
                self.VARIABLES[declaration.value][0] = TokenType(
                    var_decl_node.type_node.value
                ).name
                # default values for each data type
                DEFAULT_VALUES = {
                    TokenType.BOOL: "FALSE",
                    TokenType.INT: 0,
                    TokenType.CHAR: "",
                    TokenType.FLOAT: 0.0,
                }
                print(
                    "DEFAULT VALUE HERE"
                    + str(DEFAULT_VALUES.get(var_decl_node.type_node.value))
                )
                if self.VARIABLES[declaration.value][1] is None:
                    self.VARIABLES[declaration.value][1] = DEFAULT_VALUES.get(
                        var_decl_node.type_node.value
                    )

    def raise_error(self, exception_text: str):
        raise Exception(exception_text)

    def input_values(self, variable: ast.Variable):
        # input variables from user executable
        name = variable.value
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
            raise Exception("Invalid datatype.")

        self.VARIABLES[name] = [var[0], value]

    def visit_Compound(self, exec_node: ast.Compound):
        nodes = exec_node.children
        for node in nodes:
            self.visit(node)

    def visit_Variable(self, var_node: ast.Variable):
        if self.VARIABLES.get(var_node.value) is not None:
            return self.VARIABLES[var_node.value][1]
        else:
            self.raise_error("Undeclared Variable: " + var_node.value)

    def visit_VariableDeclaration(self, var_dec_node: ast.VariableDeclaration):
        if self.VARIABLES.get(var_dec_node.value) is not None:
            self.raise_error("Duplicate Declaration of Variable: " + var_dec_node.value)
        else:
            self.VARIABLES[var_dec_node.value] = [None, None]

    def visit_Constant(self, constant_node: ast.Constant):
        print("constant value" + constant_node.value)
        if constant_node.type == TokenType.INT:
            return int(constant_node.value)
        elif constant_node.type == TokenType.FLOAT:
            return float(constant_node.value)
        elif constant_node.type == TokenType.CHAR:
            if len(constant_node.value) == 2:
                return ""
            else:
                return constant_node.value[1]
        else:
            if constant_node.value == "TRUE":
                return True
            else:
                return False

    def get_type_name(self, type_object: type):
        type_object_name = type_object.__name__
        if type_object_name == "str":
            return "CHAR"
        elif type_object_name == "int":
            return "INT"
        elif type_object_name == "bool":
            return "BOOL"
        elif type_object_name == "float":
            return "FLOAT"

    def visit_BinOp(self, bin_op_node: ast.BinOp):
        left = self.visit(bin_op_node.left)
        right = self.visit(bin_op_node.right)

        print("visit bin_op here" + str(left) + bin_op_node.op.value + str(right))

        left_type: type = type(left)
        right_type: type = type(right)

        left_type_name = self.get_type_name(left_type)
        right_type_name = self.get_type_name(right_type)

        # if types are so different for an operation
        if left_type != right_type:
            if not (
                left_type == int
                and right_type == float
                or left_type == float
                and right_type == int
            ):
                self.raise_error(
                    "Could not perform operation "
                    + bin_op_node.op.value
                    + " on "
                    + left_type_name
                    + " and "
                    + right_type_name
                    + "\n"
                    + str(left)
                    + " "
                    + bin_op_node.op.value
                    + " "
                    + str(right)
                )

        if bin_op_node.op.type == TokenType.PLUS:
            return left + right
        elif bin_op_node.op.type == TokenType.MINUS:
            return left - right
        elif bin_op_node.op.type == TokenType.MUL:
            return left * right
        elif bin_op_node.op.type == TokenType.DIV:
            if left_type == int and right_type == int:
                return left // right
            elif left_type == float or right_type == float:
                return left / right
        elif bin_op_node.op.type == TokenType.MODULO:
            return left % right
        elif bin_op_node.op.type == TokenType.LESS_THAN:
            return left < right
        elif bin_op_node.op.type == TokenType.LESS_THAN_EQUAL:
            return left <= right
        elif bin_op_node.op.type == TokenType.GREATER_THAN:
            return left > right
        elif bin_op_node.op.type == TokenType.GREATER_THAN_EQUAL:
            return left >= right
        elif bin_op_node.op.type == TokenType.EQUAL_EQUAL:
            return left == right
        elif bin_op_node.op.type == TokenType.NOT_EQUAL:
            return left != right
        elif bin_op_node.op.type == TokenType.AND:
            if left_type != bool or right_type != bool:
                self.raise_error(
                    "Could not perform operation "
                    + bin_op_node.op.value
                    + " on "
                    + left_type_name
                    + " and "
                    + right_type_name
                    + "\n"
                    + str(left)
                    + " "
                    + bin_op_node.op.value
                    + " "
                    + str(right)
                )
            return left and right
        elif bin_op_node.op.type == TokenType.OR:
            if left_type != bool or right_type != bool:
                self.raise_error(
                    "Could not perform operation "
                    + bin_op_node.op.value
                    + " on "
                    + left_type_name
                    + " and "
                    + right_type_name
                    + "\n"
                    + str(left)
                    + " "
                    + bin_op_node.op.value
                    + " "
                    + str(right)
                )
            return left or right

    def visit_Assign(self, assign_node: ast.Assign):
        if self.VARIABLES.get(assign_node.left.value) is None:
            self.raise_error("Undeclared Variable: " + assign_node.left.value)
        right_value = self.visit(assign_node.right)
        var_type = self.VARIABLES[assign_node.left.value][0]
        right_value_type = self.get_type_name(type(right_value))
        if var_type != right_value_type:
            self.raise_error(
                "Assignment Error: could not assign type "
                + right_value_type
                + " on variable of type "
                + var_type
                + "\n"
                + str(assign_node.left.value)
                + " = "
                + str(right_value)
            )

        self.VARIABLES[assign_node.left.value][1] = right_value

    def visit_Input(self, input_node: ast.Input):
        variables = input_node.token.value
        for var in variables:
            self.input_values(var)

    def visit_Program(self, program_node: ast.Program):
        self.visit(program_node.block)

    def visit_Block(self, block_node: ast.Block):
        for node in block_node.declarations:
            self.visit(node)
        self.visit(block_node.compound_statement)

    def visit_AssignCollection(self, assign_collection_node: ast.AssignCollection):
        for node in reversed(assign_collection_node.assign_nodes):
            self.visit(node)

    def visit_executable_block(self, exec_node: ast.Compound):
        nodes = exec_node.children
        for node in nodes:
            if isinstance(node, ast.Input):
                variables = node.token.value
                for var in variables:
                    self.input_values(var)

    def visit_While(self, while_node:ast.While):
        condition = self.visit(while_node.condition_node)
        if type(condition) != bool:
            print("Invalid condition for while loop")
            return
        while(self.visit(while_node.condition_node)):
            self.visit(while_node.compound_statement_node)

    def interpret(self):
        program = self.parser.parse_execute()
        self.visit(program)

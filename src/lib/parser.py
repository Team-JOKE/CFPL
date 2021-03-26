from lib import ast
from lib.lexer import Lexer
from lib.token import Token, TokenType


class Parser(object):
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.previous_token: Token = None

    def raise_error(self, suppposed_type, received_type,additional_string=""):
        raise Exception(
            f"Parse Error {received_type} instead of {suppposed_type} current token is {self.current_token} {additional_string}"
        )

    def eat(self, token_type:TokenType, error_string=""):
        if self.current_token is not None and self.current_token.type == token_type:
            self.previous_token = self.current_token
            self.current_token = self.lexer.get_next_token()
        else:
            if self.current_token is not None:
                self.raise_error(token_type.name, self.current_token.type.name+" ",additional_string=error_string)
            else:
                raise Exception("Parse error: "+error_string)

    def variable_declaration(self):
        """Variable: 'VAR' variable_list AS data_type
        | empty"""
        # testing if format follows the grammar
        # VD-> 'VAR' variable_list AS data_type | e
        nodes = []
        self.eat(TokenType.VAR,error_string="Are you missing a \'VAR\' keyword?")
        var_list = self.variable_list()
        self.eat(TokenType.AS,error_string="Are you missing an \'AS\' keyword?" )
        data_type = self.data_type()

        # attach type node to all variables in variable_list
        for var in var_list:
            nodes.append(var)

        return ast.VariableDeclarationBlock(nodes, ast.DataType(data_type))

    def variable_list(self):
        # variable_list -> variable_expression | variable_expression, variable_list
        node = self.variable_expression()
        nodes = [node]

        while self.current_token.type in (TokenType.COMMA, TokenType.EQUAL):
            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
            nodes.append(self.variable_expression())
        return nodes

    def variable_expression(self):
        # variable_expression-> var_name | assignment_statement
        if self.current_token.type == TokenType.IDENT:
            node = ast.VariableDeclaration(self.current_token)
            self.eat(TokenType.IDENT)

        elif self.current_token.type == TokenType.EQUAL:
            prev_tok = self.previous_token
            self.eat(TokenType.EQUAL)
            if prev_tok.type == TokenType.IDENT:
                node = ast.Assign(left=ast.Variable(prev_tok), right=self.expression())
            else:
                raise(Exception("Parse Error: Incorrect variable expression"))
        else:
            raise(Exception("Parse Error: Incorrect variable expression"))

        return node

    def constant(self) -> ast.Constant:
        # for checking constants grammar correctness based on the following rules
        # constant -> int | float | char | boolean
        # int -> num_list
        # float -> num_list . num_list | numlist
        # char -> 'character'|''
        # boolean -> "TRUE"|"FALSE"
        # num_list -> num num_list | e
        constant_token = self.current_token
        if constant_token.type == TokenType.INT:  # check if all characters are digits
            for c in constant_token.value:
                if not c.isdigit():
                    self.raise_error(TokenType.INT, "Invalid Token")
        elif constant_token.type == TokenType.FLOAT:
            dot_index = constant_token.value.find(".")
            if dot_index == -1:  # check like an integer
                for c in constant_token.value:
                    if not c.isdigit():
                        self.raise_error(TokenType.FLOAT, "Invalid Token")
            else:  # check before and after dot
                if len(constant_token.value) == 1:  # constains only dot
                    self.raise_error(TokenType.FLOAT, "Invalid Token")
                for c in constant_token.value[0:dot_index]:
                    if not c.isdigit():
                        self.raise_error(TokenType.FLOAT, "Invalid Token")
                for c in constant_token.value[dot_index + 1 :]:  # noqa
                    if not c.isdigit():
                        self.raise_error(TokenType.FLOAT, "Invalid Token")
        elif constant_token.type == TokenType.CHAR:
            if len(constant_token.value) not in (3, 2):
                self.raise_error(TokenType.CHAR, "Invalid Token")
            if constant_token.value[0] != "'":
                self.raise_error(TokenType.CHAR, "Invalid Token")
            if constant_token.value[len(constant_token.value) - 1] != "'":
                self.raise_error(TokenType.CHAR, "Invalid Token")
        # elif constant_token.type == TokenType.KW_STRING:
        #     string_value = constant_token.value.replace('"', "")
        else:
            bool_value = constant_token.value.replace('"', "")
            if bool_value != "TRUE" and bool_value != "FALSE":
                self.raise_error(TokenType.BOOL, "Invalid Token")

        self.eat(self.current_token.type)

        return ast.Constant(constant_token)

    def data_type(self) -> TokenType:
        if self.current_token is None:
            raise(Exception("Parse Error: Are you missing a Data Type?"))
        token = self.current_token

        if token.type == TokenType.KW_INT:
            self.eat(TokenType.KW_INT)
            return TokenType.INT

        elif token.type == TokenType.KW_CHAR:
            self.eat(TokenType.KW_CHAR)
            return TokenType.CHAR

        elif token.type == TokenType.KW_FLOAT:
            self.eat(TokenType.KW_FLOAT)
            return TokenType.FLOAT

        elif token.type == TokenType.KW_BOOL:
            self.eat(TokenType.KW_BOOL)
            return TokenType.BOOL
        else:
            raise(Exception("Parse Error: Are you missing a Data Type?"))

        node = ast.DataType(token)
        return node

    # not used, parse_execute() is used
    def parse(self):
        # can only handle variable declaration parsing
        node = self.variable_declaration()
        return node

    def block(self):
        """block : declarations compound_statement"""
        declaration_nodes = []
        while (
            self.current_token is not None
            and self.current_token.type != TokenType.START
        ):
            declaration_nodes.append(self.variable_declaration())
        compound_statement_node = self.compound_statement()
        node = ast.Block(declaration_nodes, compound_statement_node)
        return node

    def compound_statement(self):
        """ compound_statement: START statement_list STOP """
        self.eat(TokenType.START,error_string="Are you missing a \'START\' keyword")
        nodes = self.statement_list()
        self.eat(TokenType.STOP,error_string="Are you missing a \'STOP\' keyword")

        root = ast.Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self):
        """statement_list : statement
        | statement statement_list"""

        node = self.statement()

        results = [node]
        while self.current_token is not None and self.current_token.type != TokenType.STOP:

            if self.current_token.type is None:
                break
            statement = self.statement()
            results.append(statement)
            if type(statement).__name__ == "NoOperation":
                break
        return results

    def statement(self):
        """statement : input_statement
        | output_statement
        | assignment_statement_list
        |WHILE
        |IF
        | empty"""

        if self.current_token.type == TokenType.START:
            node = self.compound_statement()
        elif self.current_token.type == TokenType.IDENT:
            node = self.assignment_statement_list()
        elif self.current_token.type == TokenType.OUTPUT:
            self.eat(TokenType.OUTPUT)
            self.eat(TokenType.COLON)
            node = self.output_statement()
        elif self.current_token.type == TokenType.INPUT:
            self.eat(TokenType.INPUT)
            self.eat(TokenType.COLON)
            temp = self.current_token
            temp.value = self.input_statement()
            node = ast.Input(temp)
        elif self.current_token.type == TokenType.WHILE:
            node = self.while_statement()
        elif self.current_token.type == TokenType.IF:
            node = self.cascading_if_statement()
        elif self.current_token.type == TokenType.ELSEIF:
            raise (Exception("ELSEIF statement must be preceeded with an If"))
        elif self.current_token.type == TokenType.ELSE:
            raise (Exception("ELSE statement must be preceeded with an If"))
        else:
            node = self.empty()
        return node

    def cascading_if_statement(self):
        # if_statement->if(expression)compound_statement (elseif_statement)* [else_statement]
        if_nodes = []
        self.eat(TokenType.IF)
        self.eat(TokenType.LPAREN,error_string="Are you missing a left parenthesis? ")
        condition_node = self.expression()
        self.eat(TokenType.RPAREN,error_string="Are you missing a right parenthesis? ")
        compound_statement_node = self.compound_statement()
        if_nodes.append(ast.If(condition_node, compound_statement_node))

        while self.current_token is not None and self.current_token.type == TokenType.ELSEIF:
            self.eat(TokenType.ELSEIF)
            self.eat(TokenType.LPAREN, error_string="Are you missing a left parenthesis? ")
            condition_node = self.expression()
            self.eat(TokenType.RPAREN, error_string="Are you missing a right parenthesis? ")
            compound_statement_node = self.compound_statement()
            if_nodes.append(ast.If(condition_node, compound_statement_node))

        if self.current_token is not None and self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            condition_node = ast.Constant(Token(TokenType.BOOL, "TRUE"))
            compound_statement_node = self.compound_statement()
            if_nodes.append(ast.If(condition_node, compound_statement_node))

        return ast.Cascading_If(if_nodes)

    def while_statement(self):
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LPAREN, error_string="Are you missing a left parenthesis? ")
        condition_node = self.expression()
        self.eat(TokenType.RPAREN, error_string="Are you missing a right parenthesis? ")
        compound_statement_node = self.compound_statement()
        return ast.While(condition_node, compound_statement_node)

    def input_statement(self):
        """input_statement: INPUT: (variable)*"""
        node = ast.Variable(self.current_token)
        var_nodes = [node]  # first ID
        self.eat(TokenType.IDENT,error_string="Are you missing an identifier? ")
        while self.current_token is not None and self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            node = ast.Variable(self.current_token)
            var_nodes.append(node)
            self.eat(TokenType.IDENT,error_string="Are you missing an identifier? ")
            if (
                self.current_token.type == TokenType.STOP
                or self.current_token is None
            ):
                break
        return var_nodes

    def output_statement(self):
        children = []
        if self.current_token is not None and self.current_token.type == TokenType.KW_STRING:
            node = ast.StringExpression(self.current_token)
            self.eat(self.current_token.type)
            children.append(node)
        else:
            if self.current_token is not None:
                node = self.expression()
                children.append(node)
        while self.current_token is not None and self.current_token.type == TokenType.AMPERSAND:
            self.eat(TokenType.AMPERSAND)
            if self.current_token.type == TokenType.KW_STRING:
                node = ast.StringExpression(self.current_token)
                self.eat(self.current_token.type)
                children.append(node)
            else:
                if self.current_token is not None:
                    node = self.expression()
                    children.append(node)
        return ast.Output(children)

    def variable(self):
        node = ast.Variable(self.current_token)
        self.eat(TokenType.IDENT)
        return node

    def assignment_statement_list(self):
        """assignment_statement_list -> variable assignment_phrases
        assignment_phrases-> = variable assignment_phrases | = variable | = expression
        """
        left = self.variable()
        self.eat(TokenType.EQUAL,error_string="Are you missing an equal sign? ")
        right = self.expression()
        node = ast.Assign(left, right)
        nodes = [node]

        while self.current_token is not None and self.current_token.type == TokenType.EQUAL:
            self.eat(TokenType.EQUAL)
            if not isinstance(right, ast.Variable):
                self.raise_error("Variable", type(right).__name__)
            left = right
            right = self.expression()
            nodes.append(ast.Assign(left, right))

        return ast.AssignCollection(nodes)

    def empty(self):
        return ast.NoOperation()

    def expression(self):
        # expression -> or_part (OR or_part)*

        node = self.or_part()
        while self.current_token is not None and self.current_token.type == TokenType.OR:
            token = self.current_token
            self.eat(TokenType.OR)
            node = ast.BinOp(left=node, op=token, right=self.or_part())

        return node

    def or_part(self):
        # or_part -> and_part (AND and_part)*
        node = self.and_part()
        while self.current_token is not None and  self.current_token.type == TokenType.AND:
            token = self.current_token
            self.eat(TokenType.AND)
            node = ast.BinOp(left=node, op=token, right=self.and_part())
        return node

    def and_part(self):
        # and_part -> rel_low_prec_part ((==|<>) rel_low_prec_part)*
        node = self.rel_low_prec_part()
        while self.current_token is not None and self.current_token.type in (TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL):
            token = self.current_token
            self.eat(token.type)
            node = ast.BinOp(left=node, op=token, right=self.rel_low_prec_part())
        return node

    def rel_low_prec_part(self):
        # rel_low_prec_part -> rel_high_prec_part ((<|>|<=|>=) rel_high_prec_part)*
        node = self.rel_high_prec_part()
        while self.current_token is not None and self.current_token.type in (
            TokenType.LESS_THAN,
            TokenType.GREATER_THAN,
            TokenType.LESS_THAN_EQUAL,
            TokenType.GREATER_THAN_EQUAL,
        ):
            token = self.current_token
            self.eat(token.type)
            node = ast.BinOp(left=node, op=token, right=self.rel_high_prec_part())
        return node

    def rel_high_prec_part(self):
        # rel_high_prec_part -> add_part ((+|-) add_part)*
        node = self.add_part()
        while self.current_token is not None and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            self.eat(token.type)
            node = ast.BinOp(left=node, op=token, right=self.add_part())
        return node

    def add_part(self):
        # add_part -> factor ((*|/|%) factor)*
        node = self.factor()
        while self.current_token is not None and self.current_token.type in (
            TokenType.MUL,
            TokenType.DIV,
            TokenType.MODULO,
        ):
            token = self.current_token
            self.eat(token.type)
            node = ast.BinOp(left=node, op=token, right=self.factor())
        return node

    def factor(self):
        """
        factor -> PLUS factor
               | MINUS factor
               | NOT factor
               | CONSTANT
               | LPAREN expr RPAREN
               | variable
        """
        if self.current_token is None:
            raise(Exception("Parse Error: Are you missing a factor? "))
        token = self.current_token
        if token.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            node = ast.UnaryOp(token, self.factor())
            return node
        elif token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            node = ast.UnaryOp(token, self.factor())
            return node
        elif token.type == TokenType.NOT:
            self.eat(TokenType.NOT)
            node = ast.UnaryOp(token, self.factor())
            return node
        elif token.type in (
            TokenType.INT,
            TokenType.FLOAT,
            TokenType.CHAR,
            TokenType.BOOL,
            TokenType.KW_STRING,
        ):
            return self.constant()
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expression()
            self.eat(TokenType.RPAREN)
            return node
        elif self.current_token.type == TokenType.IDENT:
            return self.variable()
        else:
            raise(Exception("Parse Error: Are you missing an operand? "))

    def parse_execute(self):
        """
        block : declarations compound_statement
        declarations : VAR (variable_declaration)+
                     | empty
        variable_declaration : IDENT (COMMA ID [= default value])* AS data_type

        data_type : INT | FLOAT | CHAR | BOOL

        compound_statement : START statement_list STOP
        statement_list : statement
                       | statement statement_list
        statement : compound_statement
                  | assignment_statement
                  | empty
        assignment_statement : variable EQUAL expression
        empty :
        expression : term ((PLUS | MINUS | EQUAL) term)*
        term : factor ((MUL | DIV ) factor)*
        factor : PLUS factor
               | MINUS factor
               | KW_INT
               | KW_FLOAT
               | LPAREN expr RPAREN
        """

        block_node = self.block()
        node = ast.Program(block_node)

        if self.current_token is not None:
            self.error()

        return node

from lib.token import TokenType


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()

    def raise_error(self):
        raise Exception("Error in Parsing")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.raise_error()

    def variable_declaration(self):
        # testing if format follows the grammar
        # VD-> 'VAR' variable_list AS data_type VD | e
        while self.current_token.type != TokenType.START:
            self.eat(TokenType.VAR)
            self.variable_list()
            self.eat(TokenType.AS)
            self.data_type()
            # attach all variable lists to this node

    def variable_list(self):
        # variable_list -> variable_expression | variable_expression, variable_list
        self.variable_expression()
        while self.current_token.type == TokenType.COMMA:
            self.variable_expression()
            # attach all variable expressions to this node

    def variable_expression(self):
        self.current_token = self.lexer.get_next_token()
        self.eat(TokenType.IDENT)
        if self.current_token.type == TokenType.EQUAL:
            self.eat(TokenType.EQUAL)
            self.current_token = self.lexer.get_next_token()
            # value = self.current_token # unused variable
            # construct and return assign node in parse tree/AST

        # construct and return variable node

    def data_type(self):
        token = self.current_token
        if token.type == TokenType.INT_DT:
            self.eat(TokenType.INT_DT)
        elif token.type == TokenType.CHAR_DT:
            self.eat(TokenType.CHAR_DT)
        elif token.type == TokenType.FLOAT_DT:
            self.eat(TokenType.FLOAT_DT)
        elif token.type == TokenType.BOOL_DT:
            self.eat(TokenType.BOOL_DT)

        # construct and return a type node

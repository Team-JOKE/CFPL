from lib.ast import Constant, Variable, VariableDeclarationBlock,ExecutableBlock
from lib.token import Token, TokenType

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def raise_error(self, suppposed_type, received_type):
        raise Exception(
            f"Error in Parsing received {received_type} instead of {suppposed_type}"
        )

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.raise_error(token_type, self.current_token.type)

    def variable_declaration(self):
        # testing if format follows the grammar
        # VD-> 'VAR' variable_list AS data_type VD | e
        nodes = []

        while (
            self.current_token is not None
            and self.current_token.type != TokenType.START  # noqa
        ):
            self.eat(TokenType.VAR)
            var_list = self.variable_list()
            self.eat(TokenType.AS)
            data_type = self.data_type()

            # attach type node to all variables in variable_list
            for var in var_list:
                var.type_node = data_type
                nodes.append(var)

        return VariableDeclarationBlock(nodes)

    def create_execution_block(self, variables):
        #Parsing the executable code into tokens


        checker = False
        Must_Input = False
        nodes = []

        #Checking if START was declared
        if (self.current_token is not None 
            and self.current_token.type == TokenType.START
        ):
            nodes.append(self.current_token)
            self.eat(TokenType.START)
        else:
            raise Exception(
                f"Error in Parsing, did NOT received [START]"
            )

        while(
            self.current_token is not None
            and self.current_token.type != TokenType.STOP
        ):
            #If INPUT Function is called
            if(Must_Input):
                id_token = self.current_token
                self.eat(TokenType.IDENT)

                if (id_token.value in variables ==False):
                    raise Exception("Invalid syntax")
                
                if(self.current_token.type == TokenType.COMMA):
                    nodes.append(Token(TokenType.MUL_INPUT, None))
                else:
                    nodes.append(Token(TokenType.INPUT, None))

                nodes.append(id_token)

                while self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
                    id_token = self.current_token
                    nodes.append(id_token)

                    self.eat(TokenType.IDENT)

                    if (id_token.value in variables == False):
                        raise Exception("Invalid syntax")

            if(self.current_token.type == TokenType.COLON):
                if(checker == True):
                    self.eat(TokenType.COLON)
                    checker = False
                    Must_Input = True
                else:
                    raise Exception("Invalid syntax")

            elif(self.current_token.type == TokenType.INPUT):
                self.eat(TokenType.INPUT)
                checker = True

        #Checking if STOP was declared
        if (self.current_token is not None 
            and self.current_token.type == TokenType.STOP
        ):
            nodes.append(self.current_token)
            self.eat(TokenType.STOP)
        else:
            raise Exception(
                f"Error in Parsing, did NOT received [STOP]"
            )
        return ExecutableBlock(nodes)


    def variable_list(self):
        # variable_list -> variable_expression | variable_expression, variable_list
        node = self.variable_expression()
        nodes = [node]

        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            nodes.append(self.variable_expression())

        return nodes

    def variable_expression(self):
        # variable_expression-> var_name | var_name = value
        id_token = self.current_token
        self.eat(TokenType.IDENT)
        var = Variable(id_token, None, None)

        if self.current_token.type == TokenType.EQUAL:
            self.eat(TokenType.EQUAL)

            # hack for storing only to be changed
            value = self.current_token
            self.current_token = self.lexer.get_next_token()
            var.value_node = Constant(value)

        return var

    def data_type(self) -> TokenType:
        token = self.current_token

        if token.type == TokenType.KW_INT:
            self.eat(TokenType.KW_INT)
            return TokenType.INT

        if token.type == TokenType.KW_CHAR:
            self.eat(TokenType.KW_CHAR)
            return TokenType.CHAR

        if token.type == TokenType.KW_FLOAT:
            self.eat(TokenType.KW_FLOAT)
            return TokenType.FLOAT

        if token.type == TokenType.KW_BOOL:
            self.eat(TokenType.KW_BOOL)
            return TokenType.BOOL

    def parse(self):
        # can only handle variable declaration parsing
        node = self.variable_declaration()
        return node
    def parse_executable(self, variables):
        # can only handle variable executable parsing
        node = self.create_execution_block(variables)
        return node

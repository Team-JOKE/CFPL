from lib.ast import DataType,Program,Block,NoOperation,Input,Output,Compound,Constant, Variable, VariableDeclarationBlock
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
        """ Variable: 'VAR' variable_list AS data_type
                            | empty  """
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
                "Error in Parsing, did NOT received [STOP]"
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

        node =  DataType(token)
        return node

    def parse(self):
        # can only handle variable declaration parsing
        node = self.variable_declaration()
        return node
    def parse_executable(self, variables):
        # can only handle variable executable parsing
        node = self.create_execution_block(variables)
        return node

# ###### UNKNOWN ######## #

    def block(self):
        """block : declarations compound_statement"""
        declaration_nodes = self.variable_declaration()
        compound_statement_node = self.compound_statement()
        node = Block(declaration_nodes, compound_statement_node)
        return node

    def compound_statement(self):
        """ compound_statement: START statement_list STOP """
        self.eat(TokenType.START)
        nodes = self.statement_list()
        self.eat(TokenType.STOP)

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root
    
    def statement_list(self):
        """statement_list : statement 
                          | statement statement_list """

        node = self.statement()

        results = [node]
        while self.current_token.type != TokenType.STOP:
            
            if self.current_token.type == None:
                break
            statement = self.statement()
            results.append(statement)
            if type(statement).__name__ == 'NoOperation':
                break
        return results

    def statement(self):
        """statement : compound_statement
                     | assignment_statement
                     | empty"""

        if self.current_token.type == TokenType.START:
            node = self.compound_statement()
        elif self.current_token.type == TokenType.IDENT:
            node = self.assignment_statement()
        elif self.current_token.type == TokenType.OUTPUT:
            self.eat(TokenType.OUTPUT)
            self.eat(TokenType.COLON)
            self.current_token.value = self.output_statement()
            node = Output(self.current_token)
        elif self.current_token.type == TokenType.INPUT:
            self.eat(TokenType.INPUT)
            self.eat(TokenType.COLON)
            self.current_token.value = self.input_statement()
            node = Input(self.current_token)
        else:
            node = self.empty()
        return node

    def input_statement(self):
        """input_statement: INPUT: (variable)*"""
        node = Variable(self.current_token,self.current_token.type,None)
        var_nodes = [node]  # first ID
        self.eat(TokenType.IDENT)
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            node = Variable(self.current_token,self.current_token.type,None)
            var_nodes.append(node)
            self.eat(TokenType.IDENT)
            if self.current_token.type == TokenType.STOP or self.current_token.type == None:
                break

        return var_nodes

    def output_statement(self):
        """output_statement : expression (& expression)*
        """
        terms = []
        current_pos = self.lexer.pos
        while True:
            if self.current_token.type == TokenType.KW_STRING:
                terms.append(self.expr())
            if self.current_token.type == TokenType.IDENT:
                terms.append(self.variable_expression())
            if self.lexer.pos < current_pos or self.current_token.type != TokenType.AMPERSAND:
                break
            if self.current_token.type == TokenType.AMPERSAND:
                self.eat(TokenType.AMPERSAND)
        return terms

    def assignment_statement(self):
        """assignment_statement : variable EQUAL expression """

        left = self.variable_expression()
        token = self.current_token
        self.eat(TokenType.EQUAL)
        right = self.expr()
        node = Assign(left, token, right)
        return node
    
    def empty(self):
        """An empty production"""
        return NoOperation()
    
    def expression(self):
        """
        expression : term ((PLUS | MINUS | EQUAL) term)*
        """
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS, TokenType.EQUAL):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            elif token.type == TokenType.EQUAL:
                self.eat(TokenType.EQUAL)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in (TokenType.MUL,TokenType.DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node
    
    def factor(self):
        """
           factor : PLUS factor
                  | MINUS factor
                  | KW_INT
                  | KW_FLOAT
                  | LPAREN expr RPAREN
                  | SINGLE_QOUTE expr SINGLE_QOUTE
                  | DOUBLE_QOUTE expr DOUBLE_QOUTE
                  | variable
        """
        token = self.current_token
        if token.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == TokenType.KW_INT:
            self.eat(TokenType.KW_INT)
            return Num(token)
        elif token.type == TokenType.KW_FLOAT:
            self.eat(TokenType.KW_FLOAT)
            return Num(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        else:
            return self.variable_expression()
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
        node = Program(block_node)

        if self.current_token != None:
            self.error()

        return node
from lib.ast import *
from lib.token import Token, TokenType
from lib.lexer import Lexer
class Parser(object):
    def __init__(self, lexer:Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.previous_token:Token = None

    def raise_error(self, suppposed_type, received_type):
        raise Exception(
            f"Error in Parsing received {received_type} instead of {suppposed_type} current token is {self.current_token}"
        )

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.previous_token = self.current_token
            self.current_token = self.lexer.get_next_token()
        else:
            self.raise_error(token_type, self.current_token.type)

    # def variable_declaration(self):
    #     # testing if format follows the grammar
    #     # VD-> 'VAR' variable_list AS data_type VD | e
    #     nodes = []

    #     while (
    #         self.current_token is not None
    #         and self.current_token.type != TokenType.START  # noqa
    #     ):
    #         self.eat(TokenType.VAR)
    #         var_list = self.variable_list()
    #         self.eat(TokenType.AS)
    #         data_type = self.data_type()

    #         # attach type node to all variables in variable_list
    #         for var in var_list:
    #             var.type_node = data_type
    #             nodes.append(var)

    #     return VariableDeclarationBlock(nodes)

    def variable_declaration(self):
        # testing if format follows the grammar
        # VD-> 'VAR' variable_list AS data_type | e
        nodes = []
        self.eat(TokenType.VAR)
        var_list = self.variable_list()
        self.eat(TokenType.AS)
        data_type = self.data_type()

        # attach type node to all variables in variable_list
        for var in var_list:
            nodes.append(var)

        return VariableDeclarationBlock(nodes,DataType(data_type))

    def variable_list(self):
        # variable_list -> variable_expression | variable_expression, variable_list
        node = self.variable_expression()
        nodes = [node]

        while self.current_token.type in (TokenType.COMMA,TokenType.EQUAL):
            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
            nodes.append(self.variable_expression())
        return nodes

    def variable_expression(self):
        # variable_expression-> var_name | assignment_statement
        if self.current_token.type == TokenType.IDENT:
            node = VariableDeclaration(self.current_token)
            self.eat(TokenType.IDENT)

        elif self.current_token.type == TokenType.EQUAL:
            prev_tok = self.previous_token
            self.eat(TokenType.EQUAL)
            node=Assign(left=Variable(prev_tok),right=self.expression())
        
        else:
            self.raise_error("Identifier or Equal", "Invalid Token")

        return node

    def constant(self) -> Constant:
        # for checking constants grammar correctness based on the following rules
        # constant -> int | float | char | boolean
        # int -> num_list
        # float -> num_list . num_list | numlist
        # char -> 'character'|''
        # boolean -> "TRUE"|"FALSE"
        # num_list -> num num_list | e
        constant_token= self.current_token
        if constant_token.type == TokenType.INT: # check if all characters are digits
            for c in constant_token.value:
                if not c.isdigit():
                    self.raise_error(TokenType.INT, "Invalid Token" )
        elif constant_token.type == TokenType.FLOAT:
            dot_index = constant_token.value.find('.')
            if dot_index == -1: #check like an integer
                for c in constant_token.value:
                    if not c.isdigit():
                        self.raise_error(TokenType.FLOAT, "Invalid Token")
            else: # check before and after dot
                if len(constant_token.value) == 1: # constains only dot
                    self.raise_error(TokenType.FLOAT, "Invalid Token")
                for c in constant_token.value[0:dot_index]:
                    if not c.isdigit():
                        self.raise_error(TokenType.FLOAT, "Invalid Token")
                for c in constant_token.value[dot_index+1:]:
                    if not c.isdigit():
                        self.raise_error(TokenType.FLOAT, "Invalid Token")
        elif constant_token.type == TokenType.CHAR:
            if len(constant_token.value) not in (3,2) :
                self.raise_error(TokenType.CHAR, "Invalid Token")
            if constant_token.value[0] != '\'':
                self.raise_error(TokenType.CHAR, "Invalid Token")
            if constant_token.value[len(constant_token.value)-1]!='\'':
                self.raise_error(TokenType.CHAR, "Invalid Token")
        else:
            bool_value=constant_token.value.replace("\"","")
            if bool_value != "TRUE" and bool_value != "FALSE":
                self.raise_error(TokenType.BOOL, "Invalid Token")
        

        self.eat(self.current_token.type)
        
        return Constant(constant_token)
    

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

    def block(self):
        """block : declarations compound_statement"""
        declaration_nodes=[]
        while (
            self.current_token is not None
            and self.current_token.type != TokenType.START
        ):
            declaration_nodes.append(self.variable_declaration())
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
            
            if self.current_token == None:
                break
            statement = self.statement()
            results.append(statement)
            if type(statement).__name__ == 'NoOperation':
                break
        return results

    def statement(self):
        """statement : input_statement
                     | output_statement
                     | assignment_statement_list
                     | empty"""

        if self.current_token.type == TokenType.START:
            node = self.compound_statement()
        elif self.current_token.type == TokenType.IDENT:
            node = self.assignment_statement_list()
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
        node = Variable(self.current_token)
        var_nodes = [node]  # first ID
        self.eat(TokenType.IDENT)
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            node = Variable(self.current_token)
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

    def variable(self):
        node = Variable(self.current_token)
        self.eat(TokenType.IDENT)
        return node

    def assignment_statement_list(self):
        """assignment_statement_list -> variable assignment_phrases 
            assignment_phrases-> = variable assignment_phrases | = variable | = expression 
        """
        print(self.current_token)
        print("assignment statement here")
        left = self.variable()
        self.eat(TokenType.EQUAL)
        right = self.expression()
        node = Assign(left, right)
        nodes=[node]

        while self.current_token.type == TokenType.EQUAL:
            self.eat(TokenType.EQUAL)
            print(self.current_token)
            print("loop here")
            if not isinstance(right,Variable):
                self.raise_error("Variable", type(right).__name__)
            left= right
            right=self.expression()
            nodes.append(Assign(left,right))
        
        return AssignCollection(nodes)
    
    def empty(self):
        """An empty production"""
        return NoOperation()
    
    
    def expression(self):
        #expression -> or_part (OR or_part)*
        node = self.or_part()
        while self.current_token.type == TokenType.OR:
            token = self.current_token
            self.eat(TokenType.OR)
            node= BinOp(left=node,op=token,right=self.or_part())
        return node
    def or_part(self):
        #or_part -> and_part (AND and_part)*
        node = self.and_part()
        while self.current_token.type == TokenType.AND:
            token=self.current_token
            self.eat(TokenType.AND)
            node = BinOp (left=node,op=token,right=self.and_part())
        return node
    def and_part(self):
        #and_part -> rel_low_prec_part ((==|<>) rel_low_prec_part)*
        node = self.rel_low_prec_part()
        while self.current_token.type in (TokenType.EQUAL_EQUAL,TokenType.NOT_EQUAL):
            token=self.current_token
            self.eat(token.type)
            node = BinOp (left=node,op=token,right=self.rel_low_prec_part())
        return node
    
    def rel_low_prec_part(self):
        #rel_low_prec_part -> rel_high_prec_part ((<|>|<=|>=) rel_high_prec_part)*
        node = self.rel_high_prec_part()
        while self.current_token.type in (TokenType.LESS_THAN,TokenType.GREATER_THAN,TokenType.LESS_THAN_EQUAL,TokenType.GREATER_THAN_EQUAL):
            token = self.current_token
            self.eat(token.type)
            node = BinOp (left=node,op=token,right=self.rel_high_prec_part())
        return node

    def rel_high_prec_part(self):
        #rel_high_prec_part -> add_part ((+|-) add_part)*
        node = self.add_part()
        while self.current_token.type in (TokenType.PLUS,TokenType.MINUS):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node,op=token,right=self.add_part())
        return node
    
    def add_part(self):
        #add_part -> factor ((*|/|%) factor)*
        node = self.factor()
        while self.current_token.type in (TokenType.MUL,TokenType.DIV,TokenType.MODULO):
            print("add part here")
            print (self.current_token)
            token=self.current_token
            self.eat(token.type)
            node = BinOp (left=node,op=token,right=self.factor())
        return node
    
    # def expression(self):
    #     """
    #     expression : bool_part ((< | > | ) term)*
    #     """
    #     node = self.term()

    #     while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
    #         token = self.current_token
    #         if token.type == TokenType.PLUS:
    #             self.eat(TokenType.PLUS)
    #         elif token.type == TokenType.MINUS:
    #             self.eat(TokenType.MINUS)
    #         elif token.type == TokenType.OR:
    #             self.eat(TokenType.OR)

    #         node = BinOp(left=node, op=token, right=self.term())
        

    #     return node

    # def term(self):
    #     """term : factor ((MUL | DIV | ) factor)*"""
    #     node = self.factor()

    #     while self.current_token.type in (TokenType.MUL,TokenType.DIV):
    #         token = self.current_token
    #         if token.type == TokenType.MUL:
    #             self.eat(TokenType.MUL)
    #         elif token.type == TokenType.DIV:
    #             self.eat(TokenType.DIV)

    #         node = BinOp(left=node, op=token, right=self.factor())

    #     return node
    
    def factor(self):
        """
           factor -> PLUS factor
                  | MINUS factor
                  | CONSTANT
                  | LPAREN expr RPAREN
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
        elif token.type in (TokenType.INT,TokenType.FLOAT,TokenType.CHAR,TokenType.BOOL):
            return self.constant()
        elif token.type == TokenType.FLOAT:
            return self.constant()
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expression()
            self.eat(TokenType.RPAREN)
            return node
        else:
            print(self.current_token)
            print("self.variable here")
            return self.variable()

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

#Assumes input strings are free of errors
#no operations yet,assign only

VAR,EQUAL,ID,INTEGER,CHAR_DT,BOOL_DT,AS,INT_DT,COMMA,FLOAT,FLOAT_DT, START, CHAR = 'VAR','=','ID','INTEGER','CHAR_DT','BOOL_DT', 'AS', 'INT_DT',',','FLOAT', 'FLOAT_DT', 'START', 'CHAR'

class Token(object):
    # contains type and value of a Token
    def __init__(self,type,value):
        self.type=type
        self.value=value
    
    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

class Lexer(object):
    #handles the tokenization of the input string
    #syntax checking

    def __init__(self,text):
        self.text=text
        self.pos=0
        self.current_char = text[0]
    
    def raiseError(self):
        raise Exception ("Invalid syntax")
    
    def advance(self):
        self.pos+=1
        if self.pos < len(self.text):
            self.current_char=self.text[self.pos]
        else:
            self.current_char=None
    
    def peek(self):
        peek_pos=self.pos + 1
        if peek_pos > len(self.text)-1:
            return None
        else:
            return self.text[peek_pos]

    def get_full_identifier(self):
        RESERVED_WORDS={
            'VAR': Token(VAR,'VAR'),
            'AS': Token(AS,'AS'),
            'INT': Token(INT_DT,'INT_DT'),
            'CHAR': Token(CHAR_DT, 'CHAR'),
            'BOOL':Token(BOOL_DT,'BOOL'),
            'FLOAT': Token(FLOAT_DT,'FLOAT')
        }
        id=''
        while self.current_char is not None and self.current_char.isalnum():
            id+=self.current_char
            self.advance()
            
        #returns a token for a reserved word or a new token of type id if it is not a reserved word
        token = RESERVED_WORDS.get(id,Token(ID,id))
        return token
    
    def get_full_number(self):
        #multi-digit integer or float
        #no syntax error detection yet
        number=''
        while self.current_char is not None and self.current_char.isdigit():
            number+=self.current_char
            self.advance()
        if self.current_char == '.':
            number+=self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                number+=self.current_char
                self.advance()
            return Token(FLOAT, number)
        return Token(INTEGER,number)

    def get_full_char(self):
        #character
        #no error detection yet
        char='\''
        self.advance()
        while self.current_char is not None and self.current_char != '\'':
            char+=self.current_char
            self.advance()
        if self.current_char == '\'':
            char+='\''
            self.advance()
        return Token(CHAR,char)

    def get_full_boolean(self):
        #to be changed, applicable only to variable declaration with no error detection
        boolean = "\""
        self.advance()
        while self.current_char is not None and self.current_char != '\"':
            boolean+=self.current_char
            self.advance()
        if self.current_char == '\"':
            boolean+='\"'
            self.advance()
        return Token(BOOL_DT,boolean)

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            elif self.current_char.isdigit():
                return self.get_full_number()
            elif self.current_char.isalpha():
                return self.get_full_identifier()
            elif self.current_char == ',':
                self.advance()
                return Token(COMMA,',')
            elif self.current_char == '\"':
                return self.get_full_boolean()
            elif self.current_char == '=':
                self.advance()
                return Token(EQUAL,'=')
            else:
                self.raiseError()

class AST(object):
    pass

class VariableDeclarationBlock(AST):
    def __init__(self, declarations):
        self.declarations=declarations

class Variable(AST):
    def __init__(self,token,type_node,value_node):
        self.token=token
        self.type_node=type_node
        self.value_node=value_node

class DataType(AST):
    def __init__(self,token):
        self.token=token
        self.name=token.value

class Assign(AST):
    def __init__(self,left,right):
        self.left = left
        self.right= right

class Constant(AST):
    def __init__(self, token):
        self.token=token
        self.value=token.value

class Parser(object):
    def __init__(self,lexer):
        self.lexer=lexer
        self.current_token=self.lexer.get_next_token()
    
    def raise_error(self,suppposed_type, received_type):
        raise Exception ("Error in Parsing received"+received_type +"instead of" +suppposed_type)
    
    def eat(self,token_type):
        if self.current_token.type == token_type:
            self.current_token=self.lexer.get_next_token()
        else:
            self.raise_error(token_type,self.current_token.type)

    def variable_declaration(self):
        #testing if format follows the grammar
        #VD-> 'VAR' variable_list AS data_type VD | e
        nodes=[]
        while self.current_token is not None and self.current_token.type != START :
            self.eat(VAR)
            var_list= self.variable_list()
            self.eat(AS)
            data_type= self.data_type()
            #attach type node to all variables in variable_list
            for var in var_list:
                var.type_node = data_type
                nodes.append(var)

        return VariableDeclarationBlock(nodes)

    def variable_list(self):
        #variable_list -> variable_expression | variable_expression, variable_list
        node=self.variable_expression()
        nodes=[node]
        while self.current_token.type == COMMA:
            self.eat(COMMA)
            nodes.append(self.variable_expression())
        return nodes
    
    def variable_expression(self):
        #variable_expression-> var_name | var_name = value
        id_token=self.current_token
        self.eat(ID)
        var=Variable(id_token,None,None)
        if self.current_token.type == EQUAL:
            self.eat(EQUAL)
            #hack for storing only to be changed
            value = self.current_token
            self.current_token=self.lexer.get_next_token()
            var.value_node = Constant(value)
        return var

    def data_type(self):
        token = self.current_token
        if token.type == INT_DT:
            self.eat(INT_DT)
        elif token.type == CHAR_DT:
            self.eat(CHAR_DT)
        elif token.type == FLOAT_DT:
            self.eat(FLOAT_DT)
        elif token.type == BOOL_DT:
            self.eat(BOOL_DT)

        return DataType(token)

    def parse(self):
        #can only handle variable declaration parsing
        node = self.variable_declaration()
        return node

class Interpreter(object):
    def __init__(self,parser):
        self.parser=parser
        self.VARIABLES={}

    def visit_variable_declaration_block(self,var_decl_node):
        for declaration in var_decl_node.declarations:
            self.visit_variable(declaration)
    
    def visit_variable(self,variable):
        name=variable.token.value
        var_type=variable.type_node.name
        value=None
        if (variable.value_node is not None):
             value=variable.value_node.value
        else:
            value = "None"
        self.VARIABLES[name]="TYPE: "+var_type+" Value: "+value
    
    def interpret(self):
        variable_declaration=self.parser.parse()
        self.visit_variable_declaration_block(variable_declaration)
        

def main():
    text=input("cfpl>")
    lexer=Lexer(text)
    parser=Parser(lexer)
    interpreter=Interpreter(parser)
    interpreter.interpret()
    print(interpreter.VARIABLES)

if __name__ == '__main__':
    main()
    
    


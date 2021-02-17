#Assumes input strings are free of errors
#no operations yet,assign only

VAR,EQUAL,ID,INTEGER,CHAR_DT,BOOL_DT,AS,INT_DT,COMMA,FLOAT,FLOAT_DT, START = 'VAR','=','ID','INTEGER','CHAR_DT','BOOL_DT', 'AS', 'INT_DT',',','FLOAT', 'FLOAT_DT', 'START'

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
        return Token(CHAR_DT,char)

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

class Parser(object):
    def __init__(self,lexer):
        self.lexer=lexer
        self.current_token=lexer.get_next_token()
    
    def raise_error(self):
        raise Exception ("Error in Parsing")
    
    def eat(self,token_type):
        if self.current_token.type == token_type:
            self.current_token=lexer.get_next_token()
        else:
            self.raise_error()

    def variable_declaration(self):
        #testing if format follows the grammar
        #VD-> 'VAR' variable_list AS data_type VD | e
        while self.current_token.type != START:
            self.eat(VAR)
            self.variable_list()
            self.eat(AS)
            self.data_type()
            #attach all variable lists to this node

    def variable_list(self):
        #variable_list -> variable_expression | variable_expression, variable_list
        self.variable_expression()
        while self.current_token.type == COMMA:
            self.variable_expression()
            #attach all variable expressions to this node
    
    def variable_expression(self):
        self.current_token= self.lexer.get_next_token()
        self.eat(ID)
        if self.current_token.type == EQUAL:
            self.eat(EQUAL)
            self.current_token=self.lexer.get_next_token()
            value = self.current_token
            # construct and return assign node in parse tree/AST
        
        #construct and return variable node
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

        # construct and return a type node

def main():
    text=input("cfpl>")
    lexer=Lexer(text)
    while lexer.current_char is not None:
        print(lexer.get_next_token())
        
        
if __name__ == '__main__':
    main()
    
    


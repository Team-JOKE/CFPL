from lib.token import Token, TokenType

RESERVED_WORDS = {
    "VAR": Token(TokenType.VAR, "VAR"),
    "AS": Token(TokenType.AS, "AS"),
    "INT": Token(TokenType.KW_INT, "KW_INT"),
    "CHAR": Token(TokenType.KW_CHAR, "KW_CHAR"),
    "BOOL": Token(TokenType.KW_BOOL, "KW_BOOL"),
    "FLOAT": Token(TokenType.KW_FLOAT, "KW_FLOAT"),
    "START": Token(TokenType.START, "START"),
    "STOP": Token(TokenType.STOP, "STOP"),
    "INPUT": Token(TokenType.INPUT, "INPUT"),
    "OUTPUT": Token(TokenType.OUTPUT, "OUTPUT"),
    "OR": Token(TokenType.OR, "OR"),
    "AND": Token(TokenType.AND, "AND"),
    "NOT": Token(TokenType.NOT, "NOT"),
    "WHILE": Token(TokenType.WHILE, "WHILE"),
    "IF": Token(TokenType.IF, "IF"),
    "ELSEIF": Token(TokenType.ELSEIF, "ELSEIF"),
    "ELSE": Token(TokenType.ELSE, "ELSE"),
}


class Lexer(object):
    # handles the tokenization of the input string
    # syntax checking

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[0]

    def raiseError(self):
        raise Exception("Invalid syntax at Lexeme: " + self.current_char)

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def get_full_identifier(self) -> Token:

        id = ""
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char=='_'):
            id += self.current_char
            self.advance()

        # returns a token for a reserved word or a new token of type id if it is not a reserved word
        token = RESERVED_WORDS.get(id, Token(TokenType.IDENT, id))
        return token

    def get_full_number(self) -> Token:
        # multi-digit integer or float
        number = ""

        while self.current_char is not None and self.current_char.isdigit():
            number += self.current_char
            self.advance()

        if self.current_char == ".":
            number += self.current_char
            self.advance()

            while self.current_char is not None and self.current_char.isdigit():
                number += self.current_char
                self.advance()
            return Token(TokenType.FLOAT, number)

        return Token(TokenType.INT, number)

    def get_full_char(self) -> Token:
        # character
        char = "'"
        self.advance()

        while self.current_char is not None and self.current_char != "'":
            char += self.current_char
            self.advance()

        if self.current_char == "'":
            char += "'"
            self.advance()

        return Token(TokenType.CHAR, char)

    def get_full_boolean(self) -> Token:
        # advance for starting quotation mark
        self.advance()

        boolean = ""
        while self.current_char is not None and self.current_char != '"':
            boolean += self.current_char
            self.advance()

        self.advance()

        return Token(
            TokenType.BOOL, boolean
        )

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def peek_next(self):
        i = self.pos + 1
        while self.text[i] is not None and self.text[i].isspace():
            i += 1
        return self.text[i]

    def get_comment(self):
        while self.current_char is not None and self.current_char != "\n":
            self.advance()

    def get_full_relational(self):
        token: Token
        if self.current_char == "<":
            if self.peek_next() == "=":
                token = Token(TokenType.LESS_THAN_EQUAL, "<=")
                self.advance()
                self.skip_whitespace()
                self.advance()
            elif self.peek_next() == ">":
                token = Token(TokenType.NOT_EQUAL, "<>")
                self.advance()
                self.skip_whitespace()
                self.advance()
            else:
                token = Token(TokenType.LESS_THAN, "<")
                self.advance()
        else:
            if self.peek_next() == "=":
                token = Token(TokenType.GREATER_THAN_EQUAL, ">=")
                self.advance()
                self.skip_whitespace()
                self.advance()
            else:
                token = Token(TokenType.GREATER_THAN, ">")
                self.advance()
        return token

    def get_next_token(self) -> Token:
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            elif self.current_char.isdigit() or self.current_char == ".":
                return self.get_full_number()
            elif self.current_char.isalpha() or self.current_char == '_':
                return self.get_full_identifier()
            elif self.current_char == "\\":
                self.advance()
                if self.current_char == "n":
                    self.advance()
                    if self.current_char == "*":
                        self.get_comment()
                else:
                    self.raiseError()
            elif self.current_char == "'":
                return self.get_full_char()
            elif self.current_char == ",":
                self.advance()
                return Token(TokenType.COMMA, ",")
            elif self.current_char == '"':
                return self.get_full_boolean()
            elif self.current_char == "=":
                if self.peek_next() == "=":
                    self.advance()
                    self.skip_whitespace()
                    self.advance()
                    return Token(TokenType.EQUAL_EQUAL, "==")
                self.advance()
                return Token(TokenType.EQUAL, "=")
            elif self.current_char == "+":
                self.advance()
                return Token(TokenType.PLUS, "+")
            elif self.current_char == "-":
                self.advance()
                return Token(TokenType.MINUS, "-")
            elif self.current_char == "*":
                self.advance()
                return Token(TokenType.MUL, "*")
            elif self.current_char == "/":
                self.advance()
                return Token(TokenType.DIV, "/")
            elif self.current_char == "(":
                self.advance()
                return Token(TokenType.LPAREN, "(")
            elif self.current_char == ")":
                self.advance()
                return Token(TokenType.RPAREN, ")")
            elif self.current_char == "%":
                self.advance()
                return Token(TokenType.MODULO, "%")
            elif self.current_char in ("<", ">"):
                return self.get_full_relational()
            elif self.current_char == ":":
                self.advance()
                return Token(TokenType.COLON, ":")
            else:
                self.raiseError()

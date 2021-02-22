from lib.token import Token, TokenType


class Lexer(object):
    # handles the tokenization of the input string
    # syntax checking

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[0]

    def raiseError(self):
        raise Exception("Invalid syntax")

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def get_full_identifier(self) -> Token:
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
        }

        id = ""
        while self.current_char is not None and self.current_char.isalnum():
            id += self.current_char
            self.advance()


        # returns a token for a reserved word or a new token of type id if it is not a reserved word
        token = RESERVED_WORDS.get(id, Token(TokenType.IDENT, id))
        return token

    def get_full_number(self) -> Token:
        # multi-digit integer or float
        # no syntax error detection yet
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
        # no error detection yet
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
        # to be changed, applicable only to variable declaration with no error detection
        # advance for starting quotation mark
        self.advance()

        boolean = ""
        while self.current_char is not None and self.current_char != '"':
            boolean += self.current_char
            self.advance()

        # advance for ending quotation mark
        self.advance()

        return Token(
            TokenType.BOOL, boolean
        )  # please ko check ani ervin y dili ni bool

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_next_token(self) -> Token:
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            elif self.current_char.isdigit():
                return self.get_full_number()
            elif self.current_char.isalpha():
                return self.get_full_identifier()
            elif self.current_char == ",":
                self.advance()
                return Token(TokenType.COMMA, ",")
            elif self.current_char == '"':
                return self.get_full_boolean()
            elif self.current_char == "=":
                self.advance()
                return Token(TokenType.EQUAL, "=")
            elif self.current_char == ":":
                self.advance()
                return Token(TokenType.COLON, ":")
            else:
                self.raiseError()

from .token import Token, TokenType


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
            "INT": Token(TokenType.INT_DT, "INT_DT"),
            "CHAR": Token(TokenType.CHAR_DT, "CHAR"),
            "BOOL": Token(TokenType.BOOL_DT, "BOOL"),
            "FLOAT": Token(TokenType.FLOAT_DT, "FLOAT"),
        }

        id = ""
        while self.current_char is not None and self.current_char.isalnum():
            id += self.current_char
            self.advance()
        # returns a token for a reserved word or a new token of type id if it
        # is not a reserved word
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
        return Token(TokenType.INTEGER, number)

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
        return Token(TokenType.CHAR_DT, char)

    def get_full_boolean(self) -> Token:
        # to be changed, applicable only to variable declaration with no error detection
        boolean = '"'
        self.advance()
        while self.current_char is not None and self.current_char != '"':
            boolean += self.current_char
            self.advance()
        if self.current_char == '"':
            boolean += '"'
            self.advance()
        return Token(TokenType.BOOL_DT, boolean)

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
            else:
                self.raiseError()

from enum import Enum, unique


@unique
class TokenType(Enum):
    # keywords
    VAR = 1
    AS = 2
    START = 3
    STOP = 4
    INPUT = 5
    OUTPUT = 6
    KW_INT = 7
    KW_CHAR = 8
    KW_BOOL = 9
    KW_FLOAT = 10
    KW_STRING = 11
    # data types
    INT = 12
    CHAR = 13
    BOOL = 14
    FLOAT = 15

    # symbols
    EQUAL = 16
    COMMA = 17
    PLUS = 18
    MINUS = 19
    MUL = 20
    INTEGER_DIV = 21
    FLOAT_DIV = 22
    COLON = 23
    ASSIGN = 24
    # etc
    IDENT = 25
    LPAREN = 26
    RPAREN = 27
    AMPERSAND = 28


class Token(object):
    # contains type and value of a Token
    def __init__(self, type: TokenType, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "Token({type}, {value})".format(
            type=self.type.name, value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

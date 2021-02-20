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

    # data types
    INT = 11
    CHAR = 12
    BOOL = 13
    FLOAT = 14

    # symbols
    EQUAL = 15
    COMMA = 16

    # etc
    IDENT = 17
    COLON = 18
    MUL_INPUT = 19


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

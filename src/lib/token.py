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
    WHILE = 38
    IF = 39
    ELSEIF = 40
    ELSE = 41


    # data types
    INT = 12
    CHAR = 13
    BOOL = 14
    FLOAT = 15

    # symbols
    EQUAL = 16
    COMMA = 17

    # operators
    PLUS = 18
    MINUS = 19
    MUL = 20
    DIV = 21

    # logical
    OR = 22
    AND = 23
    NOT = 24
    EQUAL_EQUAL = 25
    NOT_EQUAL = 26
    LESS_THAN = 27
    GREATER_THAN = 28
    GREATER_THAN_EQUAL = 29
    LESS_THAN_EQUAL = 30
    MODULO = 31

    # etc
    COLON = 32
    ASSIGN = 33
    LPAREN = 34
    RPAREN = 35
    AMPERSAND = 36
    IDENT = 37


class Token(object):
    # contains type and value of a Token
    def __init__(self, type: TokenType, value: str):
        self.type = type
        self.value = value

    def __str__(self):
        return "Token({type}, {value})".format(
            type=self.type.name, value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

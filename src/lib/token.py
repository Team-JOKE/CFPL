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

    #operators
    PLUS = 17
    MINUS = 18
    MUL = 19
    DIV = 20
    OR = 24
    AND = 25
    NOT = 26
    EQUAL_EQUAL=27
    NOT_EQUAL=28
    LESS_THAN=29
    GREATER_THAN=30
    GREATER_THAN_EQUAL=31
    LESS_THAN_EQUAL=32
    MODULO=33

    # etc
    IDENT = 21
    LPAREN=22
    RPAREN=23
    

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

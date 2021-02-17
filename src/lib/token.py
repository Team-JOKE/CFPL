from enum import Enum, unique


@unique
class TokenType(Enum):
    IDENT = 0
    INT = 1
    FLOAT = 2
    INT_DT = 3
    FLOAT_DT = 4
    CHAR_DT = 5
    BOOL_DT = 6
    AS = 7
    COMMA = 8
    START = 9
    STOP = 10
    VAR = 11
    EQUAL = 12
    STAR = 13


class Token(object):
    # contains type and value of a Token
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "Token({type}, {value})".format(
            type=self.type.name, value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

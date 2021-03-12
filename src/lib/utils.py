from lib.token import Token


def is_keyword(token: Token) -> bool:
    return (1 <= token.type.value <= 11) or (22 <= token.type.value <= 24)

from lib.lexer import Lexer


def main():
    text = input("cfpl>")
    lexer = Lexer(text)
    while lexer.current_char is not None:
        print(lexer.get_next_token())


if __name__ == "__main__":
    main()

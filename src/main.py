from lib.lexer import Lexer


def main():
    # hax for presentation
    with open("./sample-source-codes/1.cfpl", "r") as file:
        for line in file.readlines():
            lexer = Lexer(line)
            while lexer.current_char is not None:
                print(lexer.get_next_token())


if __name__ == "__main__":
    main()

from lib.interpreter import Interpreter
from lib.lexer import Lexer
from lib.parser import Parser


def main():
    with open("sample-source-codes/1.cfpl", "r") as file:
        for line in file.readlines():
            lexer = Lexer(line)
            while lexer.current_char is not None:
                print(lexer.get_next_token())

    text = ""
    with open("sample-source-codes/1.cfpl", "r") as file:
        for line in file.readlines():
            text += line

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()


if __name__ == "__main__":
    main()

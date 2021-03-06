from lib.interpreter import Interpreter
from lib.lexer import Lexer
from lib.parser import Parser


def main():
    text = ""
    with open("src/sample-source-codes/test5.cfpl", "r") as file:
        for line in file.readlines():
            text += line.lstrip() + "\\n"

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()


if __name__ == "__main__":
    main()

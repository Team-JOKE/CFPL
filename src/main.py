from lib.interpreter import Interpreter
from lib.lexer import Lexer
from lib.parser import Parser


def main():
    text = ""
    with open("sample-source-codes/1.cfpl", "r") as file:
        for line in file.readlines():
            text += line + "\\n"

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    print(interpreter.VARIABLES)


if __name__ == "__main__":
    main()

from lib.interpreter import Interpreter
from lib.lexer import Lexer
from lib.parser import Parser


def main():
    files = ["1", "input", "output", "simple-while", "test2", "test3", "test4", "unary"]
    for file_name in files:
        text = ""
        with open(f"src/sample-source-codes/{file_name}.cfpl", "r") as file:
            for line in file.readlines():
                text += line + "\\n"

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        interpreter.interpret()
        print(interpreter.VARIABLES)


main()

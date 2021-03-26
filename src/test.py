import os
from pathlib import Path

from lib.interpreter import Interpreter
from lib.lexer import Lexer
from lib.parser import Parser

BASE_DIR = Path(__file__).resolve().parent.parent


def main():
    files = os.listdir(f"{ BASE_DIR }/src/sample-source-codes")
    for file_name in files:
        text = ""
        with open(f"src/sample-source-codes/{file_name}", "r") as file:
            for line in file.readlines():
                text += line.lstrip() + "\\n"

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        interpreter.interpret()


main()

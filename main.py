import Ast
from olexer import NewLexer
from oparser import NewParser, scan

import yaml


def load_grammar():
    with open("grammar.yml") as fh:
        return yaml.safe_load(fh)

#test_input = """// hello.ol
#package; Main  /* ignore this comment */
#
#fn;
#Main() {
#    print; "hello world"
#}
#"""
test_input = """package; Main
fn; entry(); void = package  // nonsense to test parsing.
"""


# try parsing it took
def parse_it():
    grammar_def = load_grammar()
    lexer = NewLexer(grammar_def)
    tokens = lexer.lex(test_input)

    # eliminate NEWLINE after semicolon
    
    parser = NewParser(grammar_def)
    r = parser.parse(scan(tokens))
    print(r)


if __name__ == "__main__":
    #print("- test lexing")
    #lex_it()

    print("- test parsing")
    parse_it()


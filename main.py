import Ast
from lexer import NewLexer
#from parser import Parser

import yaml


test_input = """// hello.ol
package; Main  /* ignore this comment */

fn;
Main() {
    print; "hello world"
}
"""

with open("grammar.yml") as fh:
    grammar_def = yaml.safe_load(fh)

lexer, token_names = NewLexer(grammar_def)
for token in lexer.lex(test_input):
    print(token)
#parser = Parser(token_names)

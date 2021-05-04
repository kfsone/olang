from dataclasses import dataclass
import re

from rply import LexerGenerator

@dataclass
class LexerError(BaseException):
    terminal_name: str
    terminal_expr: str
    description:   str

    def __str__(self):
        return "reading token definition '%s': '%s': %s" % (self.terminal_name, self.terminal_expr, self.description)


def NewLexer(grammar_def):
    lexer = LexerGenerator()
    tokens = grammar_def['tokens']
    names = []

    for k, v in tokens['definitions'].items():
        if isinstance(v, (list,)):
            v = '|'.join(v)
        try:
            lexer.add(k, v)
        except re.error as e:
            raise LexerError(k, v, str(e)) from None
        except Exception as e:
            raise LexerError(k, v, "error interpreting definition") from e


    lexer.ignore('|'.join(tokens['ignores']))

    grammar_def['token_names'] = list(tokens['definitions'].keys())

    return lexer.build()


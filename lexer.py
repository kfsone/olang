from dataclasses import dataclass
import re

from rply import LexerGenerator

KEYWORDS = (
    'fn',
    'package',
    'print',
)

PRODUCTIONS = (
    ( 'identifier', r'[A-Za-z_][A-Za-z0-9_]*' ),
    ( 'string_literal', '"(\\"|\\.|.)*"|\'(\\\'|\\.|.)*\'' ),
)

SYMBOLS = (
    ('SEMI_COLON',  ';'),
    ('COMMENT', r'/\*.*\*/'),
    ('OPEN_BRACE', '{'),
    ('CLOSE_BRACE', '}'),
    ('OPEN_PAREN', '\('),
    ('CLOSE_PAREN', '\)'),
    ('NEWLINE', '\n'),
)

IGNORED = (
    # Ignore spaces and tabs, as well as '\r'. nobody wants \r.
    r'[\r\t ]+',
    # Ignore line comments while keeping the \n
    r'//[^\n]*',
    # Ignore inline block comments
    r'/\*[^\n]*\*/',
)

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

    names = [kw.upper() for kw in KEYWORDS]
    names += [k for k, _ in PRODUCTIONS]
    names += [k for k, _ in SYMBOLS]

    tokens['names'] = names

    return lexer.build(), names


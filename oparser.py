from typing import List

from rply import ParserGenerator

from Ast import Document, Package, Declaration, Function, FunctionDefn, Expression, Statement

def scan(tokens: List):
    ttype = 'SEMICOLON'
    for token in tokens:
        ltype, ttype = ttype, token.gettokentype()
        if ttype != 'NEWLINE' or ltype != 'SEMICOLON':
            yield token

def production(pg: ParserGenerator, productions: dict, rule_name: str):
    rule = productions[rule_name]
    if isinstance(rule, (list, tuple)):
        rule = " | ".join(rule)
    rule = rule.replace("/*EMPTY*/", "")
    return pg.production(f"{rule_name} : {rule}")

def NewParser(grammar_def):
    pg = ParserGenerator(grammar_def['token_names'])
    pr = grammar_def['productions']

    @production(pg, pr, "document")
    def document(p):
        return Document(p[1], p[3] if len(p) > 3 else None)

    @production(pg, pr, "package-decl")
    def package_decl(p):
        return Package(p[1])

    @production(pg, pr, "package-specifier")
    def package_specifier(p):
        return None

    @production(pg, pr, "package-name-decl")
    def package_name_decl(p):
        return p[0]

    @production(pg, pr, "continuation")
    def continuation(p):
        return p[0]

    @production(pg, pr, "declarations")
    def declarations(p):
        return p

    @production(pg, pr, "newlines-allowed")
    def newlines_allowed(p):
        pass

    @production(pg, pr, "declaration")
    def declaration(p):
        return p[0]

    @production(pg, pr, "fn-decl")
    def fn_decl(p):
        return Function(p[2], p[3])

    @production(pg, pr, "fn-defn")
    def fn_fingerprint(p):
        return FunctionDefn(p[0], p[1], p[2])

    @production(pg, pr, "fn-args")
    def fn_args(p):
        return []

    @production(pg, pr, "fn-returntype")
    def fn_returntype(p):
        return p[1] if len(p) > 1 else None

    @production(pg, pr, 'open-block')
    def open_block(p):
        return None

    @production(pg, pr, "fn-body")
    def fn_body(p):
        if p[0].gettokentype() == 'EQUALS':
            return p[1]
        if p[2].gettokentype() == 'expression':
            return p[2]
        return None

    @production(pg, pr, "expression")
    def expression(p):
        return p[0]

    # @production(pg, pr, "statement")
    # def statement(p):
    #     return p[0]

    # @production(pg, pr, "single-stmt")
    # def single_stmt(p):
    #     return p[0]

    @pg.error
    def error_handler(token):
        sp = token.getsourcepos()
        raise ValueError(f"{sp.lineno}:{sp.colno}: Unexpected {token.gettokentype()}")

    return pg.build()

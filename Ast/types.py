from dataclasses import dataclass
from typing import List

@dataclass
class Package:
    """Package name of current CU"""
    value: str

    def eval(self) -> str:
        return self.value

class Statement:
    pass

class Expression:
    expression: str

    def eval(self):
        print("expr: " + self.expression)

class AtomicStatement(Statement):
    expression: Expression
    def eval(self):
        return self.expression.eval()

class CompoundStatement(Statement):
    expressions: List[Expression]
    def eval(self):
        for expression in self.expressions:
            expression.eval()

@dataclass
class Fn:
    name: str
    arglist: List[str]
    return_type: str
    statement: Statement

    def eval(self):
        print(f"declaring {self.name}({self.arglist}) -> {self.return_type}" )


@dataclass
class String:
    value: str

    def eval(self) -> str:
        return self.value


@dataclass
class Print:
    fmt: str
    args: List



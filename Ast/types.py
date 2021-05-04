from dataclasses import dataclass
from typing import List, Union

class Document:
    package: 'Package'
    declarations: Union[List['Declaration'], None]

    def __init__(self, package, declarations=None):
        self.package = package
        self.declarations = declarations or None

    def __repr__(self):
        if self.declarations:
            return f"Document<{self.package}, {self.declarations}>"
        else:
            return f"Document<{self.package}>"

class Package:
    """Package name of current CU"""
    name: str

    def __init__(self, name_token):
        self.name = name_token.value

    def __repr__(self):
        return f"Package<{self.name}>"

class Declaration:
    """A top-level declaration"""
    pass

@dataclass
class FunctionDefn:
    name: str
    args: List
    returns: List

@dataclass
class Function(Declaration):
    """A function declaration"""
    defn: FunctionDefn
    body: Union['Expression', 'Statement']

class Expression:
    pass

class Statement:
    pass
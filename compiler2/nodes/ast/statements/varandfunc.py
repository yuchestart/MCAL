from dataclasses import dataclass
from typing import *
from nodes.ast.util import CodeBlock

@dataclass
class VariableDeclaration:
    dtype:Any
    vars:list[dict[str,Any|None]]

@dataclass
class FunctionDeclaration:
    name:str
    returntype:Any
    parameters:list[tuple[str,Any]]
    code:CodeBlock

@dataclass
class ReturnStatement:
    expression:Any
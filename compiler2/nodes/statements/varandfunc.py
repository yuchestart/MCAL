from dataclasses import dataclass
from typing import *
from nodes.util import CodeBlock

@dataclass
class VariableDeclaration:
    dtype:Any
    vars:list[dict[str,Any|None]]

@dataclass
class FunctionDeclaration:
    returntype:Any
    parameters:list[tuple[str,Any]]
    code:CodeBlock

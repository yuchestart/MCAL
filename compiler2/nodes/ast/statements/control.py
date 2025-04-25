from dataclasses import dataclass
from typing import *
from nodes.ast.util import CodeBlock

@dataclass
class If:
    blocks:list[dict[str,Any,CodeBlock]]

@dataclass
class While:
    condition:Any
    block:CodeBlock
    type:Literal['dowhile']|Literal['while']

@dataclass
class For:
    init:Any
    condition:Any
    increment:Any
    block:CodeBlock
    
@dataclass
class Try:
    tryblock:CodeBlock
    catchblocks:List[tuple[Any,CodeBlock]]
    finallyblock:CodeBlock

@dataclass
class Assert:
    condition:Any
    error:Any

@dataclass
class Throw:
    error:Any
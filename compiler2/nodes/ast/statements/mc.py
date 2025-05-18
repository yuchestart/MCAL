from dataclasses import dataclass
from typing import *
from nodes.ast.util import CodeBlock

@dataclass
class Execute:
    value:str
    blocks:CodeBlock
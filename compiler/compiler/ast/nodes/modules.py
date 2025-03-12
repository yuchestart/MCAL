from typing import *
from dataclasses import dataclass

from compiler.ast.nodes.values import Symbol
from compiler.ast.nodes.base import BaseNode

@dataclass
class ModuleImportNode(Symbol):
    availableSymbols:List[Symbol] = []
    ident:str

@dataclass
class ModuleDeclarationNode(BaseNode):
    declared:List[Symbol] = []
    exported:List[Symbol] = []
    imports:List[ModuleImportNode] = []
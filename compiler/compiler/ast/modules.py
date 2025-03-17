from typing import *
from dataclasses import dataclass

from compiler.ast.values import Symbol
from compiler.ast.base import BaseNode

@dataclass
class ModuleImportNode(Symbol):
    availableSymbols:List[Symbol]
    ident:str

@dataclass
class ModuleDeclarationNode(BaseNode):
    declared:List[Symbol]
    exported:List[Symbol]
    imports:List[ModuleImportNode]
    extern:bool=False
    ident:str=""

@dataclass
class NamespaceDeclarationNode(BaseNode):
    ident:str
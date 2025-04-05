from typing import *
from compiler.ast.values import Symbol, DataType, Value, Identifier
from compiler.ast.base import BaseNode
from dataclasses import dataclass

@dataclass
class FunctionDeclaration(Symbol):
    name: str
    parameters: List[Tuple[DataType, str, Value | None]]
    code: List[BaseNode]
    entrypoint: str | None = None

@dataclass
class AnonymousFunction(Value):
    returnType: DataType
    parameters: List[Tuple[DataType, str, Value | None]]
    code: List[BaseNode]

@dataclass
class FunctionCall(Value):
    ident: Identifier
    parameters: List[BaseNode]
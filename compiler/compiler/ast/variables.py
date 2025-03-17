from typing import *
from compiler.ast.values import DataType, Expression, Value, Symbol, Identifier
from compiler.ast.base import BaseNode
from dataclasses import dataclass


@dataclass
class VariableDeclaration(Symbol):
    dataType: DataType
    declarations: List[Tuple[str, Value|None]]


@dataclass
class ScoreboardDeclaration(Symbol):
    criteria: str
    declarations: List[Tuple[str, Value|None]]


@dataclass
class AssignmentExpression(Expression):
    ident: Identifier
    value: Value
    type: str = "="

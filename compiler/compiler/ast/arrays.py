from dataclasses import dataclass
from compiler.ast.values import Expression

@dataclass
class ArrayAccess(Expression):
    of:Expression
    where:Expression
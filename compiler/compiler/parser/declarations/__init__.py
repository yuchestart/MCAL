from compiler.parser.base import ParserBase, ParserException
from compiler.parser.expressions.datatypes import ParserDataTypes

from compiler.astnodes.values import Identifier, Value, DataType
from compiler.astnodes.base import BaseNode
from compiler.parser.declarations.modules import ParserModules
from compiler.parser.declarations.variables import ParserDeclarationVariables
from compiler.parser.declarations.functions import ParserDeclarationsFunctions

from compiler.tokenizer.interfaces import Token

import pcre2
from typing import *


class ParserDeclarations(
    ParserModules,
    ParserDeclarationsFunctions,
    ParserDataTypes,
    ParserBase
):
    def parse_declaration(self,statement:str)->Tuple[bool,BaseNode]:
        pass

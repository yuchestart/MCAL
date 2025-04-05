from compiler.parser.base import ParserBase, ParserException
from compiler.parser.expressions.datatypes import ParserDataTypes

from compiler.ast.values import Identifier, Value, DataType
from compiler.ast.base import BaseNode
from compiler.parser.statements.modules import ParserStatementsModules
from compiler.parser.statements.variables import ParserStatementsVariables
from compiler.parser.statements.functions import ParserStatementsFunctions
from compiler.parser.expressions import ParserExpressions

from compiler.tokenizer.interfaces import Token

import pcre2
from typing import *


class ParserDeclarations(
    ParserStatementsModules,
    ParserStatementsVariables,
    ParserStatementsFunctions,
    ParserExpressions,
    ParserBase
):
    def parse_declaration(self,statement:str)->Tuple[bool,BaseNode]:
        pass

from parser.base import ParserBase
from nodes.ast.expressions.operations import *
from nodes.ast.util import *
from typing import *

from parser.expressions.primitives import PrimitiveExpressions
from parser.expressions.compound import CompoundExpressions
from parser.expressions.funcandvar import FuncAndVarExpressions
from parser.expressions.mc import MinecraftExpressions


class Expressions(
    MinecraftExpressions,
    FuncAndVarExpressions,
    CompoundExpressions,
    PrimitiveExpressions,
    ParserBase
):
    def parse_access_chain(self,allowed=["[",".","::","("]) -> AccessChain | Any | None:
        accesses = []
        atom = self.parse_atom()
        while not self.eof():
            if self.is_punc("["):
                if "[" not in allowed:
                    self.err("Unexpected '['")
                self.token_next()
                accesses.append(("generic", self.parse_expression()))
                self.skip_punc("]")
            elif self.is_punc("."):
                if "." not in allowed:
                    self.err("Unexpected '.'")
                self.token_next()
                if self.token_peek()["type"] != "ident":
                    self.err("Expected Identifier")
                accesses.append(("property", self.token_next()["value"]))
            elif self.is_punc("::"):
                if "::" not in allowed:
                    self.err("Unexpected '::'")
                self.token_next()
                if self.token_peek()["type"] != "ident":
                    self.err("Expected Identifier")
                accesses.append(("namespace",self.token_next()["value"]))
            elif self.is_punc("("):
               # print(self.token_peek())
                if "(" not in allowed:
                    self.err("Unexpected '('")
                accesses.append(
                    ("call", self.delimited("(", ")", ",", self.parse_expression))
                )
            else:
                break
        if len(accesses) >= 1:
            return AccessChain(atom, accesses)
        return atom

    def parse_wrapper(self) -> WrapperOpchain | Any | None:
        prefix = []
        postfix = []
        operand = None
        state = "prefix"
        while not self.eof():
            if state == "prefix":
                if self.is_punc(self.PREFIXOP):
                    prefix.append(self.token_next()["value"])
                else:
                    state = "operand"
            if state == "operand":
                operand = self.parse_access_chain()
                state = "postfix"
            if state == "postfix":
                # print(self.POSTFIXOP,operand)
                if self.is_punc(self.POSTFIXOP):
                    postfix.append(self.token_next()["value"])
                else:
                    break
        if len(prefix) == 0 and len(postfix) == 0:
            return operand
        return WrapperOpchain(prefix, postfix, operand)

    def parse_group(self) -> Any | None:
        if not self.is_punc("("):
            return
        self.token_next()
        expr = self.parse_expression()
        self.skip_punc(")")
        return expr

    def parse_new(self) -> Any | None:
        if not self.is_keywords("new"):
            return
        self.token_next()
        parsers = [
            self.parse_coordinate,
           # self.parse_uuid,
            self.parse_init_entity,
            self.parse_init_block,
            self.parse_init_storage,
            self.parse_anonymous_function,
        ]
        v = self.loop_parsers(parsers)
        if v is None:
            ident = self.parse_identifier()
            if ident is not None:
                return New(ident)
        return v

    def parse_atom(self):
       # print(self.token_peek(), self.eof())
        parsers = [
            self.parse_group,
            self.parse_null,
            self.parse_bool,
            self.parse_number,
            self.parse_string,
            self.parse_new,
            self.parse_command_call,
            self.parse_identifier,
            self.parse_array,
            self.parse_compound,
        ]

        return self.loop_parsers(parsers)


    def parse_expression(self):
        # print(self.BINARYOP)
        operands = []
        operators = []
        mode = "operand"
        while not self.eof():
            if mode == "operand":
                operands.append(self.parse_wrapper())
                mode = "operator"
            if mode == "operator":
                if not self.is_punc(self.BINARYOP):
                    break
                operators.append(self.token_next()["value"])
                mode = "operand"
        if len(operators) >= 1:
            return Opchain(operators, operands)
        return operands[0]

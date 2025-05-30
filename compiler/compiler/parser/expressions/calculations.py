from compiler.parser.base import ParserException
from compiler.parser.expressions.base import ParserExpressionsBase

from compiler.tokenizer.interfaces import Token

from compiler.ast.variables import AssignmentExpression
from compiler.ast.values import OperatorChain, UnaryOperation, Identifier, Expression

from typing import *
import re
import pcre2


class ParserExpressionsCalculations(ParserExpressionsBase):
    BINARY_OPERATORS = "+ - * = % == != && || < > <= >=".split(" ")
    def parse_expression_opchain(self,tokens:List[Token]) -> Tuple[int,OperatorChain]:
        retval = None
        expressions = []
        operators = []
        idx = 0
        state = "expr"
        for i,token in enumerate(tokens):
            if self.ignore(token):
                continue
            if state == "expr":
                j,expr = self.parse_expression_atom(tokens[i:])
                print(j,expr)
                if expr is None and len(operators) > 0:
                    raise ParserException(
                        "Expected expression",
                        token.position
                    )
                elif expr is None:
                    #Could be declaration
                    break
                i = j
                expressions.append(expr)
                state = "operator"
            elif state == "operator":
                if token.type != "OPERATOR" or token.data not in self.BINARY_OPERATORS:
                    #This isn't an opchain or the opchain ended
                    break
                operators.append(token.data)
                idx = i
                state = "expr"
                
        if len(expressions) == 0 or len(operators) == 0:
            return 0, None
        
        retval = OperatorChain(operators,expressions)
        return idx,retval

    UNARY_OPERATORS = "! + -".split(" ")
    UNARY_AFTER_OPERATORS = "++ --".split(" ")

    def parse_expression_unaryop(self,tokens:List[Token]) -> Tuple[int,UnaryOperation]:
        ret = None
        idx = 0
        op = None

        state = "operator"
        for i, token in enumerate(tokens):
            if self.ignore(token):
                continue
            if state == "operator":
                if token.type == "OPERATOR" and token.data in self.UNARY_OPERATORS:
                    op = token.data
                    state = "expr"
                elif token.type == "IDENTIFIER":
                    # Handle potential postfix (unary after) operators
                    ident = Identifier(token.data)
                    if i + 1 < len(tokens) and tokens[i + 1].type == "OPERATOR" and tokens[i + 1].data in self.UNARY_AFTER_OPERATORS:
                        ret = UnaryOperation(tokens[i + 1].data, ident, True)
                        idx = i + 1
                        break
                    else:
                        break
                else:
                    break
            elif state == "expr":
                if token.type == "IDENTIFIER":
                    ident = Identifier(token.data)
                ret = UnaryOperation(op, expr, False)
                break

        return idx, ret

    def parse_expression_group(self,tokens:List[Token]) -> Tuple[int,Expression]:
        
        # Instead of returning a GroupExpression class, this function seperates the expressions.
        # It's more concise that way, because the OperationChain handles everything in between
        # So (1+2)-3 would be this:
        # OpChain
        #   OpChain
        #      1 + 2
        #   - 3
        
        retval = None
        idx = 0
        state = "begin"
        for i,token in enumerate(tokens):
            if self.ignore(token):
                continue

            if state == "begin":
                if token.type != "GROUP_START":
                    #There could be a chance that it's not a group
                    break
                state = "content"
            elif state == "content":
                toparse = []
                elevation = 0
                for j,t in enumerate(tokens[i:]):
                    if self.ignore(t):
                        continue
                    if t.type == "GROUP_START":
                        elevation += 1
                    elif t.type == "GROUP_END":
                        elevation -= 1
                        if elevation < 0:
                            if j == 0:
                                raise ParserException(
                                    "Expected expression.",
                                    t.position
                                )
                            i+=j
                            break
                    toparse.append(t)
                _,expr = self.parse_expression(toparse)
                retval = expr
                state = "end"
            elif state == "end":
                if token.type != "GROUP_END":
                    raise ParserException(
                        "Expected ')'",
                        t.position
                    )
                break
        return idx,retval

    ASSIGNMENT_OPERATORS = "= += -= *= /= %=".split(" ")

    def parse_expression_assignment(self,tokens:List[Token]) -> Tuple[int,AssignmentExpression]:
        retval = None
        idx = 0
        state = "ident"
        op:str = None
        ident:Identifier = None
        for i,token in enumerate(tokens):
            if self.ignore(token):
                continue
            if state == "ident":
                if token.type != "IDENTIFIER":
                    #Could be non-assignment expression
                    break
                ident = Identifier(token.data)
                state = "type"
            elif state == "type":
                if token.type != "OPERATOR":
                    #HACK: Find a case where this needs an error
                    #Could be some kind of hogwash
                    break
                #Check if it is assignment
                if token.data not in self.ASSIGNMENT_OPERATORS:
                    #This could be an opchain
                    break
                op = token.data
                state = "expression"
            elif state == "expression":
                j,value = self.parse_expression(tokens[i:])
                retval = AssignmentExpression(ident,value,op)
                idx = i+j

        return idx,retval
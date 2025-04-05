from compiler.parser.expressions.base import ParserExpressionsBase
from compiler.parser.base import ParserException

from compiler.tokenizer.interfaces import Token
from compiler.ast.values import Identifier
from compiler.ast.functions import FunctionCall,AnonymousFunction

class ParserExpressionsFunctions(ParserExpressionsBase):
    def parse_function_call(self,tokens:list[Token]) -> tuple[int,FunctionCall]:
        ret = None
        idx = 0
        ident = None
        didcall = False
        parameters = []

        state = "ident"
        i = -1
        while i < len(tokens)-1:
            i+=1
            token = tokens[i]

            if self.ignore(token):
                continue
            if state == "ident":
                if token.type != "IDENTIFIER":
                    break
                ident = Identifier(token.data)
                state = "openbracket"
            elif state == "openbracket":
                if token.type != "GROUP_START":
                    break
                state = "value"
            elif state == "value":
                if token.type == "GROUP_END":
                    didcall = True
                    idx = i
                    break
                toparse = []
                elevation = 0
                end = False
                endidx = 0
                for j,t in enumerate(tokens[i:]):
                    if self.ignore(t):
                        continue
                    if t.type == "GROUP_START":
                        elevation += 1
                    elif t.type == "GROUP_END":
                        elevation -= 1
                        if elevation < 0:
                            end = True
                            endidx = j-1
                            break
                    elif t.type == "LIST_SEPERATOR" and elevation == 0:
                        endidx = j-1
                        break
                    toparse.append(t)
                i+=endidx
                _,value = self.parse_expression(toparse)
                parameters.append(value)
                if end:
                    idx = i
                    break
                state = "seperator"
            elif state == "seperator":
                if token.type == "GROUP_END":
                    idx = i
                    break
                elif token.type == "LIST_SEPERATOR":
                    state = "value"
                else:
                    raise ParserException("Expected ')' or ','",token.position)
        if didcall:
            ret = FunctionCall(ident,[])
        else:
            if len(parameters) > 0 and ident:
                ret = FunctionCall(ident,parameters)
            

        return idx, ret

    def parse_anonymous_function(self,tokens:list[Token]) -> tuple[int,AnonymousFunction]:
        pass
from compiler.util import printError

class ParserException(Exception):
    kind:str
    pos:int
    def __init__(self,kind:str,pos:int):
        self.kind = kind
        self.pos = pos
    def print(self):
        printError(self.kind,self.pos)


class ParserBase():
    code:str
    regex:str

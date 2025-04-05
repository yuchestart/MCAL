import os
import re

class Token:
    value:str
    type:str

class Tokenizer:
    code:str
    pos:int
    def next(self,i=1):
        ret = self.code[self.pos:self.pos+i]
        pos += i
        return ret
    
    def peek(self,i=1):
        return self.code[self.pos:self.pos+i]
    
    def eof(self):
        return self.pos == len(self.code)

    def err(self,msg):
        print(f"Error @ {self.pos}: {msg}")
        raise Exception("Parsing Failed")
    
    
    KEYWORDS:list[str] = []
    BINARYOP:list[str] = []
    POSTFIXOP:list[str] = []
    PREFIXOP:list[str] = []

    COMMENT_REGEX:str = r"(?:\/\/.*$)|(?:\/\*(?:.|\n)*\*\/)"
    GROUP_OPEN:list[str] = "[{(".split("")
    GROUP_CLOSE:list[str] = "]})".split("")
    TYPEGROUP_OPEN:str = "<"
    TYPEGROUP_CLOSE:str = ">"
    STATEMENT_SEPERATOR:str = ";"
    LIST_SEPERATOR:str = ","

    def init_tokenizer(self):
        os.chdir(os.path.dirname(__file__))
        with open("parser/def/binaryop.txt") as f:
            self.BINARYOP = list(filter(lambda x: not x.startswith("#"),f.read().splitlines()))
        with open("parser/def/postfixop.txt") as f:
            self.POSTFIXOP = list(filter(lambda x: not x.startswith("#"),f.read().splitlines()))
        with open("parser/def/prefixop.txt") as f:
            self.PREFIXOP = list(filter(lambda x: not x.startswith("#"),f.read().splitlines()))
        with open("parser/def/kw.txt") as f:
            self.KEYWORDS = list(filter(lambda x: not x.startswith("#"),f.read().splitlines()))

    DIGITS = "0123456789".split("")
    SIGNS = "uUsS".split("")
    NUMTYPES = "iIfFlLdDsSbB".split("")
    NUMSPLITREGEX = r"(\d*\.\d*)([uUsS])?([iIfFlLdDsSbB])?"
    def read_number(self):
        s = ""
        has_dot = False
        has_digits = False
        has_sign = False
        has_type = False
        while (not self.eof()):
            if self.peek() == ".":
                if has_dot:
                    self.err("Unexpected '.'")
                has_dot = True
            elif self.peek() in self.DIGITS:
                has_digits = True
            elif self.peek() in self.NUMTYPES:
                if has_type:
                    self.err(f"Unexpected '{self.peek()}'")
                if not has_digits:
                    self.err(f"Unexpected '{self.peek()}'")
                has_type = True
            elif self.peek() in self.SIGNS:
                if has_sign:
                    self.err(f"Unexpected '{self.peek()}'")
                if has_type:
                    self.err(f"Unexpected '{self.peek()}'")
                    return False
                has_sign = True
            else:
                break
            s+=self.next()
        
        return 

    def skip_comment(self):
        comment = None
        while not self.eof():
            if comment is None:
                if self.peek(2) == "//":
                    comment = "oneline"
                elif self.peek(2) == "/*":
                    comment = "multiline"
                else:
                    continue
            elif comment == "oneline":
                if self.peek() == "\n":
                    break
                self.next()
            elif comment == "multiline":
                if self.peek(2) == "*/":
                    self.next(2)
                    break
                self.next()
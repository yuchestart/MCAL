import os
import re
from dataclasses import dataclass
from typing import *

Token = Dict[str,Any]

class Tokenizer:
    code:str
    tokens:list[Token]
    token_cache:list[Token]
    pos:int
    mode:str
    def input_next(self,i=1):
        if (self.pos + i) > len(self.code):
           # print(self.pos+i)
            self.err("Unexpected EOF")
        ret = self.code[self.pos:self.pos+i]
        self.pos += i
        return ret
    
    def input_peek(self,i=1):
        return self.code[self.pos:min(self.pos+i,len(self.code))]
    
    def eof(self):
        if self.mode == "code":
            length = len(self.code)
        elif self.mode == "tokens":
            length = len(self.tokens)
        return self.pos == length

    def err(self,msg):
        print(f"Error @ {self.pos}: {msg}")
        raise Exception("Parsing Failed")
    
    currentToken:Token|None = None

    def token_peek(self):
        if self.eof():
            raise EOFError()
        return self.read_next_token(preservepos = True)
    
    def token_next(self) -> Token | None:
        if self.eof():
            raise EOFError()
        return self.read_next_token()

    KEYWORDS:list[str] = []
    BINARYOP:list[str] = []
    POSTFIXOP:list[str] = []
    PREFIXOP:list[str] = []
    PUNCTUATION:list[str] = []
    OTHEROP:list[str] = []

    COMMENT_REGEX:str = r"(?:\/\/.*$)|(?:\/\*(?:.|\n)*\*\/)"
    IDENT_START_REGEX:str = r"[a-zA-Z_$]"
    IDENT_CHAR_REGEX:str = r"[a-zA-Z0-9_$]"
    GROUP_OPEN:list[str] = "[{("
    GROUP_CLOSE:list[str] = "]})"

    def init_tokenizer(self,mode):
        self.pos = 0
        #print(self.tokens if mode == "tokens" else None,self.pos)
        # TODO: Auto-walk the path thingy
        with open("parser/def/binaryop.txt") as f:
            self.BINARYOP = list(filter(lambda x: not x.startswith("#"),f.read().splitlines()))
        with open("parser/def/postfixop.txt") as f:
            self.POSTFIXOP = list(filter(lambda x: not x.startswith("#"),f.read().splitlines()))
        with open("parser/def/prefixop.txt") as f:
            self.PREFIXOP = list(filter(lambda x: not x.startswith("#"),f.read().splitlines()))
        with open("parser/def/kw.txt") as f:
            self.KEYWORDS = list(filter(lambda x: not x.startswith("#"),f.read().splitlines()))
        with open("parser/def/miscop.txt") as f:
            self.OTHEROP = list(filter(lambda x: not x.startswith("#"),f.read().splitlines()))
        self.PUNCTUATION = [*{
            *self.BINARYOP,
            *self.POSTFIXOP,
            *self.PREFIXOP,
            *self.GROUP_OPEN,
            *self.GROUP_CLOSE,
            *self.OTHEROP
        }]
        # Make sure that longer (e.g. ::) doesn't get mistaken for shorter (e.g. :)
        self.PUNCTUATION.sort(key=lambda x: len(x),reverse=True)
        self.KEYWORDS.sort(key=lambda x: len(x),reverse=True)

        self.mode = mode

    DIGITS = "0123456789"
    SIGNS = "uUsS"
    NUMTYPES = "iIfFlLdDsSbB"
    NUMSPLITREGEX = r"(\d*\.\d*)([uUsS])?([iIfFlLdDsSbB])?"

    def read_number(self) -> Token | None:
        s = ""
        has_dot = False
        has_digits = False
        has_sign = False
        has_type = False
        while (not self.eof()):
            if self.input_peek() == ".":
                if has_dot:
                    self.err("Unexpected '.'")
                has_dot = True
            elif self.input_peek() in self.DIGITS:
                has_digits = True
            elif self.input_peek() in self.NUMTYPES:
                if has_type:
                    self.err(f"Unexpected '{self.input_peek()}'")
                if not has_digits:
                    self.err(f"Unexpected '{self.input_peek()}'")
                has_type = True
            elif self.input_peek() in self.SIGNS:
                if has_sign:
                    self.err(f"Unexpected '{self.input_peek()}'")
                if has_type:
                    self.err(f"Unexpected '{self.input_peek()}'")
                has_sign = True
            else:
                break
            s+=self.input_next()
        if has_digits:
            return dict(type="number",value=s)
        return None

    def skip_comment(self) -> None:
        comment = None
        while not self.eof():
            if comment is None:
                if self.input_peek(2) == "//":
                    comment = "oneline"
                elif self.input_peek(2) == "/*":
                    comment = "multiline"
                else:
                    break
            elif comment == "oneline":
                if self.input_peek() == "\n":
                    break
                self.input_next()
            elif comment == "multiline":
                if self.input_peek(2) == "*/":
                    self.input_next(2)
                    break
                self.input_next()
    
    def read_name(self) -> Token | None:
        ident = self.input_next() # This is guaranteed to be valid start char
        while not self.eof():
            if re.match(self.IDENT_CHAR_REGEX,self.input_peek()) is not None:
                ident += self.input_next()
            else:
                break
        
        for kw in self.KEYWORDS:
            if ident == kw:
                return dict(type="keyword",value=kw)
        return dict(type="ident",value=ident)

    def read_string(self) -> Token | None:
        chars = ""
        startchar=self.input_next()
        escaped = False
        substitutions = {}
        i = -1
        while not self.eof():
            i+=1
            if self.input_peek() == "\\":
                escaped = True
                self.input_next()
                continue
            if escaped:
                chars += self.input_next()
                continue
            elif self.input_peek() == startchar:
                self.input_next()
                break
            elif self.input_peek(2) == "${":
                self.input_next(2)
                x = self.read_substitution()
                substitutions[i] = x
                continue
            chars += self.input_next()
        return dict(type="string",value=chars,substitutions=substitutions)

    def read_substitution(self,brace_type="{}") -> list[Token]:
        elevation = 0
        tokens:list[Token] = []
        while True:
            next = self.read_next_token()
            if next is None:
                break
            if next["type"] == "punc" and next["value"] == brace_type[0]:
                elevation += 1
            elif next["type"] == "punc" and next["value"] == brace_type[1]:
                elevation -= 1
                if elevation < 0:
                    break
            tokens.append(next)
        return tokens
    
    def read_command(self,bchar="()") -> Token | None:
        chars = ""
        instring = False
        elevation = 0
        escape = 0
        sub = {}
        i = -1
        while not self.eof():
            i+=1
           # print(chars)
            if escape:
                chars += self.input_next(escape)
                i+=escape
                escape = 0
                continue
            #region escapes
            #escaped normal
            if self.input_peek() == "\\" and not bool(instring):
                escape = 1
                continue
            if self.input_peek(3) == "\\${":
                escape = 2
                self.input_next()
                continue
            if self.input_peek(2) == f"\\{bchar[1]}":
                escape = 1
                self.input_next()
                continue
            #\\${ or \\) i.e. escaped backslash
            if self.input_peek(4) == "\\\\${" or self.input_peek(3) == f"\\\\{bchar[1]}" and not bool(instring):
                escape = 1
                self.input_next()
                continue
            #endregion
            #strings
            if self.input_peek() in "\'\"":
                if not bool(instring):
                    instring = None
                else:
                    instring = self.input_peek()
            #substitutions:
            if self.input_peek(2) == "${":
                self.input_next(2)
                sub[i] = self.read_substitution()
            #braces
            if self.input_peek() == bchar[1] and not bool(instring):
                elevation -= 1
                if elevation <= 0:
                    self.input_next(1)
                    break
            elif self.input_peek() == bchar[0] and not bool(instring):
                elevation += 1
            #print(chars,i,elevation,bchar[1]==self.input_peek(),instring)
            chars += self.input_next(1)
        return dict(type="command",value=chars,substitutions=sub,start=bchar[0])   



    def read_next_token(self,preservepos = False) -> Token | None:
        if preservepos:
            backtrackpos = self.pos
        try:
            if self.mode == "tokens":
                if not self.eof():
                    self.pos += 1
                   # print(self.tokens,self.pos)
                    return self.tokens[self.pos-1]
                raise EOFError()
            while not self.eof() and re.match(r"\s",self.input_peek()) is not None:
                self.input_next()
            if self.eof():
                raise EOFError()
            self.skip_comment()
            ch = self.input_peek()
            if ch in "\"'":
                return self.read_string()
            if ch in self.DIGITS:
                return self.read_number()
            if re.match(self.IDENT_START_REGEX,ch) is not None:
                return self.read_name()
            if self.input_peek(2) == "!(":
                self.input_next(2)
                return self.read_command("()")
            if self.input_peek(2) == "!{":
                self.input_next(2)
                return self.read_command("{}")
            for op in self.PUNCTUATION:
                if self.input_peek(len(op)) == op:
                    self.input_next(len(op))
                    return dict(type="punc",value=op)
            self.err(f"Can't handle character '{ch}'.")
        finally:
            if preservepos:
                self.pos = backtrackpos
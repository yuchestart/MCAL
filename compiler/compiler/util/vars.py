

class CompilerVarsSingleton:
    code:str
    fname:str
    def setCode(self,code:str,path:str)->None:
        self.code = code
        self.path = path

COMPILERVARS = CompilerVarsSingleton()
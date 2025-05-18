from nodes.ast.statements.varandfunc import *
from nodes.ast.statements.control import *
from nodes.ast.statements.mc import *
from nodes.ast.statements.modules import *
from nodes.ast.statements.oop import *
from nodes.ast.expressions.mc import *
from nodes.ast.expressions.primitives import *
from nodes.ast.expressions.operations import *
from nodes.ast.util import *

class Desugarer:
    modules = {}

    def desugarvar(self,ast:Any):
        pass

    def desugarfunc(self,ast:Any):
        pass

    def desugar(self,ast:Any):
        if isinstance(ast,VariableDeclaration):
            self.desugarvar(ast)
        elif isinstance(ast,FunctionDeclaration):
            self.desugarfunc(ast)
        elif isinstance(ast,Namespace):
            pass
        elif isinstance(ast,UsingNamespace):
            pass
        elif isinstance(ast,Import):
            pass
        elif isinstance(ast,Export):
            pass
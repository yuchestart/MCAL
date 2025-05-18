from lowerer.lowerer.base import LowererBase
from nodes.ast.statements.varandfunc import *
from nodes.ir.control import *
from nodes.ir.memory import *
from nodes.ir.util import *

class Lowerer(LowererBase):
    def __init__(self,ast):
        self.ast = ast

    def lower_func(self,ast):
        pass

    def lower_var_dec(self,ast:VariableDeclaration,type="stack"):
        ir = []
        ir_type = StoreStack if type == "stack" else StoreHeap if type == "heap" else StoreGlobal
        for var in ast.vars:
            ir.append(ir_type(var["name"],self.lower_expression(ast)))
        return ir

    def lower_expression(self,ast):
        pass

    def lower(self):
        ir = []
        for dec in self.ast:
            if isinstance(dec,FunctionDeclaration):
                ir.extend(self.lower_func(dec))
            elif isinstance(dec,VariableDeclaration):
                ir.extend(self.lower_var_dec(dec,"global"))
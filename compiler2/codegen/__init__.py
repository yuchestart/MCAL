from typing import Any
from nodes.ir.control import *
from nodes.ir.memory import *
from nodes.ir.util import *


class CodeGenerator:
    ir:List[DefineFunc] = []
    functions:dict[str,str] = {}
    extern_functions:dict[str,str] = {}
    namespace:str
    runtime:str

    def __init__(self,ir,namespace,runtime):
        self.ir = ir
        self.namespace = namespace
        self.runtime = runtime
    
    def generate_code(self):
        for ir in self.ir:
            if ir.extern:
                self.extern_functions[ir.name] = self.generate_sequence(ir.impl,ir.name,ir.params,ir.extern)
            else:
                self.functions[ir.name] = self.generate_sequence(ir.impl,ir.name,ir.params,ir.extern)

    def transpile_value(self,node):
        currentCommand = ""
        if isinstance(node,CallFunc):
            currentCommand = f"function {self.namespace}:{node.name}"
        return currentCommand

    def generate_sequence(self,ir:list[Any]):
        code = ""
        for node in ir:
            currentCommand = ""
            if isinstance(node,NewStack):
                currentCommand = f"function {self.runtime}:api/new_stack"
            elif isinstance(node,DisposeStack):
                currentCommand = f"function {self.runtime}:api/dispose_stack"
            elif isinstance(node,StoreStack):
                pass
            elif isinstance(node,StoreHeap):
                pass
            elif isinstance(node,Delete):
                pass
            elif isinstance(node,Loop):
                impl = self.generate_sequence(node.impl)
                if len(node.next) > 0:
                    self.functions[node.name + "_LOOPIMPL"] = impl
                    next = self.generate_sequence(node.next)
                    func = f"function {self.namespace}:{node.name+'_LOOPIMPL'}\n"
                    func += next + '\n'
                    self.functions[node.name] = func
                else:
                    self.functions[node.name] = impl
                currentCommand = f"function {self.namespace}:{node.name}"

            elif isinstance(node,Command):
                if len(node.macros) > 0:
                    for macro in node.macros:
                        pass
                else:
                    currentCommand = node.value
            elif isinstance(node,CallFunc):
                
                currentCommand = f"function {self.namespace}:{node.name}"
            
            code += currentCommand + "\n"

        return code

import ast
from ast import NodeTransformer, fix_missing_locations

class ChangeVar(NodeTransformer): 
    def __init__(self, oldVar, newVar):
        self.oldVar = oldVar
        self.newVar = newVar
    
    def visit_Name(self, node): 
        if node.id == self.oldVar:  
            node.id = self.newVar
        return node 
    
def changeVar(methodStr, oldVar, newVar):
    tree = ast.parse(methodStr)
    ChangeVar(oldVar, newVar).visit(tree)
    fix_missing_locations(tree)

    # Here we unparse the modified AST back into a code string
    new_code = ast.unparse(tree)
    
    return new_code
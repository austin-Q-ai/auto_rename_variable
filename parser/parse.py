import ast
from autopep8 import fix_code
import re


def fix_python_code(code):
    well_formatted_code = fix_code(code)

    return well_formatted_code


class VariableVisitor(ast.NodeVisitor):
    def __init__(self):
        self.variables = set()

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variables.add(target.id)
        self.generic_visit(node)


def parse(methodStr):
    methodStr = fix_python_code(methodStr)

    tree = ast.parse(methodStr)
    visitor = VariableVisitor()
    visitor.visit(tree)

    return list(visitor.variables)
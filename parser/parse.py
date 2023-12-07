import ast
from autopep8 import fix_code
import re


def fix_python_code(code):
    well_formatted_code = fix_code(code)

    return well_formatted_code


class VariableVisitor(ast.NodeVisitor):
    def __init__(self):
        super().__init__()  # Initialize the base class
        self.variables = set()
        self.parameters = set()

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variables.add(target.id)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        for arg in node.args.args:
            # Note: In Python 3.8 and later, you can use 'arg.arg' instead of 'arg.id'
            self.parameters.add(arg.arg)
        # Check for arguments in other parameter lists (e.g., *args, **kwargs)
        if node.args.vararg:
            self.parameters.add(node.args.vararg.arg)
        if node.args.kwarg:
            self.parameters.add(node.args.kwarg.arg)
        # Visit the body of the function in case it contains more variables
        self.generic_visit(node)


def parse(methodStr):
    methodStr = fix_python_code(methodStr)

    tree = ast.parse(methodStr)
    visitor = VariableVisitor()
    visitor.visit(tree)

    return list(visitor.variables) + list(visitor.parameters)
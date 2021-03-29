import ast
from prettiest_ast import ppast

filename ="C:/Users/vniko/PycharmProjects/BSP2-PlagiarismDetection/RandomCode.py"

with open(filename) as src_file:
    tree = ast.parse(src_file.read())

"""Create a list to save the names of the function of the .py"""
methodList = []

class Analyzer(ast.NodeVisitor):

    def visit_FunctionDef(self, node):
        methodList.append(node.name)
        ast.NodeVisitor.generic_visit(self, node)

ppast(tree)
v = Analyzer()
v.visit(tree)
print(methodList)





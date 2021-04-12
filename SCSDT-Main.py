import ast
from prettiest_ast import ppast

filename ="C:/Users/vniko/PycharmProjects/BSP2-PlagiarismDetection/RandomCode.py"

with open(filename) as src_file:
    tree = ast.parse(src_file.read())


def binoptostring(op):
    if isinstance(op, ast.Add):
        return "+"
    elif isinstance(op, ast.Mult):
        return "*"
    elif isinstance(op, ast.Sub):
        return "-"
    elif isinstance(op, ast.Div):
        return "/"
    elif isinstance(op, ast.Mod):
        return "%"
    elif isinstance(op, ast.Pow):
        return "**"


class Analyzer(ast.NodeVisitor):

    def __init__(self):
        self.methodList = []
        self.astToString = ""

    def visit_ClassDef(self, node):
        self.astToString += "class(" + node.name + ") "
        ast.NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node):
        self.methodList.append(node.name)
        self.astToString += "def(" + node.name + ") "
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Assign(self, node):
        self.astToString += "=( "
        ast.NodeVisitor.generic_visit(self, node)
        self.astToString += ") "

    def visit_Name(self, node):
        self.astToString += node.id + " "
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Num(self, node):
        self.astToString += str(node.n) + " "
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Return(self, node):
        self.astToString += "return( "
        ast.NodeVisitor.generic_visit(self, node)
        self.astToString += ") "

    def visit_Call(self, node):
        self.astToString += node.func.id + "( "
        ast.NodeVisitor.generic_visit(self, node)
        self.astToString += ") "

    def visit_Tuple(self, node):
        self.astToString += "( "
        ast.NodeVisitor.generic_visit(self, node)
        self.astToString += ") "

    def visit_List(self, node):
        self.astToString += "[ "
        ast.NodeVisitor.generic_visit(self, node)
        self.astToString += "] "

    def visit_ListComp(self, node):
        self.astToString += "[ "
        ast.NodeVisitor.generic_visit(self, node)
        self.astToString += "] "

    def visit_BinOp(self, node):
        self.astToString += binoptostring(node.op) + "( "
        ast.NodeVisitor.generic_visit(self, node)
        self.astToString += ") "

    def visit_For(self, node):
        self.astToString += "forloop( "
        ast.NodeVisitor.generic_visit(self, node)
        self.astToString += ") "

    def visit_While(self, node):
        self.astToString += "whileloop( "
        ast.NodeVisitor.generic_visit(self, node)
        self.astToString += ") "

    def visit_comprehension(self, node):
        self.astToString += "forloop( "
        ast.NodeVisitor.generic_visit(self, node)
        self.astToString += ") "



    def print_methodlist(self):
        print(self.methodList)

    def print_astToString(self):
        print(self.astToString)


ppast(tree)
v = Analyzer()
v.visit(tree)
v.print_methodlist()
v.print_astToString()





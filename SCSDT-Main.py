import ast
from prettiest_ast import ppast

filename = "C:/Users/vniko/OneDrive/VFile/UniLu/Semester 2/BSP 2/Project/RandomCode.py"

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

def cmpopoptostring(op):
  if isinstance(op, ast.Eq):
    return "=="
  elif isinstance(op, ast.NotEq):
    return "!="
  elif isinstance(op, ast.Lt):
    return "<"
  elif isinstance(op, ast.LtE):
    return "<=>"
  elif isinstance(op, ast.Gt):
    return ">"
  elif isinstance(op, ast.GtE):
    return ">="
  elif isinstance(op, ast.Is):
    return "is"
  elif isinstance(op, ast.IsNot):
    return "is not"
  elif isinstance(op, ast.In):
    return "in"
  elif isinstance(op, ast.NotIn):
    return "not in"

class Analyzer(ast.NodeVisitor):

  def __init__(self):
    self.methodList = []
    self.astToString = ""
    self.lineno = 0

  def generic_Visit(self, node):
    """if self.lineno != node.lineno:
      self.lineno += 1
      self.astToString += "\n"""""
    ast.NodeVisitor.generic_visit(self, node)

  def visit_ClassDef(self, node):
    self.astToString += "class " + node.name + " "
    self.generic_Visit(node)

  def visit_FunctionDef(self, node):
    self.methodList.append(node.name)
    self.astToString += "def " + node.name
    self.generic_Visit(node)

  def visit_Assign(self, node):
    for target in node.targets:
      self.generic_Visit(target)
      self.astToString += "= "

    self.generic_Visit(node.value)
    """self.astToString += "=( "
    self.generic_Visit(node)
    self.astToString += ") """""

  def visit_Name(self, node):
    self.astToString += node.id + " "
    self.generic_Visit(node)

  def visit_Num(self, node):
    self.astToString += str(node.n) + " "
    self.generic_Visit(node)

  def visit_Return(self, node):
    self.astToString += "return "
    self.generic_Visit(node)
    self.astToString += " "

  def visit_Call(self, node):
    self.astToString += node.func.id + "( "
    if len(node.args) > 0:
      self.generic_Visit(node.args[0])
      for arg in node.args[1:]:
        self.astToString += ", "
        self.generic_Visit(arg)
    self.astToString += ") "

  def visit_Tuple(self, node):
    self.astToString += "( "
    self.generic_Visit(node)
    self.astToString += ") "

  def visit_List(self, node):
    self.astToString += "[ "
    self.generic_Visit(node)
    self.astToString += "] "

  def visit_ListComp(self, node):
    self.astToString += "[ "
    self.generic_Visit(node)
    self.astToString += "] "

  def visit_BinOp(self, node):
    try:
      self.visit_Name(node.left)
      self.visit_Constant(node.left)
      self.visit_Call(node.left)
    except:
      pass
    self.astToString += " " + binoptostring(node.op) + " "
    try:
      self.visit_Name(node.right)
      self.visit_Constant(node.right)
      self.visit_Call(node.right)
    except:
      pass

  def visit_For(self, node):
    self.astToString += "forloop( "
    self.generic_Visit(node)
    self.astToString += ") "

  def visit_While(self, node):
    self.astToString += "whileloop( "
    self.generic_Visit(node)
    self.astToString += ") "

  def visit_comprehension(self, node):
    self.astToString += "for "
    self.generic_Visit(node.target)
    try:
      self.visit_Name(node.target)
    except:
      pass
    self.astToString += "in "
    ast.NodeVisitor.generic_visit(self, node.iter)

  def visit_arguments(self, node):
    self.astToString += "("
    if len(node.args) > 0:
      self.astToString += node.args[0].arg
      for arg in node.args[1:]:
        self.astToString += ", "
        self.visit_arg(arg)
    self.astToString += ") "

  def visit_arg(self, node):
    self.astToString += node.arg
    ast.NodeVisitor.generic_visit(self, node)

  def visit_Constant(self, node):
    self.astToString += str(node.value)
    ast.NodeVisitor.generic_visit(self, node)

  def visit_Attribute(self, node):
    self.astToString += str(node.value)
    ast.NodeVisitor.generic_visit(self, node)

  def visit_Starred(self, node):
    self.astToString += str(node.value)
    ast.NodeVisitor.generic_visit(self, node)

  def visit_Compare(self, node):
    self.generic_Visit(node.left)
    self.astToString += " " + cmpopoptostring(node.op) + " "
    self.generic_Visit(node.right)

  def visit_NamedExpr(self, node):
    self.astToString += str(node.target)
    ast.NodeVisitor.generic_visit(self, node)

  def visit_Expr(self, node):
    self.astToString += str(node.value)


  def print_methodlist(self):
    print(self.methodList)

  def print_astToString(self):
    print(self.astToString)


ppast(tree)
v = Analyzer()
v.visit(tree)
v.print_methodlist()
v.print_astToString()

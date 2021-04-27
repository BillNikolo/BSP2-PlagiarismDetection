import ast
from prettiest_ast import ppast

filename = "RandomCode.py"

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

def unaroptostring(op):
  if isinstance(op, ast.Invert):
    return "~"
  elif isinstance(op, ast.Not):
    return "not"
  elif isinstance(op, ast.UAdd):
    return "+"
  elif isinstance(op, ast.USub):
    return "-"

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
      self.lineno = node.lineno
      print(node.lineno)
      self.astToString += "\n"""""
    ast.NodeVisitor.generic_visit(self, node)

  def visit_ClassDef(self, node):
    self.astToString += "class " + node.name + " "
    self.generic_Visit(node)

  def visit_FunctionDef(self, node):
    self.methodList.append(node.name)
    self.astToString += "def " + node.name
    self.generic_Visit(node)
    self.astToString += "\n"


  def visit_Assign(self, node):
    for target in node.targets:
      self.visit(target)
      self.astToString += "= "
    self.visit(node.value)

  def visit_Name(self, node):
    self.astToString += node.id + " "

  def visit_Num(self, node):
    self.astToString += str(node.n) + " "

  def visit_Return(self, node):
    self.astToString += "return "
    self.generic_Visit(node)
    self.astToString += " "

  def visit_Call(self, node):
    self.visit(node.func)
    self.astToString += "("
    if len(node.args) > 0:
      self.visit(node.args[0])
      for arg in node.args[1:]:
        self.astToString += ", "
        self.visit(arg)
    if len(node.keywords) > 0:
      self.visit(node.keywords[0])
      for keyword in node.keywords[1:]:
        self.astToString += ", "
        self.visit(keyword)
    self.astToString += ") "

  def visit_Tuple(self, node):
    self.astToString += "("
    self.visit(node.elts[0])
    for con in node.elts[1:]:
      self.astToString +=","
      self.visit(con)
    self.astToString += ") "

  def visit_List(self, node):
    self.astToString += "[ "
    self.visit(node)
    self.astToString += "] "

  def visit_ListComp(self, node):
    self.astToString += "[ "
    self.generic_Visit(node)
    self.astToString += "] "

  def visit_BinOp(self, node):
    self.visit(node.left)
    self.astToString += " " + binoptostring(node.op) + " "
    self.visit(node.right)

  def visit_For(self, node):
    self.astToString += "for( "
    self.visit(node.target)
    self.astToString += "in "
    self.visit(node.iter)
    for arg in node.body:
      self.visit(arg)
    for orelse in node.orelse:
      self.visit(orelse)

  def visit_While(self, node):
    self.astToString += "while "
    self.visit(node.test)
    for arg in node.body:
      self.visit(arg)
    for orelse in node.orelse:
      self.visit(orelse)

  def visit_If(self, node):
    self.astToString += "if "
    self.visit(node.test)
    for arg in node.body:
      self.visit(arg)
    for orelse in node.orelse:
      self.astToString += "el"
      self.visit(orelse)

  def visit_comprehension(self, node):
    self.astToString += "for "
    self.visit(node.target)
    self.astToString += "in "
    self.visit(node.iter)

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
    if isinstance(node.value, str):
      self.astToString += "'"
      self.astToString += node.value
      self.astToString += "'"
    else:
      self.astToString += str(node.value)

  def visit_Attribute(self, node):
    self.visit(node.value)
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
    self.visit(node.value)

  def visit_keyword(self, node):
    self.astToString += node.arg
    self.astToString += "="
    self.visit(node.value)

  def visit_UnaryOp(self, node):
    self.astToString += " " + unaroptostring(node.op)
    self.visit(node.operand)

  def visit_Lambda(self, node):
    self.visit(node.args)
    self.astToString += ":"
    self.visit(node.body)
    self.astToString += "\n"

  def visit_Dict(self, node):
    self.astToString += "{"
    for i in range(len(node.keys)):
      if i>0:
        self.astToString += ","
      self.visit(node.keys[i])
      self.astToString += ":"
      self.visit(node.values[i])
    self.astToString += "}"

  def visit_Continue(self, node):
    self.astToString += "continue"

  def visit_Break(self, node):
    self.astToString += "break"

  def visit_Global(self, node):
    self.visit(node.names)

  def print_methodlist(self):
    print(self.methodList)

  def print_astToString(self):
    print(self.astToString)


ppast(tree)
v = Analyzer()
v.visit(tree)
v.print_methodlist()
v.print_astToString()

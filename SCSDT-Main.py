import ast, contextlib
#from prettiest_ast import ppast

filename = "SCSDT-Main.py"

with open(filename) as src_file:
  tree = ast.parse(src_file.read())

BINOP_STR = { ast.Add: '+', ast.Mult: '*', ast.Sub: '-', ast.Div: '/', ast.Mod: '%', ast.Pow: '**' }

def binoptostring(op):
  return BINOP_STR[type(op)]

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
    self.astToString = ""
    self.lineno = 0
    self.indentation = ""

  def generic_Visit(self, node):
    """if self.lineno != node.lineno:
      self.lineno = node.lineno
      print(node.lineno)
      self.astToString += "\n"""""
    ast.NodeVisitor.generic_visit(self, node)

  def visit_ClassDef(self, node):
    self.add_text(node.name + "(")

    with self.no_indent():
      self.visit(node.bases[0])
      for el in node.bases:
        self.add_text(', ')
        self.visit(el)

      self.add_text("):")
    self.next_line()

    self.indent()
    for el in node.body:
      self.visit(el)
    self.dedent()
    self.next_line()
    self.next_line()

  def visit_FunctionDef(self, node):
    self.add_text("def " + node.name)
    with self.no_indent():
      self.visit(node.args)

    self.add_text(":")
    self.next_line()
    self.indent()
    for element in node.body:
      self.visit(element)
      self.next_line()
    self.dedent()
    self.next_line()
    self.next_line()

  def visit_Assign(self, node):
    for target in node.targets:
      self.visit(target)
      self.add_text(" = ")
    with self.no_indent():
      self.visit(node.value)


  def visit_AugAssign(self, node):
    self.visit(node.target)
    self.astToString += " " + binoptostring(node.op) + "= "
    self.visit(node.value)

  def visit_Name(self, node):
    self.add_text(node.id)

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
      self.astToString += ","
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
    self.astToString += "for "
    self.visit(node.target)
    self.astToString += " in "
    self.visit(node.iter)
    self.astToString += ":"
    self.next_line()
    self.indentation()
    for arg in node.body:
      self.toIndent()
      self.visit(arg)
      self.next_line()
    for orelse in node.orelse:
      self.visit(orelse)
    self.deindentation()

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
    self.next_line()
    self.indentation()
    for arg in node.body:
      self.toIndent()
      self.visit(arg)
      self.next_line()
    self.deindentation()
    for orelse in node.orelse:
      self.toIndent()
      self.astToString += "else: "
      self.next_line()
      self.toIndent()
      self.visit(orelse)

  def visit_comprehension(self, node):
    self.toIndent()
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

  def visit_Constant(self, node):
    if isinstance(node.value, str):
      self.astToString += "'"
      self.astToString += node.value
      self.astToString += "'"
    else:
      self.astToString += str(node.value)

  def visit_Attribute(self, node):
    self.visit(node.value)
    self.astToString += "." + node.attr

  def visit_Starred(self, node):
    self.astToString += str(node.value)

  def visit_Compare(self, node):
    self.visit(node.left)
    for i in range(len(node.ops)):
      self.astToString += " " + cmpopoptostring(node.ops[i]) + " "
      self.visit(node.comparators[i])

  def visit_NamedExpr(self, node):
    self.astToString += str(node.target)

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
    self.next_line()

  def visit_Dict(self, node):
    self.astToString += "{"
    for i in range(len(node.keys)):
      if i > 0:
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

  def indent(self):
    self.indentation = self.indentation + "  "

  def dedent(self):
    self.indentation = (len(self.indentation)-2) * " "

  def add_text(self, text):
    self.astToString += self.indentation + text

  def toIndent(self):
    self.astToString += self.indentation

  def next_line(self):
    self.astToString += "\n"

  @contextlib.contextmanager
  def no_indent(self):
      i = self.indentation
      self.indentation = ''
      yield
      self.indentation = i

  def __str__(self):
    return self.astToString


#ppast(tree)
v = Analyzer()
v.visit(tree)
print(v)

import ast, contextlib, glob
from os import listdir
from os.path import isfile, join
from prettiest_ast import ppast


BINOP_STR = {ast.Add: '+', ast.Mult: '*', ast.Sub: '-', ast.Div: '/', ast.Mod: '%', ast.Pow: '**' }
UNA_OP = {ast.Invert: '~', ast.Not: 'not', ast.UAdd: "+", ast.USub: "-"}
CMP_OP = {ast.Eq: "==", ast.NotEq: "!=", ast.Lt: "<", ast.LtE: "<=", ast.Gt: ">", ast.GtE: ">=", ast.Is: "is", ast.IsNot: "is not",
          ast.In: "in", ast.NotIn: "not in"}
BOOL_OP = {ast.And: "and", ast.Or: "or"}


def booloptostring(op):
  return BOOL_OP[type(op)]


def binoptostring(op):
  return BINOP_STR[type(op)]


def unaroptostring(op):
  return UNA_OP[type(op)]


def cmpopoptostring(op):
  return CMP_OP[type(op)]


def clown(x):
  if x==1 and x < 5 and x > -1 or x == 2:
    print(1)
  elif x==2:
    print(2)
  else:
    for i in range(10):
      x +=1


class Analyzer(ast.NodeVisitor):

  def __init__(self):
    self.astToString = ""
    self.lineno = 0
    self.indentation = ""
    self.newLine = True

  def generic_Visit(self, node):
    ast.NodeVisitor.generic_visit(self, node)

  def visit_ClassDef(self, node):
      self.next_line()
      with self.new_line():
        self.add_text("class " + node.name + "(")
        with self.no_indent():
          self.visit(node.bases[0])
          self.add_text(")")
      self.next_line()
      self.indent()
      for el in node.body:
        self.visit(el)
      self.dedent()

  def visit_FunctionDef(self, node):
    with self.new_line():
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

  def visit_Assign(self, node):
    with self.new_line():
      self.visit(node.targets[0])
      with self.no_indent():
        for target in node.targets[1:]:
          self.visit(target)
        self.add_text(" = ")
      with self.no_indent():
        self.visit(node.value)

  def visit_AugAssign(self, node):
    with self.new_line():
      self.visit(node.target)
      with self.no_indent():
        self.add_text(" " + binoptostring(node.op) + "= ")
        self.visit(node.value)

  def visit_Name(self, node):
    self.add_text(node.id)

  def visit_Num(self, node):
    self.add_text(str(node.n))

  def visit_Return(self, node):
    self.add_text("return ")
    with self.no_indent():
      self.generic_Visit(node)

  def visit_Call(self, node):
    with self.new_line():
      self.visit(node.func)
      with self.no_indent():
        self.add_text("(")
        if len(node.args) > 0:
          self.visit(node.args[0])
          for arg in node.args[1:]:
            self.add_text(", ")
            self.visit(arg)
        if len(node.keywords) > 0:
          self.visit(node.keywords[0])
          for keyword in node.keywords[1:]:
            with self.no_indent():
              self.add_text(", ")
              self.visit(keyword)
        self.add_text(")")

  def visit_Tuple(self, node):
    self.add_text("(")
    with self.no_indent():
      self.visit(node.elts[0])
      for con in node.elts[1:]:
        self.add_text(", ")
        self.visit(con)
      self.astToString += ")"

  def visit_List(self, node):
    self.add_text("[")
    with self.no_indent():
      self.visit(node)
    self.add_text("]")

  def visit_ListComp(self, node):
    with self.new_line():
      self.add_text("[ ")
      with self.no_indent():
        self.generic_Visit(node)
        self.add_text("]")

  def visit_BinOp(self, node):
    self.visit(node.left)
    with self.no_indent():
      self.add_text(" " + binoptostring(node.op) + " ")
      self.visit(node.right)

  def visit_For(self, node):
    with self.new_line():
      self.add_text("for ")
      with self.no_indent():
        self.visit(node.target)
        self.add_text(" in ")
        self.visit(node.iter)
        self.add_text(":")
      self.next_line()
      self.indent()
      for arg in node.body[:-1]:
        self.visit(arg)
        self.next_line()
      self.visit(node.body[-1])
      self.dedent()

  def visit_While(self, node):
    with self.new_line():
      self.add("while ")
      with self.no_indent():
        self.visit(node.test)
        self.next_line()
        self.indent()
        for arg in node.body[:-1]:
          self.visit(arg)
        self.visit(node.body[-1])

  def visit_If(self, node):
    with self.new_line():
      self.add_text("if ")
      with self.no_indent():
        self.visit(node.test)
        self.add_text(":")
      self.next_line()
      self.indent()
      for arg in node.body[:-1]:
        self.visit(arg)
        self.next_line()
      self.visit(node.body[-1])
      self.dedent()
      for orelse in node.orelse:
        self.next_line()
        self.add_text("else: ")
        self.next_line()
        self.indent()
        self.visit(orelse)
        self.dedent()

  def visit_comprehension(self, node):
    with self.new_line():
      self.add_text("for ")
      with self.no_indent():
        self.visit(node.target)
        self.add_text("in ")
        self.visit(node.iter)

  def visit_arguments(self, node):
    with self.new_line():
      with self.no_indent():
        self.astToString += "("
        if len(node.args) > 0:
          self.astToString += node.args[0].arg
          for arg in node.args[1:]:
            self.astToString += ", "
            self.visit_arg(arg)
        self.astToString += ")"

  def visit_arg(self, node):
    self.add_text(node.arg)

  def visit_Constant(self, node):
    with self.new_line():
      if node.value == "\n":
        self.add_text("\ n")
      elif isinstance(node.value, str):
        self.add_text("'")
        with self.no_indent():
          self.add_text(node.value + "'")
      else:
        self.add_text(str(node.value))

  def visit_Attribute(self, node):
    with self.new_line():
      self.visit(node.value)
      with self.no_indent():
        self.add_text("." + node.attr)

  def visit_Starred(self, node):
    self.add_text(node.value)

  def visit_Compare(self, node):
    self.visit(node.left)
    with self.no_indent():
      for i in range(len(node.ops)):
        self.add_text(" " + cmpopoptostring(node.ops[i]) + " ")
        self.visit(node.comparators[i])

  def visit_NamedExpr(self, node):
    self.add(str(node.target))

  def visit_Expr(self, node):
    self.visit(node.value)

  def visit_keyword(self, node):
    self.add(node.arg)
    with self.no_indent():
      self.add_text(" = ")
      self.visit(node.value)

  def visit_UnaryOp(self, node):
    with self.new_line():
      self.add_text(unaroptostring(node.op) + " ")
      with self.no_indent():
        self.visit(node.operand)

  def visit_Lambda(self, node):
    with self.new_line():
      self.visit(node.args)
      with self.no_indent():
        self.add(":")
        self.visit(node.body)
        self.next_line()

  def visit_Dict(self, node):
    self.add_text("{")
    with self.no_indent():
      for i in range(len(node.keys)):
        if i > 0:
          self.add_text(", ")
        self.visit(node.keys[i])
        self.add_text(": ")
        self.visit(node.values[i])
      self.add_text("}")

  def visit_Slice(self, node):
    self.add_text("[")
    with self.no_indent():
      try:
        self.visit(node.lower)
      except:
        pass
      self.add_text(":")
      try:
        self.visit(node.upper)
      except:
        pass
      self.add_text("]")

  def visit_Continue(self, node):
    self.add_text("continue")

  def visit_Pass(self, node):
    self.add_text("pass")

  def visit_Break(self, node):
    self.add_text("break")

  def visit_Global(self, node):
    self.visit(node.names)

  def visit_Yield(self, node):
      self.add_text("yield")

  def visit_With(self, node):
    with self.new_line():
      self.add_text("with ")
      with self.no_indent():
        if len(node.items) > 0:
          self.visit(node.items[0])
          for withitem in node.items[1:]:
            self.add_text(", ")
            self.visit(withitem)
            self.next_line()
        self.add_text(":")
      self.indent()
      self.next_line()
      for line in node.body[:-1]:
        self.visit(line)
        self.next_line()
      self.visit(node.body[-1])
      self.dedent()

  def visit_withitem(self, node):
    self.visit(node.context_expr)
    with self.no_indent():
      if node.optional_vars != None:
        self.add_text(" as ")
        self.visit(node.optional_vars)

  def visit_BoolOp(self, node):
    self.visit(node.values[0])
    with self.no_indent():
      for boolop in node.values[1:]:
        self.add_text(" " + booloptostring(node.op) + " ")
        self.visit(boolop)

  def visit_Try(self, node):
    with self.new_line():
      self.add_text("try:")
      self.next_line()
      self.indent()
      for expr in node.body:
        self.visit(expr)
        self.next_line()
      self.dedent()
      if len(node.handlers) != 0:
        for handler in node.handlers:
          self.add_text("except ")
          with self.no_indent():
            try:
              self.visit(handler.type)
            except:
              pass
            self.add_text(":")
          self.next_line()
          self.indent()
          for elem in handler.body[:-1]:
            self.visit(elem)
            self.next_line()
          self.visit(handler.body[-1])
          self.dedent()
      if len(node.orelse) != 0:
        self.add_text("else:")
        self.next_line()
        self.indent()
        for elem in node.orelse:
          self.visit(elem)
          self.next_line()
        self.dedent()
      if len(node.finalbody) != 0:
        self.add_text("finally:")
        self.next_line()
        self.indent()
        for elem in node.finalbody:
          self.visit(elem)
          self.next_line()
        self.dedent()

  def indent(self):
    self.indentation = self.indentation + "  "

  def dedent(self):
    self.indentation = (len(self.indentation)-2) * " "

  def add_text(self, text):
    self.astToString += self.indentation + text

  """def toIndent(self):
        self.astToString += self.indentation"""

  def next_line(self):
    self.astToString += "\n"

  @contextlib.contextmanager
  def no_indent(self):
    i = self.indentation
    self.indentation = ''
    yield
    self.indentation = i

  @contextlib.contextmanager
  def new_line(self):
    if self.newLine:
      self.next_line()
      self.newLine = False
      yield
      self.newLine = True
    else:
      yield

  def __str__(self):
    return self.astToString


class Transform(Analyzer):

  def __init__(self):
    super(Transform, self).__init__()

  def visit_FunctionDef(self, node):
    with self.new_line():
      self.add_text("def namedef")
      with self.no_indent():
        self.visit(node.args)
        self.add_text(":")
      self.next_line()
      self.indent()
      for element in node.body:
        self.visit(element)
        self.next_line()
      self.dedent()

  def visit_Call(self, node):
    with self.new_line():
      self.add_text("callFunc")
      with self.no_indent():
        self.add_text("(")
        if len(node.args) > 0:
          self.visit(node.args[0])
          for arg in node.args[1:]:
            self.add_text(", ")
            self.visit(arg)
        if len(node.keywords) > 0:
          self.visit(node.keywords[0])
          for keyword in node.keywords[1:]:
            with self.no_indent():
              self.add_text(", ")
              self.visit(keyword)
        self.add_text(")")
#ppast(tree)

filename = "SCSDT-Main.py"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

with open(filename) as src_file:
  tree = ast.parse(src_file.read())

v = Analyzer()
print(files)
s = Transform()
s.visit(tree)
print(s)

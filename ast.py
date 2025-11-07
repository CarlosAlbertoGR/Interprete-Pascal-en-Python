# ast.py

class AST:
    """Clase base para todos los nodos del Árbol de Sintaxis Abstracta."""
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Program(AST):
    def __init__(self, name, block):
        self.name = name
        self.block = block

class Block(AST):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement

class VarDecl(AST):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node

class Type(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Compound(AST):
    def __init__(self):
        self.children = []

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
        
class IfStatement(AST):
    """Nodo para la sentencia IF (IF condition THEN statement [ELSE statement])."""
    def __init__(self, condition, true_statement, false_statement=None):
        self.condition = condition
        self.true_statement = true_statement
        self.false_statement = false_statement

class WhileStatement(AST): # <-- ¡NUEVO NODO!
    """Nodo para la sentencia WHILE (WHILE condition DO statement)."""
    def __init__(self, condition, statement):
        self.condition = condition
        self.statement = statement
        
class NoOp(AST):
    pass
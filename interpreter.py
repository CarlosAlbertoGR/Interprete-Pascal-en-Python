# interpreter.py

from ast import (
    Program, Block, VarDecl, Type, Compound, 
    Assign, Var, NoOp, BinOp, Num, IfStatement, WhileStatement # <-- Importar WhileStatement
)
from token import TokenType

class NodeVisitor:
    """Clase base que implementa el patrón Visitor."""
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No existe el método visit_{type(node).__name__}')

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = {}

    def visit_BinOp(self, node):
        """Evalúa operaciones aritméticas y de comparación (booleanas)."""
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        
        # Operadores Aritméticos
        if node.op.type == TokenType.PLUS:
            return left_value + right_value
        elif node.op.type == TokenType.MINUS:
            return left_value - right_value
        elif node.op.type == TokenType.MUL:
            return left_value * right_value
        elif node.op.type == TokenType.DIV:
            return left_value // right_value 
        
        # Operadores de Comparación (Booleanos)
        elif node.op.type == TokenType.EQ:
            return left_value == right_value
        elif node.op.type == TokenType.LT:
            return left_value < right_value
        elif node.op.type == TokenType.GT:
            return left_value > right_value

    def visit_Num(self, node):
        return node.value

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_VarDecl(self, node):
        pass

    def visit_Type(self, node):
        pass

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Assign(self, node):
        var_name = node.left.value
        value = self.visit(node.right)
        self.GLOBAL_SCOPE[var_name] = value

    def visit_Var(self, node):
        var_name = node.value
        value = self.GLOBAL_SCOPE.get(var_name)
        if value is None:
            raise Exception(f'Error Semántico: Variable no inicializada o declarada "{var_name}"')
        return value

    def visit_IfStatement(self, node):
        """Ejecuta la sentencia IF-THEN-ELSE."""
        condition_result = self.visit(node.condition)
        
        if condition_result:
            self.visit(node.true_statement)
        elif node.false_statement is not None:
            self.visit(node.false_statement)

    def visit_WhileStatement(self, node): # <-- ¡NUEVO MÉTODO!
        """Ejecuta el bucle WHILE: evalúa la condición y ejecuta el cuerpo."""
        # Mientras la condición sea True, ejecuta la sentencia.
        while self.visit(node.condition):
            self.visit(node.statement)

    def visit_NoOp(self):
        pass

    def interpret(self):
        tree = self.parser.parse()
        if tree is None:
            return {}
        self.visit(tree)
        return self.GLOBAL_SCOPE
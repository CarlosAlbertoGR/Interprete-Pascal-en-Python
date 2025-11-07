# parser.py

from lexer import Lexer
from token import TokenType
from ast import (
    Program, Block, VarDecl, Type, Compound, 
    Assign, Var, NoOp, BinOp, Num, IfStatement, WhileStatement # <-- Importar WhileStatement
)

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None # Token se lee en parse()

    def error(self, expected_token_type=None):
        """Método para indicar un error sintáctico (la gramática fue violada)."""
        msg = f'Error Sintáctico: Token inesperado {self.current_token.type.name}'
        if expected_token_type:
            msg += f', se esperaba {expected_token_type.name}'
        raise Exception(msg)

    def eat(self, token_type):
        """Consume el token actual y avanza al siguiente."""
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(token_type)

    # --- Manejo de la Lógica Booleana ---

    def boolean_expr(self):
        """boolean_expr : expr ((EQ | LT | GT) expr)"""
        node = self.expr() 
        
        # Operadores de comparación
        if self.current_token.type in (TokenType.EQ, TokenType.LT, TokenType.GT):
            token = self.current_token
            
            if token.type == TokenType.EQ:
                self.eat(TokenType.EQ)
            elif token.type == TokenType.LT:
                self.eat(TokenType.LT)
            elif token.type == TokenType.GT:
                self.eat(TokenType.GT)
            
            node = BinOp(left=node, op=token, right=self.expr())
        
        return node

    # --- Nuevas Reglas de Flujo ---

    def if_statement(self):
        """if_statement : IF boolean_expr THEN statement [ELSE statement]"""
        self.eat(TokenType.IF)
        
        condition_node = self.boolean_expr()
        self.eat(TokenType.THEN)
        
        true_statement = self.statement()
        false_statement = None
        
        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            false_statement = self.statement()
        
        return IfStatement(condition_node, true_statement, false_statement)

    def while_statement(self): # <-- ¡NUEVA REGLA!
        """while_statement : WHILE boolean_expr DO statement"""
        self.eat(TokenType.WHILE)
        condition = self.boolean_expr()
        self.eat(TokenType.DO)
        statement = self.statement()
        
        return WhileStatement(condition, statement)

    def statement(self):
        """statement : compound_statement | assignment_statement | if_statement | while_statement | empty""" # <-- Añadido while_statement
        if self.current_token.type == TokenType.BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == TokenType.ID:
            node = self.assignment_statement()
        elif self.current_token.type == TokenType.IF:
            node = self.if_statement()
        elif self.current_token.type == TokenType.WHILE: # <-- Manejo del token WHILE
            node = self.while_statement()
        else:
            node = self.empty()
        return node
    
    # --- Métodos Base (program, block, declarations, etc.) ---
    
    def program(self):
        """program : PROGRAM variable SEMI block DOT"""
        self.eat(TokenType.PROGRAM)
        var_node = self.variable()
        prog_name = var_node.value
        self.eat(TokenType.SEMI)
        block_node = self.block()
        self.eat(TokenType.DOT)
        return Program(prog_name, block_node)

    def block(self):
        """block : declarations compound_statement"""
        declarations = self.declarations()
        compound_statement = self.compound_statement()
        return Block(declarations, compound_statement)

    def declarations(self):
        """declarations : VAR (variable_declaration SEMI)+ | empty"""
        declarations = []
        if self.current_token.type == TokenType.VAR:
            self.eat(TokenType.VAR)
            while self.current_token.type == TokenType.ID:
                decl = self.variable_declaration()
                declarations.extend(decl)
                self.eat(TokenType.SEMI)
        return declarations

    def variable_declaration(self):
        """variable_declaration : ID COLON type_spec"""
        var_nodes = [self.variable()]
        self.eat(TokenType.COLON)
        type_node = self.type_spec()
        return [VarDecl(var_node, type_node) for var_node in var_nodes]

    def type_spec(self):
        """type_spec : INTEGER"""
        token = self.current_token
        if self.current_token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Type(token)
        self.error()

    def compound_statement(self):
        """compound_statement : BEGIN statement_list END"""
        self.eat(TokenType.BEGIN)
        nodes = self.statement_list()
        self.eat(TokenType.END)
        
        root = Compound()
        for node in nodes:
            root.children.append(node)
        return root

    def statement_list(self):
        """statement_list : statement | statement SEMI statement_list"""
        statement = self.statement()
        results = [statement]

        while self.current_token.type == TokenType.SEMI:
            self.eat(TokenType.SEMI)
            results.append(self.statement())
        
        if self.current_token.type == TokenType.ID or \
           self.current_token.type == TokenType.BEGIN:
            self.error()
        return results
    
    def assignment_statement(self):
        """assignment_statement : variable ASSIGN expr"""
        left = self.variable()
        token = self.current_token
        self.eat(TokenType.ASSIGN)
        right = self.expr()
        return Assign(left, token, right)
    
    def variable(self):
        """variable : ID"""
        node = Var(self.current_token)
        self.eat(TokenType.ID)
        return node

    def empty(self):
        """empty : """
        return NoOp()

    # --- Reglas para Expresiones Aritméticas ---

    def expr(self):
        """expr : term ((PLUS | MINUS) term)*"""
        node = self.term()
        
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            
            node = BinOp(left=node, op=token, right=self.term())
        return node
        
    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()
        
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)

            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def factor(self):
        """factor : INTEGER_CONST | LPAREN expr RPAREN | variable"""
        token = self.current_token
        
        if token.type == TokenType.INTEGER_CONST:
            self.eat(TokenType.INTEGER_CONST)
            return Num(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        elif token.type == TokenType.ID:
            return self.variable()
        
        self.error()

    def parse(self):
        """Método principal: inicializa la lectura y comienza el parsing del programa."""
        # LECTURA DEL PRIMER TOKEN
        if self.current_token is None:
             self.current_token = self.lexer.get_next_token() 

        # Verificación del primer token
        if self.current_token.type != TokenType.PROGRAM:
             self.error(TokenType.PROGRAM)

        node = self.program()
        
        # Verifica que el último token sea EOF
        if self.current_token.type != TokenType.EOF:
            self.error()
        return node
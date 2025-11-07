# token.py

from enum import Enum

class TokenType(Enum):
    
    # --- Palabras Clave Estructurales de Pascal ---
    PROGRAM = 'PROGRAM'
    VAR = 'VAR'
    BEGIN = 'BEGIN'
    END = 'END'
    INTEGER = 'INTEGER'
    
    # --- Palabras Clave de Control de Flujo (IF/WHILE) ---
    IF = 'IF'
    THEN = 'THEN'
    ELSE = 'ELSE'
    WHILE = 'WHILE' # <-- NUEVO
    DO = 'DO'       # <-- NUEVO
    
    # --- Operadores Aritméticos ---
    PLUS = 'PLUS'         
    MINUS = 'MINUS'       
    MUL = 'MUL'           
    DIV = 'DIV'           
    
    # --- Operadores de Comparación (Booleanos) ---
    EQ = 'EQ'           # = (Igualdad)
    LT = 'LT'           # < (Menor que)
    GT = 'GT'           # > (Mayor que)
    
    # --- Delimitadores y Símbolos Especiales ---
    DOT = 'DOT'           # .
    SEMI = 'SEMI'         # ;
    COLON = 'COLON'       # :
    ASSIGN = 'ASSIGN'     # :=
    LPAREN = 'LPAREN'     # (
    RPAREN = 'RPAREN'     # )
    
    # --- Tipos de Tokens de Valor ---
    ID = 'ID'             
    INTEGER_CONST = 'INTEGER_CONST'
    EOF = 'EOF'           

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type.name}, {repr(self.value)})'
    
    def __repr__(self):
        return self.__str__()

# Palabras clave reservadas de Pascal
RESERVED_KEYWORDS = {
    'PROGRAM': Token(TokenType.PROGRAM, 'PROGRAM'),
    'VAR': Token(TokenType.VAR, 'VAR'),
    'BEGIN': Token(TokenType.BEGIN, 'BEGIN'),
    'END': Token(TokenType.END, 'END'),
    'INTEGER': Token(TokenType.INTEGER, 'INTEGER'),
    
    # Palabras clave de control de flujo
    'IF': Token(TokenType.IF, 'IF'),
    'THEN': Token(TokenType.THEN, 'THEN'),
    'ELSE': Token(TokenType.ELSE, 'ELSE'),
    'WHILE': Token(TokenType.WHILE, 'WHILE'), # <-- NUEVO
    'DO': Token(TokenType.DO, 'DO'),         # <-- NUEVO
}
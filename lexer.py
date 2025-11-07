# lexer.py

from token import Token, TokenType, RESERVED_KEYWORDS

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        """Método para indicar un error léxico (carácter no reconocido)."""
        # --- DEBUGGING DE CARÁCTER ---
        char_repr = repr(self.current_char)
        char_ascii = ord(self.current_char) if self.current_char else "None"
        raise Exception(f'Error Léxico: Carácter no válido: {char_repr} (ASCII: {char_ascii})')
        # -----------------------------
    def advance(self):
        """Avanza la posición y actualiza el carácter actual."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        """Ignora espacios en blanco y saltos de línea."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        """Ignora los comentarios de Pascal ({...})."""
        self.advance()
        while self.current_char is not None and self.current_char != '}':
            self.advance()
        
        if self.current_char == '}':
            self.advance()
        else:
            raise Exception('Error Léxico: Comentario no cerrado')
            
    def integer(self):
        """Retorna un número entero multi-dígito."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def _id(self):
        """Maneja identificadores y palabras clave reservadas."""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        # Convierte a mayúsculas y consulta RESERVED_KEYWORDS globalmente
        token = RESERVED_KEYWORDS.get(result.upper())
        
        if token is None:
            token = Token(TokenType.ID, result)
        return token

    def get_next_token(self):
        """El corazón del analizador: produce el siguiente token."""
        while self.current_char is not None:
            
            # 1. LIMPIEZA INICIAL (Ignora espacios y comentarios)
            while self.current_char is not None and \
                  (self.current_char.isspace() or self.current_char == '{'):
                
                if self.current_char.isspace():
                    self.skip_whitespace()
                elif self.current_char == '{':
                    self.skip_comment()
            
            # Si se terminó el archivo después de la limpieza
            if self.current_char is None:
                return Token(TokenType.EOF, None)

            # 2. RECONOCIMIENTO DE LETRAS/PALABRAS CLAVE (La 'P' de PROGRAM)
            # Este bloque DEBE ejecutarse para la 'P' (ASCII 80)
            if self.current_char.isalpha():
                return self._id()
            
            # 3. RECONOCIMIENTO DE NÚMEROS
            if self.current_char.isdigit():
                return Token(TokenType.INTEGER_CONST, self.integer())
            
            # 4. RECONOCIMIENTO DE SÍMBOLOS (Operadores y Delimitadores)
            
            # Paréntesis
            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(')
            
            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')')
            
            # Comparación y Asignación
            if self.current_char == '=':
                self.advance()
                return Token(TokenType.EQ, '=')
            
            if self.current_char == '<':
                self.advance()
                return Token(TokenType.LT, '<')
            
            if self.current_char == '>':
                self.advance()
                return Token(TokenType.GT, '>')
            
            if self.current_char == '+' :
                self.advance()
                return Token(TokenType.PLUS, '+')
            
            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')
            
            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MUL, '*')
            
            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIV, '/')
            
            if self.current_char == ':' and self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '=':
                self.advance()
                self.advance()
                return Token(TokenType.ASSIGN, ':=')

            if self.current_char == ':':
                self.advance()
                return Token(TokenType.COLON, ':')

            if self.current_char == ';':
                self.advance()
                return Token(TokenType.SEMI, ';')

            if self.current_char == '.':
                self.advance()
                return Token(TokenType.DOT, '.')

            # 5. ERROR (Si ninguna regla anterior aplica)
            self.error()

        return Token(TokenType.EOF, None)
# main.py (VERSIÓN FINAL DE PRUEBA con IF/WHILE)

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

# -----------------------------------------------------------
# CÓDIGO PASCAL DE PRUEBA CON WHILE
# Objetivo: sumar números del 1 al 4. Resultado esperado: 10
# -----------------------------------------------------------
text = """
PROGRAM ContadorWhile;
VAR
    contador : INTEGER;
    suma_total : INTEGER;
    flag : INTEGER;

BEGIN
    contador := 1;
    suma_total := 0;
    flag := 0;

    WHILE contador < 5 DO
    BEGIN
        suma_total := suma_total + contador;
        contador := contador + 1;
        
        IF contador = 3 THEN
            flag := 1;
    END; 
    
    IF flag = 1 THEN
        suma_total := suma_total + 10;
        
    { Resultado final esperado: 10 + 10 = 20 }
END.
"""
# Elimina todos los espacios alrededor del texto
text = text.strip() 
# -----------------------------------------------------------


def run_interpreter(text_input):
    """Función para encapsular el proceso completo de interpretación."""
    try:
        # FASE 1: Lexer
        lexer = Lexer(text_input) 
        
        # FASE 2: Parser
        parser = Parser(lexer)
        tree = parser.parse()
        
        print("✅ ANÁLISIS COMPLETO (Léxico y Sintáctico)")
        
        # FASE 3: Interpretación
        interpreter = Interpreter(parser)
        result_scope = interpreter.interpret()
        
        print("\n🚀 EJECUCIÓN COMPLETA")
        print("\n--- ÁMBITO GLOBAL (Memoria de variables) ---")
        for var, val in result_scope.items():
            print(f"    {var} = {val}")

    except Exception as e:
        print(f"\n❌ ERROR DETECTADO: {e}")

if __name__ == '__main__':
    run_interpreter(text)
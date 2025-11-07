# run_test.py

import sys
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
import os

def run_test(file_path):
    # 1. Lee el código de forma segura
    with open(file_path, 'r', encoding='utf-8') as f:
        pascal_code = f.read().strip()
    
    # 2. Inicializa el intérprete
    lexer = Lexer(pascal_code) 
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    
    # 3. Ejecuta y obtén el resultado
    global_scope = interpreter.interpret()
    
    # 4. Verificación del Resultado (para la Action)
    expected_total = 10
    actual_total = global_scope.get('total')

    if actual_total == expected_total:
        print(f"✅ ÉXITO: El test pasó. TOTAL = {actual_total}")
        sys.exit(0) # Salida 0 indica éxito
    else:
        print(f"❌ FALLO: Resultado inesperado. TOTAL esperado: {expected_total}, obtenido: {actual_total}")
        sys.exit(1) # Salida 1 indica fallo

if __name__ == '__main__':
    # Ejecuta el test usando el archivo test.pascal
    try:
        run_test('test.pascal')
    except Exception as e:
        print(f"❌ ERROR CRÍTICO DURANTE EL PARSING O EJECUCIÓN: {e}")
        sys.exit(1)
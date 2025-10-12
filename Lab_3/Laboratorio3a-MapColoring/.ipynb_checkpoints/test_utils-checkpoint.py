import numpy as np


import sys
import os

# --- Definición de Códigos de Color ANSI ---
# Estos códigos son universales para la mayoría de las terminales modernas
# y coinciden con los que solicitaste.
COLOR_SUCCESS = '\033[92m'  # Verde brillante
COLOR_FAIL = '\033[91m'     # Rojo brillante
COLOR_WARNING = '\033[93m'  # Amarillo brillante
COLOR_RESET = '\033[0m'     # Restablece el color de la terminal

def test_list(variable_a_verificar, contenido_esperado):
    """
    Verifica si una variable es una lista y si contiene todo el contenido esperado.
    
    Imprime el resultado con colores en la terminal.
    
    :param variable_a_verificar: La variable a ser examinada.
    :param contenido_esperado: Una lista con los elementos que se espera que contenga la variable.
    :return: True si la verificación es exitosa, False en caso contrario.
    """
    
    # Inicializar para soportar colores en terminales Windows
    if os.name == 'nt':
        os.system('') 
    
    print(f"\n--- Ejecutando Verificación ---")
    
    # 1. Verificar si es una lista
    if not isinstance(variable_a_verificar, list):
        print(f"{COLOR_FAIL}❌ Error de Tipo:{COLOR_RESET} La variable NO es una lista. Es de tipo: {type(variable_a_verificar).__name__}")
        return False

    print(f"{COLOR_SUCCESS}✅ Tipo Correcto:{COLOR_RESET} La variable es una lista.")
    
    # 2. Verificar el contenido
    elementos_faltantes = [item for item in contenido_esperado if item not in variable_a_verificar]
    
    if not elementos_faltantes:
        # Éxito: es una lista y contiene todo el contenido esperado
        print(f"{COLOR_SUCCESS}✅ Contenido Correcto:{COLOR_RESET} Todos los elementos esperados están presentes.")
        print(f"{COLOR_SUCCESS}--- PRUEBA EXITOSA ---{COLOR_RESET}")
        return True
    else:
        # Falla: es una lista, pero faltan elementos
        print(f"{COLOR_FAIL}❌ Contenido Incorrecto:{COLOR_RESET} Faltan los siguientes elementos: {elementos_faltantes}")
        print(f"{COLOR_FAIL}--- PRUEBA FALLIDA ---{COLOR_RESET}")
        return False

def test_dict(dict_a, dict_b, nombre_a="regiones programadas", nombre_b="regiones esperadas"):
    """
    Compara dos diccionarios, detalla las diferencias y emite el resultado final 
    como 'PRUEBA EXITOSA' o '--- PRUEBA FALLIDA ---'.

    :param dict_a: El primer diccionario.
    :param dict_b: El segundo diccionario.
    :param nombre_a: Nombre para mostrar en el resultado (ej. 'Diccionario Original').
    :param nombre_b: Nombre para mostrar en el resultado (ej. 'Diccionario Nuevo').
    :return: True si son idénticos, False en caso contrario.
    """
    
    # Inicializar para soportar colores en terminales Windows
    if os.name == 'nt':
        os.system('') 
    
    diferencias = []
    
    print(f"\n--- Comparando {nombre_a} y {nombre_b} ---")

    # 1. La forma más rápida: si son idénticos
    if dict_a == dict_b:
        print(f"{COLOR_SUCCESS}✅ Contenido Idéntico:{COLOR_RESET} Ambos diccionarios son exactamente iguales.")
        print(f"{COLOR_SUCCESS}PRUEBA EXITOSA{COLOR_RESET}")
        return True

    # 2. Claves presentes solo en A
    claves_solo_en_a = set(dict_a.keys()) - set(dict_b.keys())
    if claves_solo_en_a:
        diferencias.append(f"{COLOR_WARNING}Claves solo en {nombre_a}:{COLOR_RESET} {list(claves_solo_en_a)}")

    # 3. Claves presentes solo en B
    claves_solo_en_b = set(dict_b.keys()) - set(dict_a.keys())
    if claves_solo_en_b:
        diferencias.append(f"{COLOR_WARNING}Claves solo en {nombre_b}:{COLOR_RESET} {list(claves_solo_en_b)}")

    # 4. Claves que tienen valores diferentes
    claves_comunes = set(dict_a.keys()) & set(dict_b.keys())
    for clave in claves_comunes:
        # Nota: Esta comprobación puede ser superficial si los valores son listas u otros diccionarios mutables, 
        # pero para estructuras simples funciona correctamente.
        if dict_a[clave] != dict_b[clave]:
            diferencias.append(
                f"Clave '{clave}' difiere. "
                f"Valor en {nombre_a}: {dict_a[clave]}; "
                f"Valor en {nombre_b}: {dict_b[clave]}"
            )

    # 5. Mostrar resultados detallados si hay diferencias
    if diferencias:
        print(f"{COLOR_FAIL}❌ Diferencias Encontradas:{COLOR_RESET}")
        for dif in diferencias:
            print(f"   - {dif}")
        # Emitir la salida de PRUEBA FALLIDA
        print(f"{COLOR_FAIL}--- PRUEBA FALLIDA ---{COLOR_RESET}")
        return False
        
    # Esta línea es un fallback, pero por lo general el primer 'if' captura la igualdad.
    print(f"{COLOR_FAIL}--- PRUEBA FALLIDA ---{COLOR_RESET}")
    return False



import numpy as np
from test_utils import *

def test_domain(target):
	expected_output = ["rojo", "verde", "azul" ]
	test_list(target, expected_output)

    
def test_variables(target):
	expected_output = ["WA", "NT", "SA", "Q", "NSW", "V", "T"]
	test_list(target, expected_output)

def test_region_graph(target):
    expected_output =  {}
    expected_output["WA"] = ["NT", "SA"]
    expected_output["NT"] = ["WA", "SA", "Q"]
    expected_output["SA"] = ["WA", "NT", "Q", "NSW", "V"]
    expected_output["Q"] = ["NT", "SA", "NSW"]
    expected_output["NSW"] = ["Q", "SA", "V"]
    expected_output["V"] = ["SA", "NSW"]
    expected_output["T"] = []
    test_dict(target, expected_output)

# -------------------------------
# Casos de prueba (de las soluciones anteriores)
# -------------------------------

# Asignaciones consistentes
asignaciones_validas = [
    {'WA': 'rojo', 'NT': 'verde', 'SA': 'azul', 'Q': 'rojo', 'NSW': 'verde', 'V': 'rojo', 'T': 'rojo'},
    {'WA': 'azul', 'NT': 'rojo', 'SA': 'verde', 'Q': 'azul', 'NSW': 'rojo', 'V': 'azul', 'T': 'verde'},
    {'WA': 'verde', 'NT': 'rojo', 'SA': 'azul', 'Q': 'verde', 'NSW': 'rojo', 'V': 'verde', 'T': 'azul'},
    {'WA': 'azul', 'NT': 'verde', 'SA': 'rojo', 'Q': 'azul', 'NSW': 'verde', 'V': 'azul', 'T': 'rojo'}
]

# Asignaciones inconsistentes
asignaciones_invalidas = [
    {'WA': 'azul', 'NT': 'rojo', 'SA': 'rojo', 'Q': 'verde', 'NSW': 'azul', 'V': 'rojo', 'T': 'verde'},
    {'WA': 'rojo', 'NT': 'azul', 'SA': 'verde', 'Q': 'verde', 'NSW': 'verde', 'V': 'rojo', 'T': 'azul'},
    {'WA': 'verde', 'NT': 'rojo', 'SA': 'azul', 'Q': 'verde', 'NSW': 'rojo', 'V': 'azul', 'T': 'rojo'}
]

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

# ------------------------------------------------
# 🧪 Casos de prueba para remove_inconsistent_values
# ------------------------------------------------

test_cases_remove_inconsistent_values = [
    {
        "desc": "Caso 1: Eliminación simple",
        "input": {"Xi": "WA", "Xj": "NT", "dominios": {"WA": ["rojo", "verde"], "NT": ["rojo"]}},
        "expected_dominios": {"WA": ["verde"], "NT": ["rojo"]},
        "expected_result": True
    },
    {
        "desc": "Caso 2: Sin conflicto",
        "input": {"Xi": "WA", "Xj": "NT", "dominios": {"WA": ["rojo", "verde"], "NT": ["azul"]}},
        "expected_dominios": {"WA": ["rojo", "verde"], "NT": ["azul"]},
        "expected_result": False
    },
    {
        "desc": "Caso 3: Dominio vacío tras eliminación",
        "input": {"Xi": "SA", "Xj": "V", "dominios": {"SA": ["rojo"], "V": ["rojo"]}},
        "expected_dominios": {"SA": [], "V": ["rojo"]},
        "expected_result": True
    },
    {
        "desc": "Caso 4: Al menos un valor compatible",
        "input": {"Xi": "Q", "Xj": "NSW", "dominios": {"Q": ["rojo", "verde"], "NSW": ["rojo", "azul"]}},
        "expected_dominios": {"Q": ["rojo", "verde"], "NSW": ["rojo", "azul"]},
        "expected_result": False
    },
    {
        "desc": "Caso 5: Propagación de restricción a Xk",
        "input": {"Xi": "A", "Xj": "B", "dominios": {"A": ["rojo", "verde"], "B": ["rojo"], "C": ["rojo", "verde"]}},
        "expected_dominios": {"A": ["verde"], "B": ["rojo"], "C": ["rojo", "verde"]},
        "expected_result": True
    }
]


# ------------------------------------------------
# 🧪 Casos de prueba para remove_inconsistent_values (versión extendida)
# ------------------------------------------------

test_cases_remove_inconsistent_values_ac_3 = [
    {
        "desc": "Caso 1: No debe eliminar valores si no hay conflicto.",
        "input": {
            "Xi": "A",
            "Xj": "B",
            "dominios": {"A": ["rojo", "verde"], "B": ["azul"]}
        },
        "expected_dominios": {"A": ["rojo", "verde"], "B": ["azul"]},
        "expected_result": False
    },
    {
        "desc": "Caso 2: Debe eliminar el valor 'rojo' de A.",
        "input": {
            "Xi": "A",
            "Xj": "B",
            "dominios": {"A": ["rojo", "verde"], "B": ["rojo"]}
        },
        "expected_dominios": {"A": ["verde"], "B": ["rojo"]},
        "expected_result": True
    },
    {
        "desc": "Caso 3: Xi debe quedar vacío si todos los valores son inconsistentes.",
        "input": {
            "Xi": "A",
            "Xj": "B",
            "dominios": {"A": ["rojo"], "B": ["rojo"]}
        },
        "expected_dominios": {"A": [], "B": ["rojo"]},
        "expected_result": True
    },
    {
        "desc": "Caso 4: No debe eliminar valores si hay al menos un color distinto en B.",
        "input": {
            "Xi": "A",
            "Xj": "B",
            "dominios": {"A": ["rojo", "verde"], "B": ["rojo", "azul"]}
        },
        "expected_dominios": {"A": ["rojo", "verde"], "B": ["rojo", "azul"]},
        "expected_result": False
    },
    {
        "desc": "Caso 5: Debe eliminar 'azul' de A, dejando solo 'rojo'.",
        "input": {
            "Xi": "A",
            "Xj": "B",
            "dominios": {"A": ["rojo", "azul"], "B": ["azul"]}
        },
        "expected_dominios": {"A": ["rojo"], "B": ["azul"]},
        "expected_result": True
    },
    {
        "desc": "Caso 6: Propagación correcta A -> B -> C (B pierde 'rojo', luego C pierde 'verde').",
        "input": {
            "Xi": "B",
            "Xj": "A",
            "dominios": {"A": ["rojo"], "B": ["rojo", "verde"], "C": ["rojo", "verde", "azul"]},
            "propagacion": True  # se usará para ejecutar el segundo paso (C,B)
        },
        "expected_dominios": {"A": ["rojo"], "B": ["verde"], "C": ["rojo", "azul"]},
        "expected_result": True
    }
]

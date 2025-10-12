def es_consistente(variable, valor, asignacion, vecinos):
    for vecino in vecinos[variable]:
        if vecino in asignacion and asignacion[vecino] == valor:
            return False
    return True


def backtracking(asignacion, dominios, vecinos, variables):
    if len(asignacion) == len(variables):
        return asignacion

    # Selecciona una variable no asignada
    var = next(v for v in variables if v not in asignacion)

    for valor in dominios[var]:
        if es_consistente(var, valor, asignacion, vecinos):
            nueva_asig = asignacion.copy()
            nueva_asig[var] = valor
            resultado = backtracking(nueva_asig, dominios, vecinos, variables)
            if resultado:
                return resultado
    return None

def pretty_print(nodo, indent=0):
    espacio = '  ' * indent
    if nodo is None:
        print(f"{espacio}None")
        return

    clase = nodo.__class__.__name__

    if clase == 'Programa':
        print(f"{espacio}Programa:")
        for stmt in nodo.sentencias:
            pretty_print(stmt, indent + 1)

    elif clase == 'Portal':
        print(f"{espacio}Portal: {nodo.nombre}({', '.join(nodo.parametros)})")
        for stmt in nodo.cuerpo:
            pretty_print(stmt, indent + 1)

    elif clase == 'Si':
        print(f"{espacio}Si:")
        print(f"{espacio}  Condición:")
        pretty_print(nodo.condicion, indent + 2)
        print(f"{espacio}  Entonces:")
        for stmt in nodo.entonces:
            pretty_print(stmt, indent + 2)
        print(f"{espacio}  Sino:")
        for stmt in nodo.sino:
            pretty_print(stmt, indent + 2)

    elif clase == 'Asignacion':
        print(f"{espacio}Asignación: {nodo.id} =")
        pretty_print(nodo.expresion, indent + 1)

    elif clase == 'ExpresionBinaria':
        print(f"{espacio}Expresión binaria: {nodo.op}")
        pretty_print(nodo.izq, indent + 1)
        pretty_print(nodo.der, indent + 1)

    elif clase == 'Identificador':
        print(f"{espacio}Identificador: {nodo.nombre}")

    elif clase == 'Numero':
        print(f"{espacio}Número: {nodo.valor}")

    else:
        print(f"{espacio}{clase} (no manejado)")

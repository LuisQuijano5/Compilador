class Nodo:
    pass

class Programa(Nodo):
    def __init__(self, sentencias):
        self.sentencias = sentencias

class Portal(Nodo):
    def __init__(self, nombre, parametros, cuerpo):
        self.nombre = nombre
        self.parametros = parametros
        self.cuerpo = cuerpo

class Si(Nodo):
    def __init__(self, condicion, entonces, sino):
        self.condicion = condicion
        self.entonces = entonces
        self.sino = sino

class Asignacion(Nodo):
    def __init__(self, id, expresion):
        self.id = id
        self.expresion = expresion

class ExpresionBinaria(Nodo):
    def __init__(self, izq, op, der):
        self.izq = izq
        self.op = op
        self.der = der

class Identificador(Nodo):
    def __init__(self, nombre):
        self.nombre = nombre

class Numero(Nodo):
    def __init__(self, valor):
        self.valor = valor
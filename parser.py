from ast_nodes import *
from Token import Token

# Códigos de tokens
EOF = 1
PORTAL = 1017
SI = 1020
SINO = 1021
ID = 6000
INT = 7000
FLOAT = 8000
LPAREN = 5001
RPAREN = 5002
LBRACE = 4001
RBRACE = 4002
ASSIGN = 2031
SEMICOLON = 3003
COMMA = 3002
PLUS = 2021
MINUS = 2022
MUL = 2011
DIV = 2012

class DummyToken:
    def __init__(self):
        self.type = EOF
        self.value = 'EOF'

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.sync_tokens = [SEMICOLON, RBRACE]

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        else:
            return Token(EOF, '', -1, -1)

    def match(self, expected_type):
        if self.current().type == expected_type:
            self.pos += 1
        else:
            self.error(f"Se esperaba tipo {expected_type}, se encontró {self.current().type}")

    def error(self, mensaje):
        print(f"[Error] {mensaje} en token {self.current().type} (posición {self.pos})")
        self.panic()

    def panic(self):
        while self.current().type not in self.sync_tokens and self.current().type != EOF:
            self.pos += 1
        if self.current().type in self.sync_tokens:
            self.pos += 1
        elif self.current().type == EOF:
            return  # deja de avanzar más allá

    def parse(self):
        sentencias = self.lista_sentencias()
        return Programa(sentencias)

    def lista_sentencias(self):
        sentencias = []
        while self.current().type in [PORTAL, ID, SI]:
            s = self.sentencia()
            if s:
                sentencias.append(s)
        return sentencias

    def sentencia(self):
        tipo = self.current().type
        if tipo == PORTAL:
            return self.sentencia_portal()
        elif tipo == SI:
            return self.sentencia_si()
        elif tipo == ID:
            return self.sentencia_asignacion()
        else:
            self.error("Sentencia no válida")
            return None

    def sentencia_portal(self):
        self.match(PORTAL)
        nombre = self.current().value
        self.match(ID)
        self.match(LPAREN)
        parametros = self.parametros()
        self.match(RPAREN)
        self.match(LBRACE)
        cuerpo = self.lista_sentencias()
        self.match(RBRACE)
        return Portal(nombre, parametros, cuerpo)

    def parametros(self):
        params = []
        if self.current().type == ID:
            params.append(self.current().value)
            self.match(ID)
            while self.current().type == COMMA:
                self.match(COMMA)
                params.append(self.current().value)
                self.match(ID)
        return params

    def sentencia_si(self):
        self.match(SI)
        self.match(LPAREN)
        cond = self.expresion()
        self.match(RPAREN)
        self.match(LBRACE)
        entonces = self.lista_sentencias()
        self.match(RBRACE)
        self.match(SINO)
        self.match(LBRACE)
        sino = self.lista_sentencias()
        self.match(RBRACE)
        return Si(cond, entonces, sino)

    def sentencia_asignacion(self):
        id_nombre = self.current().value
        self.match(ID)
        self.match(ASSIGN)
        expr = self.expresion()
        self.match(SEMICOLON)
        return Asignacion(id_nombre, expr)

    def expresion(self):
        izq = self.termino()
        while self.current().type in [PLUS, MINUS]:
            op = self.current().value
            self.match(self.current().type)
            der = self.termino()
            izq = ExpresionBinaria(izq, op, der)
        return izq

    def termino(self):
        izq = self.factor()
        while self.current().type in [MUL, DIV]:
            op = self.current().value
            self.match(self.current().type)
            der = self.factor()
            izq = ExpresionBinaria(izq, op, der)
        return izq

    def factor(self):
        tipo = self.current().type
        valor = self.current().value
        if tipo == INT or tipo == FLOAT:
            self.match(tipo)
            return Numero(valor)
        elif tipo == ID:
            self.match(ID)
            return Identificador(valor)
        elif tipo == LPAREN:
            self.match(LPAREN)
            expr = self.expresion()
            self.match(RPAREN)
            return expr
        else:
            self.error("Expresión inválida")
            return Numero(0)  # valor por defecto para no romper


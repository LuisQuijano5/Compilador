from warnings import catch_warnings

from unicodedata import numeric

from series import *
from ast_nodes import *

class Simbolo:
    def __init__(self, nombre, tipo, ambito, es_funcion=False, parametros=None, tipo_retorno=None):
        self.nombre = nombre
        self.tipo = tipo
        self.ambito = ambito
        self.es_funcion = es_funcion
        self.parametros = parametros or []
        self.tipo_retorno = tipo_retorno


class Entorno:
    def __init__(self):
        self.ambitos = [{}]  # lista de diccionarios para representar los ámbitos

    def entrar_ambito(self):
        self.ambitos.append({})

    def salir_ambito(self):
        self.ambitos.pop()

    def declarar(self, nombre, simbolo):
        self.ambitos[-1][nombre] = simbolo

    def buscar(self, nombre):
        for ambito in reversed(self.ambitos):
            if nombre in ambito:
                return ambito[nombre]
        return None

    def existe_en_actual(self, nombre):
        return nombre in self.ambitos[-1]


class AnalizadorSemantico:
    def __init__(self):
        self.entorno = Entorno()
        self.funcion_actual = None
        self.errores = []

    def analizar(self, nodo):
        metodo = f"visitar_{type(nodo).__name__}"
        visitador = getattr(self, metodo, self.visitar_desconocido)
        return visitador(nodo)

    def visitar_desconocido(self, nodo):
        self.errores.append(f"[Error] Nodo no reconocido: {type(nodo).__name__}")

    def visitar_Programa(self, nodo):
        self.entorno.entrar_ambito()
        for sentencia in nodo.sentencias:
            self.analizar(sentencia)
        self.entorno.salir_ambito()

    def visitar_DeclaracionFuncion(self, nodo):
        if self.entorno.existe_en_actual(nodo.nombre):
            self.errores.append(f"[Error] Función '{nodo.nombre}' ya declarada en este ámbito")
        tipo_retorno = self.inferir_tipo_retorno(nodo.cuerpo)
        simbolo = Simbolo(nodo.nombre, 'funcion', ambito='local', es_funcion=True, parametros=nodo.parametros, tipo_retorno=tipo_retorno)
        self.entorno.declarar(nodo.nombre, simbolo)
        self.entorno.entrar_ambito()
        for param in nodo.parametros:
            if self.entorno.existe_en_actual(param):
                self.errores.append(f"[Error] Parámetro '{param}' ya declarado en esta función")
            self.entorno.declarar(param, Simbolo(param, 'item', ambito='local'))
        self.funcion_actual = nodo.nombre
        # contiene_tp = False
        # for sentencia in nodo.cuerpo:
        #     self.analizar(sentencia)
        #     if isinstance(sentencia, SentenciaTP):
        #         contiene_tp = True
        # if not contiene_tp:
        #     self.errores.append(f"[Error] La función '{nodo.nombre}' no contiene una sentencia TELETRANSPORTAR")
        self.funcion_actual = None
        self.entorno.salir_ambito()

    def inferir_tipo_retorno(self, cuerpo):
        for s in cuerpo:
            if isinstance(s, SentenciaTP) and s.destino:
                return self.analizar(s.destino)
        return 'item' #esto no estoy seguro, tal vez no esta bien

    def visitar_SentenciaDeclaracion(self, nodo):
        if self.entorno.existe_en_actual(nodo.nombre):
            self.errores.append(f"[Error] Variable '{nodo.nombre}' ya declarada en este ámbito")
        tipo = self.obtener_tipo_nombre(nodo.tipo)
        self.entorno.declarar(nodo.nombre, Simbolo(nodo.nombre, tipo, ambito='local'))
        if hasattr(nodo, 'valor') and nodo.valor:
            tipo_valor = self.analizar(nodo.valor)
            if not self.comparar_tipos(tipo, tipo_valor):
                self.errores.append(f"[Error] Tipo incompatible en asignación a '{nodo.nombre}': {tipo} = {tipo_valor}")

    def visitar_SentenciaAsignacion(self, nodo):
        simbolo = self.entorno.buscar(nodo.nombre)
        if simbolo is None:
            self.errores.append(f"[Error] Variable '{nodo.nombre}' no declarada")
        else:
            tipo_valor = self.analizar(nodo.valor)
            if not self.comparar_tipos(simbolo.tipo, tipo_valor):
                self.errores.append(f"[Error] Tipo incompatible en asignación a '{nodo.nombre}': {simbolo.tipo} = {tipo_valor}")

    def visitar_SentenciaSi(self, nodo):
        tipo_cond = self.analizar(nodo.condicion)
        if tipo_cond != 'palanca':
            self.errores.append(f"[Error] Condición del SI debe ser de tipo palanca, se encontró '{tipo_cond}'")
        self.entorno.entrar_ambito()
        for s in nodo.entonces:
            self.analizar(s)
        self.entorno.salir_ambito()
        if nodo.sino:
            self.entorno.entrar_ambito()
            for s in nodo.sino:
                self.analizar(s)
            self.entorno.salir_ambito()

    def visitar_SentenciaMientras(self, nodo):
        tipo_cond = self.analizar(nodo.condicion)
        if tipo_cond != 'palanca':
            self.errores.append(f"[Error] Condición del MIENTRAS debe ser de tipo palanca, se encontró '{tipo_cond}'")
        self.entorno.entrar_ambito()
        for s in nodo.cuerpo:
            self.analizar(s)
        self.entorno.salir_ambito()

    def visitar_SentenciaPara(self, nodo):
        self.entorno.entrar_ambito()
        self.analizar(nodo.inicial)
        tipo_cond = self.analizar(nodo.condicion)
        if tipo_cond != 'palanca':
            self.errores.append(f"[Error] La condición en PARA debe ser de tipo palanca, se encontró '{tipo_cond}'")
        self.analizar(nodo.actualizacion)
        for s in nodo.cuerpo:
            self.analizar(s)
        self.entorno.salir_ambito()

    def visitar_ExpresionLiteral(self, nodo):
        try:
            if '.' in nodo.valor:
                float_val = float(nodo.valor)
                return 'losa'
            else:
                int_val = int(nodo.valor)
                return 'bloque'
        except ValueError:
            return 'item'
        except TypeError:
            if isinstance(nodo.valor, int):
                return 'bloque'
            elif isinstance(nodo.valor, float):
                print("hey")
                return 'losa'
            return 'item'

    def visitar_ExpresionBooleana(self, nodo):
        return 'palanca'

    def visitar_ExpresionIdentificador(self, nodo):
        simbolo = self.entorno.buscar(nodo.nombre)
        if simbolo is None:
            self.errores.append(f"[Error] Variable '{nodo.nombre}' no declarada")
            return 'item'
        return simbolo.tipo

    def visitar_ExpresionAccesoArreglo(self, nodo):
        simbolo = self.entorno.buscar(nodo.nombre)
        if simbolo is None:
            self.errores.append(f"[Error] Variable '{nodo.nombre}' no declarada")
            return 'item'
        if simbolo.tipo != 'cofre':
            self.errores.append(f"[Error] Variable '{nodo.nombre}' no es un cofre y se intenta indexar")
        tipo_indice = self.analizar(nodo.indice)
        if tipo_indice != 'bloque':
            self.errores.append(f"[Error] El índice en '{nodo.nombre}[exp]' debe ser de tipo bloque, se recibió '{tipo_indice}'")
        return 'item'

    def visitar_ExpresionLlamadaFuncion(self, nodo):
        simbolo = self.entorno.buscar(nodo.funcion)
        if simbolo is None or not simbolo.es_funcion:
            return self.verificar_funcion_nativa(nodo)
        if len(nodo.argumentos) != len(simbolo.parametros):
            self.errores.append(f"[Error] Número de argumentos inválido para función '{nodo.funcion}'")
        else:
            for arg, param in zip(nodo.argumentos, simbolo.parametros):
                tipo_arg = self.analizar(arg)
                tipo_param = self.entorno.buscar(param).tipo if self.entorno.buscar(param) else 'item'
                if not self.comparar_tipos(tipo_arg, tipo_param):
                    self.errores.append(f"[Error] Tipo de argumento incompatible en llamada a '{nodo.nombre}': {tipo_arg} ≠ {tipo_param}")
        return simbolo.tipo_retorno or 'item'

    def verificar_funcion_nativa(self, nodo):
        nombre = nodo.nombre.upper()
        args = [self.analizar(arg) for arg in nodo.argumentos]
        if nombre == 'CHAT':
            return 'item'
        if nombre == 'ANTORCHAR':
            if args and args[0] != 'palanca':
                self.errores.append("[Error] ANTORCHAR espera una expresión de tipo palanca")
            return 'item'
        if nombre in ['CRAFTEAR', 'ROMPER', 'APILAR', 'REPARTIR', 'SOBRAR', 'ENCANTAR']:
            if len(args) != 2:
                self.errores.append(f"[Error] {nombre} espera exactamente 2 argumentos")
            else:
                for i, tipo in enumerate(args):
                    if tipo not in ['bloque', 'losa', 'item']:
                        self.errores.append(f"[Error] Argumento {i+1} de {nombre} debe ser tipo numérico")
                if nombre == 'SOBRAR' and 'losa' in args:
                    self.errores.append("[Error] SOBRAR no permite valores tipo losa (debe ser entero)")
                if nombre == 'REPARTIR' and len(nodo.argumentos) == 2:
                    segundo = nodo.argumentos[1]
                    if isinstance(segundo, ExpresionLiteral) and segundo.valor == 0:
                        self.errores.append("[Error] Segundo argumento de REPARTIR no puede ser cero")
            return 'item'
        self.errores.append(f"[Error] Función '{nodo.nombre}' no declarada")
        return 'item'

    def visitar_ExpresionBinaria(self, nodo):
        tipo_izq = self.analizar(nodo.izquierda)
        tipo_der = self.analizar(nodo.derecha)
        if nodo.operador in ['+', '-', '*', '/', '%']:
            if tipo_izq in ['bloque', 'losa', 'item'] and tipo_der in ['bloque', 'losa', 'item']:
                if nodo.operador in ['/', '%'] or 'losa' in [tipo_izq, tipo_der]:
                    return 'losa'
                if 'item' in [tipo_izq, tipo_der]:
                    return 'item'
                return 'bloque'
            else:
                self.errores.append(f"[Error] Operación aritmética inválida entre '{tipo_izq}' y '{tipo_der}'")
                return 'item'
        elif nodo.operador in ['==']:
            if self.comparar_tipos(tipo_izq, tipo_der):
                return 'palanca'
            else:
                self.errores.append(f"[Error] Comparación de igualdad inválida entre '{tipo_izq}' y '{tipo_der}'")
                return 'item'
        elif nodo.operador in ['<', '>', '<=', '>=']:
            if tipo_izq in ['bloque', 'losa'] and tipo_der in ['bloque', 'losa']:
                return 'palanca'
            else:
                self.errores.append(f"[Error] Comparación relacional inválida entre '{tipo_izq}' y '{tipo_der}'")
                return 'item'
        elif nodo.operador in ['y', 'o']:
            if tipo_izq == 'palanca' and tipo_der == 'palanca':
                return 'palanca'
            else:
                self.errores.append(f"[Error] Operación lógica inválida entre '{tipo_izq}' y '{tipo_der}'")
                return 'item'
        return 'item'

    def visitar_SentenciaTP(self, nodo):
        if self.funcion_actual is None:
            self.errores.append(f"[Error] TELETRANSPORTAR sólo se permite dentro de funciones")
        if nodo.destino:
            self.analizar(nodo.destino)

#tal vez agregar para strings?? al menos el ==
    def comparar_tipos(self, tipo_destino, tipo_origen):
        if tipo_destino == tipo_origen:
            return True
        if tipo_destino == 'item':
            return True
        if tipo_destino == 'losa' and (tipo_origen == 'losa' or tipo_origen == 'bloque'):
            return True
        if tipo_destino == 'bloque' and (tipo_origen == 'losa' or tipo_origen == 'item'):
            return False
        return False

    def obtener_tipo_nombre(self, token_type):
        tipos = {
            BLOQUE: 'bloque',
            LOSA: 'losa',
            PALANCA: 'palanca',
            LIBRO: 'libro',
            HOJA: 'hoja',
            COFRE: 'cofre',
            ITEM: 'item'
        }
        return tipos.get(token_type, 'item')
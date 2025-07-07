from excel import Excel
from textfile import TextFile
from algorithm import Automaton

def main():
    excel = Excel()
    resultsfile=TextFile()
    textfile = TextFile()

    resultsfile.clear('Tokens.txt')
    resultsfile.clear('Lists.txt')

    excel.open()
    textfile.open()
    # while True:
    #     if excel.open():
    #        break
    #     print("Porfa selecciona el archivo de la matriz excel")
    #
    # while True:
    #     if textfile.open():
    #         break
    #     print("Porfa selecciona el archivo de texto a revisar")

    excel_data = excel.read()
    textfile_data = textfile.read()
    #textfile_data = "Hello\rWorld\this is a test."

    matrix = [i[1:] for i in excel_data[1:]]
    sigma = excel_data[0][1:]
    Q = [i[0] for i in excel_data[1:]]
    q0 = Q[0]
    F = [998, 999]
    for row in matrix:
        for i in row:
            if i and i not in F and i > 999:
                F.append(i)

    automaton = Automaton(matrix, sigma, Q, q0, F)
    tokens, identifiers, strings, errors = automaton.run(textfile_data)

    if not tokens:
        print("El archivo no arrojo resultado, favor de revisar")
    else:
        #print("Done")
        resultsfile.write(tokens)
        resultsfile.write_symbol_data(identifiers, strings)
        if errors:
            resultsfile.write_errors(errors)
            print("Hubo errores lexicos")

    # for token in tokens:
    #     print(token.value, token.index, token.length)
    #     print(repr(textfile_data[token.index:token.index+token.length]))

    from parser import Parser
    from pretty_print import pretty_print

    # lista de tokens como antes
    parser = Parser(tokens)
    ast = parser.parse()
    syntax_errors = parser.errors
    for error in syntax_errors:
        print(error.value)
    #print(pretty_print(ast))
    #print("Posición final del parser:", parser.pos, "/", len(tokens))

    from semantic import AnalizadorSemantico

    sem = AnalizadorSemantico()
    sem.visitar_Programa(ast)
    #print(sem.entorno.imprimir_historial())
    for error in sem.errores:
        print(error)


    from intermediate import GeneradorIntermedio

    generador = GeneradorIntermedio()
    generador.generar(ast)
    # for instr in generador.instrucciones:
    #     print(instr)

    from optimizer import OptimizadorCodigoIntermedio

    opt = OptimizadorCodigoIntermedio(generador.instrucciones)
    opt.optimizar()
    # for ins in opt.codigo_intermedio:
    #     print(ins)

    from backend import PythonCode

    exe = PythonCode(opt.codigo_intermedio)
    exe.translate()
    exe.save_n_exec()


if __name__ == "__main__":
    main()
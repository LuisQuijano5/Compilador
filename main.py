from excel import Excel
from textfile import TextFile
from algorithm import Automaton
from parser import BacktrackingParser

def normalize_indent_tokens(tokens, base_indent_value=100000, newline_token=9100, semicolon_token = 3020):
    normalized = []
    indent_stack = [0]
    i = 0
    after_newline = True
    after_semicolon = False

    while i < len(tokens):
        token = tokens[i]

        if token == semicolon_token:
            after_semicolon = True
            normalized.append(str(token))
            i += 1
            continue
        elif token == newline_token and after_semicolon:
            normalized.append(str(token))
            after_newline = True
            i += 1
            continue

        if after_newline:
            if isinstance(token, int) and token >= base_indent_value:
                space_count = token - base_indent_value + 1
                i += 1
            else:
                space_count = 0

            if space_count > indent_stack[-1]:
                indent_stack.append(space_count)
                normalized.append("INDENT")
            elif space_count < indent_stack[-1]:
                while indent_stack and space_count < indent_stack[-1]:
                    indent_stack.pop()
                    normalized.append("DEDENT")
                if indent_stack[-1] != space_count:
                    return False
            after_newline = False
            continue

        if isinstance(token, int) and token >= base_indent_value:
            pass
        else:
            normalized.append(str(token))

        i += 1

    while len(indent_stack) > 1:
        indent_stack.pop()
        normalized.append("DEDENT")

    return normalized



def main():
    excel = Excel()
    resultsfile=TextFile()
    textfile = TextFile()

    resultsfile.clear('Tokens.txt')

    while True:
        if excel.open():
           break
        print("Porfa selecciona el archivo de la matriz excel")

    while True:
        if textfile.open():
            break
        print("Porfa selecciona el archivo de texto a revisar")

    excel_data = excel.read()
    textfile_data = textfile.read()

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
    result = automaton.run(textfile_data)

    if not result:
        resultsfile.write("0")
        print("El archivo no arrojo resultado, favor de revisar")
    else:
        tokens = normalize_indent_tokens(result)
        resultsfile.write(tokens)
        print("Terminado. Revisar el archivo de texto Tokens")

    # while True:
    #     if excel.open():
    #         break
    #     print("Porfa selecciona el archivo de la gramatica excel")
    # excel_data = excel.read_asymmetrical()
    #
    #
    #
    # tokens = normalize_indent_tokens(result)
    # grammar = {}
    # for rule in excel_data:
    #     head = rule[0]
    #     bodies = rule[1:]
    #     if head not in grammar:
    #         grammar[head] = []
    #     for body in bodies:
    #         if isinstance(body, str):
    #             body = body.strip()
    #             if body == 'E':
    #                 grammar[head].append([])
    #             else:
    #                 symbols = body.split()
    #                 grammar[head].append(symbols)
    #         else:
    #             grammar[head].append([str(body)])
    #
    # print(grammar)
    # print(tokens)
    # parser = BacktrackingParser(tokens, grammar, '<p>')
    # print(parser.run())

if __name__ == "__main__":
    main()
class Automaton:
    def __init__(self, matrix, sigma, Q, q0, F):
        self.Q = Q
        self.matrix = matrix
        self.sigma = sigma
        self.q0 = q0
        self.F = F

    def run(self, text):
        list = []
        identifiers = []
        numbers = []
        strings = []
        i = 0
        line_pos = 0
        n_line = 1
        while i < len(text):
            current = self.q0
            j = i
            blanks = 0
            accepted = False
            word = ""

            while j < len(text):
                symbol = text[j]
                if symbol.isdigit():
                    symbol = int(symbol)

                if symbol == "\n":
                    symbol = "\\n"
                if symbol == " ":
                    symbol = "\\s"
                    if current == 8:
                        blanks += 1

                if symbol not in self.sigma:
                    current = 996 if 1 < current < 8 else 997
                    break

                current = self.matrix[self.Q.index(current)][self.sigma.index(symbol)]

                if current in self.F:
                    accepted = True
                    break

                j += 1
                line_pos += 1
                word += str(symbol)

            i = j
            if 996 <= current <= 999:
                list.clear()
                if current == 999:
                    list.append(f"LEXICAL ERROR, invalid identifier in line {n_line} near position " + str(line_pos))
                elif current == 998:
                    list.append(f"LEXICAL ERROR, invalid numerical literal in line {n_line} near position " + str(line_pos))
                elif current == 997:
                    list.append(f"LEXICAL ERROR, invalid identifier in line {n_line} near position {line_pos}. (non recognized symbol at: {line_pos})")
                elif current == 996:
                    list.append(f"LEXICAL ERROR, invalid numerical literal in line {n_line} near position {line_pos}. (non recognized symbol at: {line_pos})")
                break
                # j += 1
                # line_pos += 1
                # i = j
            elif accepted:#agregar a la matriz lo de eof
                if 6000 <= current < 7000:
                    if word not in [identifier[0] for identifier in identifiers]:
                        identifiers.append((word, len(identifiers) + current))
                elif 7000 <= current < 9000:
                    if word not in [str(num[0]) for num in numbers]:
                        numbers.append((float(word) if '.' in word else int(word), len(numbers) + current))
                elif current == 3040:
                    if word not in [string[0] for string in strings]:
                        strings.append((word, len(strings) + current))

                if blanks > 0:
                    list.append(100000 + blanks)
                else:
                    list.append(current)
                    if current == 9100:
                        line_pos = 0
                        n_line += 1
                i = j
            elif j == len(text):
                if blanks > 0:
                    list.append(100000 + blanks)
                else:
                    current = self.matrix[self.Q.index(current)][self.sigma.index("\\n")]
                    if current == 999:
                        list.append("LEXICAL ERROR, invalid identifier near position: " + str(line_pos))
                    elif current == 998:
                        list.append("LEXICAL ERROR, invalid numerical literal near position: " + str(line_pos))
                    elif current == 997:
                        list.append("LEXICAL ERROR, non recognized symbol at: " + str(line_pos))
                    else:
                        list.append(current)
                break

        return list, identifiers, numbers, strings





class Automaton:
    def __init__(self, matrix, sigma, Q, q0, F):
        self.Q = Q
        self.matrix = matrix
        self.sigma = sigma
        self.q0 = q0
        self.F = F

    def run(self, text):
        list = []
        i = 0
        line_pos = 0
        while i < len(text):
            current = self.q0
            j = i
            blanks = 0
            accepted = False

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
                    #print(f"Invalid symbol '{symbol}' at position {j}")
                    current = 996 if 1 < current < 8 else 997
                    break

                current = self.matrix[self.Q.index(current)][self.sigma.index(symbol)]

                if current in self.F:
                    #print(f"Accepted token from {i} to {j} (final state: {current})")
                    accepted = True
                    break

                j += 1
                line_pos += 1

            i = j
            if 996 <= current <= 999:
                if current == 999:
                    list.append("LEXICAL ERROR, invalid identifier near position: " + str(line_pos))
                elif current == 998:
                    list.append("LEXICAL ERROR, invalid numerical literal near position: " + str(line_pos))
                elif current == 997:
                    list.append(f"LEXICAL ERROR, invalid identifier near position: {line_pos}. (non recognized symbol at: {line_pos})")
                elif current == 996:
                    list.append(f"LEXICAL ERROR, invalid numerical literal near position: {line_pos}. (non recognized symbol at: {line_pos})")
                j += 1
                line_pos += 1
                i = j
            elif accepted:#agregar a la matriz lo de eof
                if blanks > 0:
                    list.append(100000 + blanks)
                else:
                    list.append(current)
                    if current == 9100:
                        line_pos = 0
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

        return list





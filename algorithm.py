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
                    print(f"Invalid symbol '{symbol}' at position {j}")
                    break

                current = self.matrix[self.Q.index(current)][self.sigma.index(symbol)]

                if current in self.F:
                    print(f"Accepted token from {i} to {j} (final state: {current})")
                    accepted = True
                    break

                j += 1

            if current == 999:
                list = ["error lexico en simbolo: " + str(j + 1)]
                break
            elif accepted:#agregar a la matriz lo de eof
                if blanks > 0:
                    list.append(100000 + blanks)
                else:
                    list.append(current)
                i = j
            elif j == len(text):
                if blanks > 0:
                    list.append(100000 + blanks)
                else:
                    current = self.matrix[self.Q.index(current)][self.sigma.index("\\n")]
                    if current == 999:
                        list = ["error lexico en simbolo: " + str(j + 1)]
                    else:
                        list.append(current)
                break
            # else:
            #     print(f"No accepting state reached starting at position {i}")
            #     i+=1

        return list





import os
import tkinter as tk
from tkinter import filedialog

class TextFile:
    def __init__(self):
        self.file_path = None
        self.result_path = "Tokens.txt"
        self.root = tk.Tk()

    def open(self):
        self.root.withdraw()
        self.file_path = filedialog.askopenfilename(title="Introduce el archivo de texto a revisar",
                                                    filetypes=[("Text Files", "*.txt")])
        if self.file_path:
            return True
        return False

    def read(self):
        with open(self.file_path, "r") as file:
            content = file.read()
        return content

    def write(self, content):
        try:
            with open(self.result_path, "a") as file:
                for item in content:
                    file.write(f"{item}   ")
                    if item == '9100':
                        file.write(f"\n")
        except Exception as e:
            print(f"An error occurred: {e}")

    def write_symbol_data(self, identifiers, numbers, strings):
        try:
            with open("Lists.txt", "a", encoding="utf-8") as file:
                col_width = 40

                file.write(f"{'IDENTIFIER'.ljust(col_width)}MEMORY\n")
                file.write("-" * (col_width + 10) + "\n")
                for name, address in identifiers:
                    file.write(f"{name.ljust(col_width)}{address}\n")
                file.write("\n\n")

                file.write(f"{'NUMERICAL CONSTANT'.ljust(col_width)}MEMORY\n")
                file.write("-" * (col_width + 10) + "\n")
                for value, address in numbers:
                    file.write(f"{str(value).ljust(col_width)}{address}\n")
                file.write("\n\n")

                file.write(f"{'STRING'.ljust(col_width)}MEMORY\n")
                file.write("-" * (col_width + 10) + "\n")
                for string, address in strings:
                    file.write(f"{string.ljust(col_width)}{address}\n")
                file.write("\n\n")

        except Exception as e:
            print(f"An error occurred, could list the items: {e}")

    def clear(self, filename):
        if os.path.exists(filename):
            try:
                with open(filename, "w") as file:
                    file.truncate(0)
            except Exception as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    textfile = TextFile()
    textfile.open()
    content = textfile.read()
    textfile.clear(textfile.result_path)
    textfile.write(content)
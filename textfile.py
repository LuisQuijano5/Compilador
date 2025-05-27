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
        n_line = 1
        try:
            with open(self.result_path, "a") as file:
                file.write(f"LINE NO {n_line}\n")
                for item in content:
                    file.write(f"{item}   ")
                    if item == '9100':
                        n_line += 1
                        file.write(f"\n\nLINE NO {n_line}\n")
        except Exception as e:
            print(f"An error occurred: {e}")

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
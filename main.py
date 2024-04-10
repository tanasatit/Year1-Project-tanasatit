import tkinter as tk
from tkinter import ttk


class DemoUI(tk.Tk):
    def __int__(self):
        self.title("Playstation")

    def init_components(self):
        pass

    def run(self):
        self.mainloop()


if __name__ == '__main__':
    x = DemoUI()
    x.run()

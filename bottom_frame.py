import tkinter as tk


class BottomFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="yellow",  height=50, pady=5, bd=4, relief=tk.RAISED)
        self.parent = parent
        self.grid(row=2, column=0, sticky="nsew")
        # TODO fill this

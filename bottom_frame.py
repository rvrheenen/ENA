import tkinter as tk


class BottomFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="yellow",  height=50, pady=5, bd=4, relief=tk.RAISED)
        self.parent = parent
        self.grid(row=2, column=0, sticky="nsew")
        self.lbl_copyright = tk.Label(self, text="© 2018-2019 Robin Vergouwen & Rick van Rheenen")
        self.lbl_copyright.grid(row=0, column=0, sticky="ns", pady=10)
        self.columnconfigure(0, weight=1)
        # TODO fill this

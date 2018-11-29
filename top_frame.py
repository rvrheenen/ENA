import tkinter as tk


class TopFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="yellow", pady=5, bd=4, relief=tk.RAISED)
        self.parent = parent
        self.grid(row=0, sticky="new", ipady=5)

        # create widgets
        self.lbl_dim_enter = tk.Label(self, text="Enter the dimensions of the area: ")
        self.txt_dim_x = tk.Entry(self, width=5)
        self.lbl_dim_mult = tk.Label(self, text="x")
        self.txt_dim_y = tk.Entry(self, width=5)
        self.btn_dim_start = tk.Button(self, text="START", command=self.click_start)

        # place widgets
        self.txt_dim_x.grid(column=1, row=0, padx=2)
        self.lbl_dim_enter.grid(column=0, row=0, padx=2)
        self.lbl_dim_mult.grid(column=2, row=0, padx=2)
        self.txt_dim_y.grid(column=3, row=0, padx=2)
        self.btn_dim_start.grid(column=5, row=0, padx=2)

    def click_start(self):
        self.btn_dim_start['text'] = "RESTART"
        self.parent.start()

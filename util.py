import tkinter as tk
from tkinter import font, messagebox

class Helper:
    @staticmethod
    def message_box(type, title, message):
        {
            "info": messagebox.showinfo,
            "warning": messagebox.showwarning,
            "error": messagebox.showerror
        }[type](title, message)


class OptionMenu(tk.OptionMenu):
    ''' Extend the tk OptionMenu to have a function that fixes its width to its content.'''
    def _set_max_width(self, *args):
        f = tk.font.nametofont(self.cget("font"))
        zerowidth = f.measure("0")
        w = round(max([f.measure(i) for i in args]) / zerowidth)

        self.config(width=w)


class Selectors(list):
    def __init__(self):
        self._inner_list = list()
        self.TYPE_COVERAGE = "coverage"
        self.TYPE_ITEM = "item"

        self.append(self.Selector(self, "basic coverage", self.TYPE_COVERAGE, "yellow"))
        self.append(self.Selector(self, "high coverage", self.TYPE_COVERAGE, "orange"))
        self.append(self.Selector(self, "intense coverage", self.TYPE_COVERAGE, "red"))
        self.append(self.Selector(self, "no coverage needed", self.TYPE_COVERAGE, "white"))
        self.append(self.Selector(self, "not on map", self.TYPE_COVERAGE, "black"))
        self.append(self.Selector(self, "uplink", self.TYPE_ITEM, ""))
        self.append(self.Selector(self, "cable", self.TYPE_ITEM, ""))
        self.append(self.Selector(self, "AP", self.TYPE_ITEM, ""))

    def get_by_name(self, name):
        for sel in self:
            if sel.name == name:
                return sel

    def names(self):
        return [s.name for s in self]

    class Selector:
        def __init__(self, p, n, t, r):
            self.parent = p
            self.name = n
            self.type = t
            self.repr = r

        def __repr__(self):
            return self.name

        def is_draggable(self):
            return self.type == self.parent.TYPE_COVERAGE

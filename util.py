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
    def set_max_width(self, *args):
        f = tk.font.nametofont(self.cget("font"))
        zerowidth = f.measure("0")
        w = round(max([f.measure(i) for i in args]) / zerowidth)

        self.config(width=w)


class Selectors(list):
    TYPE_COVERAGE = "coverage"
    TYPE_ITEM = "item"

    DISTANCE_FOR_BASIC = 20
    DISTANCE_FOR_HIGH = 10
    DISTANCE_FOR_INTENSE = 5

    def __init__(self, fill=None):
        self._inner_list = list()

        if fill == None:
            self.append(self.Selector(self, "basic coverage", self.TYPE_COVERAGE, "yellow", check=self.DISTANCE_FOR_BASIC))
            self.append(self.Selector(self, "high coverage", self.TYPE_COVERAGE, "orange", check=self.DISTANCE_FOR_HIGH))
            self.append(self.Selector(self, "intense coverage", self.TYPE_COVERAGE, "red", check=self.DISTANCE_FOR_INTENSE))
            self.append(self.Selector(self, "no coverage needed", self.TYPE_COVERAGE, "white"))
            self.append(self.Selector(self, "not on map", self.TYPE_COVERAGE, "gray"))
            self.append(self.Selector(self, "uplink", self.TYPE_ITEM, "U"))
            self.append(self.Selector(self, "cable", self.TYPE_ITEM, "C"))
            self.append(self.Selector(self, "AP", self.TYPE_ITEM, "A"))
        else:
            for thing in fill:
                self.append(thing)

    def get_by_name(self, name):
        for sel in self:
            if sel.name == name:
                return sel

    def get_by_repr(self, repr):
        for sel in self:
            if sel.repr == repr:
                return sel

    def names(self):
        return [s.name for s in self]

    def of_type(self, type):
        return Selectors([sel for sel in self if sel.type == type])

    class Selector:
        def __init__(self, p, n, t, r, **kwargs):
            self.parent = p
            self.name = n
            self.type = t
            self.repr = r

            # print(kwargs)
            for k, v in kwargs.items():
                setattr(self, k, v)

        def __repr__(self):
            return self.name

        def hasattr(self, a):
            return hasattr(self, a)

        def is_draggable(self):
            return self.type == self.parent.TYPE_COVERAGE

class Trial:
    ''' Allows for one-line try with no errors without except
        EG: with Trial(): doesntexist.destroy()
    '''
    def __enter__(self):
        pass

    def __exit__(self, *args):
        return True

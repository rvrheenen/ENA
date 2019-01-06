import tkinter as tk
from tkinter import font, messagebox
import configparser

class Helper:
    '''
    Class with helper functions to be used at various places throughout the project
    '''
    @staticmethod
    def message_box(type, title, message):
        '''
        Display message
        :param type:
        :param title:
        :param message:
        :return:
        '''
        {
            "info": messagebox.showinfo,
            "warning": messagebox.showwarning,
            "error": messagebox.showerror
        }[type](title, message)


class OptionMenu(tk.OptionMenu):
    '''
    Extend the tk OptionMenu to have a function that fixes its width to its content.
    '''
    def set_max_width(self, *args):
        '''
        Set the width of the optionmenu to fit content
        :param args:
        :return:
        '''
        f = tk.font.nametofont(self.cget("font"))
        zerowidth = f.measure("0")
        w = round(max([f.measure(i) for i in args]) / zerowidth)

        self.config(width=w)


class Settings(configparser.ConfigParser):
    '''
    Class that reads the configuration from the settings file.
    '''
    DEFAULT_CONFIG_FILE = "settings.ini"

    def __init__(self, config_file=None):
        configparser.ConfigParser.__init__(self)
        self.config_file = self.DEFAULT_CONFIG_FILE if config_file is None else config_file
        self.read(self.config_file)

    def write_changes(self):
        with open(self.config_file, 'w') as configfile:
            self.write(configfile)


class Selectors(list):
    TYPE_COVERAGE = "coverage"
    TYPE_ITEM = "item"

    def __init__(self, fill=None):
        self._inner_list = list()

        if fill == None:
            settings = Settings()
            self.append(self.Selector(self, "basic coverage", self.TYPE_COVERAGE, "yellow", check=settings.getfloat('DISTANCES', 'distance_for_basic')))
            self.append(self.Selector(self, "high coverage", self.TYPE_COVERAGE, "orange", check=settings.getfloat('DISTANCES', 'distance_for_high')))
            self.append(self.Selector(self, "intense coverage", self.TYPE_COVERAGE, "red", check=settings.getfloat('DISTANCES', 'distance_for_intense')))
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

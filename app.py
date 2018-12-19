import tkinter as tk
from menu_bar import *
from top_frame import *
from center_frame import *
from bottom_frame import *
from util import Helper

WIDTH = 1280
HEIGHT = 800
DEBUG = False


class App(tk.Tk):
    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent

        # Set constants
        self.width  = WIDTH
        self.height = HEIGHT
        self.debug  = DEBUG

        #initialize app
        self.initialize()

    def initialize(self):
        # placeholder vars
        self.dim_x = 10
        self.dim_y = 10

        # dimensions
        if [self.winfo_screenwidth(), self.winfo_screenheight()] == [1680, 1050]:
            self.attributes("-fullscreen", True)
        else:
            self.geometry('1680x1050')


        # Create frames
        self.menu_bar = MenuBar(self)
        self.config(menu=self.menu_bar)
        self.top_frame = TopFrame(self)
        self.center_frame = CenterFrame(self)
        self.bottom_frame = BottomFrame(self)

        # configure rows of frames,
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        # self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=0)

    def reinitialize(self):
        for thing in ["menu_bar", "top_frame", "center_frame", "bottom_frame"]:
            if hasattr(self, thing):
                try:
                    self.__getattribute__(thing).destroy()
                except:
                    pass

        self.initialize()

    def start(self):
        try:
            self.dim_x = int(self.top_frame.txt_dim_x.get())
            self.dim_y = int(self.top_frame.txt_dim_y.get())
            self.center_frame = CenterFrame(self)
            self.center_frame.start_map_design()
        except ValueError as e:
            Helper.message_box("error", "Bad Input", "Illegal values, please try again")

    def load(self, dim_x, dim_y, ena_map):
        self.dim_x = dim_x
        self.dim_y = dim_y

        # set the dimension parameters in input fields
        self.top_frame.txt_dim_x.delete('0', 'end')
        self.top_frame.txt_dim_y.delete('0', 'end')
        self.top_frame.txt_dim_x.insert('0', dim_x)
        self.top_frame.txt_dim_y.insert('0', dim_y)

        # initialize center frame with loaded file
        self.center_frame = CenterFrame(self)
        self.center_frame.start_map_design(ena_map)

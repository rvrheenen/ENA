import tkinter as tk
from ENA.util import Selectors, OptionMenu

class CenterFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="gray", padx=5, pady=5)
        self.parent = parent
        self.grid(row=1, column=0, ipady=5, sticky="nsew")

        if parent.debug:
            self.start_map_design()

    ##### MAP METHODS
    def start_map_design(self):
        self.set_parameters()
        self.create_map_settings()
        self.create_map_canvas()
        self.create_map_legend()

    def set_parameters(self):
        # TODO generate more intelligent dimensions and square_size
        self.dim_x = self.parent.dim_x
        self.dim_y = self.parent.dim_y
        self.square_size = 20
        self.selectors = Selectors()

    def create_map_settings(self):
        self.lbl_instruct = tk.Label(self, text="Choose cursor: ")
        self.lbl_instruct.grid(column=0, row=0, sticky="nw", pady=10)

        self.selector = tk.StringVar(self)
        self.selector.set(self.selectors[0].name)
        self.selector_menu = OptionMenu(self, self.selector, *self.selectors.names())
        self.selector_menu._set_max_width(*self.selectors.names())
        self.selector_menu.grid(row=0, column=1, sticky="nw", padx=10)
        menu = self.selector_menu["menu"]

        self.num_selector = tk.StringVar(self)
        self.num_selector.set(1)
        self.num_selector_menu = tk.OptionMenu(self, self.num_selector, *range(1,9))
        self.num_selector_menu.grid(row=0, column=2, sticky="nw", padx=10)

    def create_map_canvas(self):
        try:
            self.canvas.destroy()  # remove canvas if it exists
        except:
            pass
        self.canvas = tk.Canvas(self, bg="gray", height=self.square_size*self.dim_y + 1)
        self.canvas.grid(column=0, row=1, sticky="new", columnspan=3)
        self.grid_columnconfigure(2, weight=1)

        self.squares = []
        for x in range(self.parent.dim_x):
            squares_row = []
            for y in range(self.parent.dim_y):
                square = self.canvas.create_rectangle(self.square_size*x + 1,
                                                      self.square_size*y + 1,
                                                      self.square_size*x + self.square_size+1,
                                                      self.square_size*y + self.square_size+1)
                squares_row.append(square)
            self.squares.append(squares_row)

        self.canvas.bind("<ButtonPress-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def create_map_legend(self):
        self.lbl_legend_head = tk.Label(self, text="Legend:")
        self.lbl_legend_head.grid(column=3, row=1, sticky="ne")

    ##### CLICK EVENTS
    def on_click(self, event):
        self._dragging = True
        self.on_move(event)

    def on_move(self, event):
        ss = self.square_size

        def sq_offset(c):  # used to correct mismatching of closest element.
            return max(0, (c - ss // 2) if c % ss > ss // 2 else c)

        cursor_in_map = event.x < self.dim_x * ss
        if cursor_in_map and self._dragging:
            items = self.canvas.find_closest(sq_offset(event.x), sq_offset(event.y))
            if items:
                rect_id = items[0]
                selector = self.selectors.get_by_name(self.selector.get())
                if selector.is_draggable():
                    self.canvas.itemconfigure(rect_id, fill=selector.repr)
                else:
                    self._dragging = False

    def on_release(self, event):
        self._dragging = False

import tkinter as tk
from PIL import Image, ImageTk
import pyscreenshot as ImageGrab # TODO check OS compatibility
from io import BytesIO
from util import Selectors, OptionMenu, Trial



class CenterFrame(tk.Frame):
    def __init__(self, parent):
        self.DRAW_MODE_COVERAGE = "coverage"
        self.DRAW_MODE_ITEMS = "item"
        self.draw_mode = self.DRAW_MODE_COVERAGE

        tk.Frame.__init__(self, parent, bg="gray", padx=5, pady=5)
        self.parent = parent
        self.grid(row=1, column=0, ipady=5, sticky="nsew")

        if parent.debug:
            self.start_map_design()

    ##### MAP METHODS
    def start_map_design(self):
        self.grid_columnconfigure(3, weight=1)
        self.set_parameters()
        self.create_map_settings()
        self.create_map_canvas()
        self.create_map_legend()

    def set_parameters(self):
        # TODO generate more intelligent dimensions and square_size
        self.dim_x = self.parent.dim_x
        self.dim_y = self.parent.dim_y
        self.square_size = 20
        self.selector_options = Selectors()

    def create_map_settings(self):
        self.btn_toggle_draw_mode= tk.Button(self, text="item mode", command=self.click_toggle_draw_mode)
        self.btn_toggle_draw_mode.grid(row=0, column=0, pady=10)

        self.lbl_instruct = tk.Label(self, text="Choose cursor: ")
        self.lbl_instruct.grid(row=0, column=1, sticky="nw", pady=10)

        self.coverage_options = self.selector_options.of_type(self.DRAW_MODE_COVERAGE)
        self.selector_coverage = tk.StringVar(self)
        self.selector_coverage.set(self.coverage_options[0].name)
        self.selector_menu_coverage = OptionMenu(self, self.selector_coverage, *self.coverage_options.names())
        self.selector_menu_coverage.set_max_width(*self.coverage_options.names())
        self.selector_menu_coverage.grid(row=0, column=2, sticky="nw", padx=10)
        self.selector_menu_coverage.grid_remove()

        self.item_options = self.selector_options.of_type(self.DRAW_MODE_ITEMS)
        self.selector_items = tk.StringVar(self)
        self.selector_items.set(self.item_options[0].name)
        self.selector_menu_items = OptionMenu(self, self.selector_items, *self.item_options.names(), command=self.selector_menu_items_selection_event)
        self.selector_menu_items.set_max_width(*self.item_options.names())
        self.selector_menu_items.grid(row=0, column=2, sticky="nw", padx=10)
        self.selector_menu_items.grid_remove()

        self.num_selector = tk.StringVar(self)
        self.num_selector.set(1)
        self.num_selector_menu = tk.OptionMenu(self, self.num_selector, *range(1,9))
        self.num_selector_menu.grid(row=0, column=3, sticky="nw", padx=10)
        self.num_selector_menu.grid_remove()

    def click_toggle_draw_mode(self):
        if self.draw_mode == self.DRAW_MODE_COVERAGE:
            self.set_draw_mode(self.DRAW_MODE_ITEMS)
        else:
            self.set_draw_mode(self.DRAW_MODE_COVERAGE)

    def selector_menu_items_selection_event(self):
        if self.draw_mode == self.DRAW_MODE_ITEMS and self.selector_items.get() == "cable":
            self.num_selector_menu.grid()
        else:
            self.num_selector_menu.grid_remove()

    def set_draw_mode(self, mode):
        self.draw_mode = mode

        if mode == self.DRAW_MODE_COVERAGE:
            tk.Misc.lift(self.canvas_coverage)  # activate coverage canvas

            self.selector_menu_items.grid_remove()
            self.selector_menu_coverage.grid()
            self.btn_toggle_draw_mode['text'] = f"{self.DRAW_MODE_ITEMS} mode"
            self.selector_menu_items_selection_event()

        elif mode == self.DRAW_MODE_ITEMS:
            tk.Misc.lift(self.canvas_items)

            self.selector_menu_coverage.grid_remove()
            self.selector_menu_items.grid()
            self.btn_toggle_draw_mode['text'] = f"{self.DRAW_MODE_COVERAGE} mode"
            self.selector_menu_items_selection_event()

            box = (self.canvas_coverage.winfo_rootx(),
                   self.canvas_coverage.winfo_rooty(),
                   self.canvas_coverage.winfo_rootx() + self.canvas_coverage.winfo_width(),
                   self.canvas_coverage.winfo_rooty() + self.canvas_coverage.winfo_height() )

            fp = BytesIO()
            ImageGrab.grab(bbox=box).save(fp, 'PNG')
            self.canvas_items.background = ImageTk.PhotoImage(Image.open(fp))

            self.canvas_items.create_image(0, 0, image=self.canvas_items.background, anchor=tk.NW)

    def create_map_canvas(self):
        with Trial(): self.canvas_coverage.destroy()  # remove canvas_coverage if it exists
        with Trial(): self.canvas_items.destroy()  # remove canvas_items if it exists

        self.canvas_coverage = tk.Canvas(self, height=self.square_size*self.dim_y + 1)
        self.canvas_coverage.grid(column=0, row=1, sticky="new", columnspan=4)

        for x in range(self.parent.dim_x):
            for y in range(self.parent.dim_y):
                self.canvas_coverage.create_rectangle(self.square_size * x + 1,
                                                      self.square_size * y + 1,
                                                      self.square_size * x + self.square_size + 1,
                                                      self.square_size * y + self.square_size + 1)

        self.canvas_items = tk.Canvas(self, height=self.square_size*self.dim_y + 1)
        self.canvas_items.grid(column=0, row=1, sticky="new", columnspan=4)
        self.canvas_items.create_oval(10,10,20,20)

        for canv in [self.canvas_coverage, self.canvas_items]:
            canv.bind("<ButtonPress-1>", self.on_click)
            canv.bind("<B1-Motion>", self.on_move)
            canv.bind("<ButtonRelease-1>", self.on_release)

        self.set_draw_mode(self.DRAW_MODE_COVERAGE)

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
            if self.draw_mode == self.DRAW_MODE_COVERAGE:
                items = self.canvas_coverage.find_closest(sq_offset(event.x), sq_offset(event.y))
                if items:
                    rect_id = items[0]
                    selector = self.coverage_options.get_by_name(self.selector_coverage.get())
                    self.canvas_coverage.itemconfigure(rect_id, fill=selector.repr)

            elif self.draw_mode == self.DRAW_MODE_ITEMS:
                pass
                # TODO make the rest of the map draw things

    def on_release(self, event):
        self._dragging = False

    def create_map_legend(self):
        # TODO Fill the legend
        self.lbl_legend_head = tk.Label(self, text="Legend:")
        self.lbl_legend_head.grid(column=3, row=1, sticky="ne")

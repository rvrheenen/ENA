import tkinter as tk
from PIL import Image, ImageTk
import pyscreenshot as ImageGrab
from io import BytesIO
import math
from util import Selectors, OptionMenu, Trial, Helper
from ena_map import ENAMap
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
import time


class CenterFrame(tk.Frame):
    def __init__(self, parent):
        self.DRAW_MODE_COVERAGE = "coverage"
        self.DRAW_MODE_ITEMS = "item"
        self.draw_mode = self.DRAW_MODE_COVERAGE
        self.dislay_coverage_mode = False

        tk.Frame.__init__(self, parent, padx=5, pady=5)
        self.parent = parent
        self.grid(row=1, column=0, ipady=5, sticky="nsew")

    ##### MAP METHODS
    def start_map_design(self, ena_map=None):
        """
        initialize the map design components
        :param ena_map:
        :return:
        """
        self.grid_columnconfigure(3, weight=1)
        self.set_parameters()
        self.create_map_settings()
        self.create_map_canvas()
        self.create_map_legend()
        if ena_map:
            self.load_squares(ena_map)
            self.set_draw_mode(self.DRAW_MODE_ITEMS)

    def load_squares(self, ena_map):
        """
        Load map from file
        :param ena_map:
        :return:
        """
        for x in range(ena_map.squares_x):
            for y in range(ena_map.squares_y):
                sq = ena_map.squares[x][y]
                if sq.coverage:
                    self.set_square_coverage(x*self.square_size+1, y*self.square_size+1, sq.coverage)
                for feature in sq.features:
                    self.set_square_item(x*self.square_size+1, y*self.square_size+1, feature)
        self.update()


    def set_parameters(self):
        """
        Set all the parameters needed for the map designing
        :return:
        """
        self.dim_x = self.parent.dim_x
        self.dim_y = self.parent.dim_y

        self.legend_width = 200
        self.square_size = 20
        self.text_size = 6
        self.meter_per_square = 1

        self.update()
        not_enough_width = lambda: (self.winfo_width() - self.legend_width - self.square_size) < (self.dim_x * self.square_size) / self.meter_per_square
        not_enough_height = lambda: (self.winfo_height() - 50) < (self.dim_y * self.square_size) / self.meter_per_square
        while not_enough_width() or not_enough_height():
            self.meter_per_square *= 2

        self.squares_x = math.ceil(self.parent.dim_x / self.meter_per_square)
        self.squares_y = math.ceil(self.parent.dim_y / self.meter_per_square)

        self.selector_options = Selectors()

    def create_map_settings(self):
        """
        Generate the bar with drawing tools
        :return:
        """
        self.btn_toggle_draw_mode = tk.Button(self, text="item mode", command=self.click_toggle_draw_mode)
        self.btn_toggle_draw_mode.grid(row=0, column=0, sticky="nws", pady=10)

        self.lbl_instruct = tk.Label(self, text="Choose cursor: ")
        self.lbl_instruct.grid(row=0, column=1, sticky="nws", pady=10)

        self.coverage_options = self.selector_options.of_type(self.DRAW_MODE_COVERAGE)
        self.selector_coverage = tk.StringVar(self)
        self.selector_coverage.set(self.coverage_options[0].name)
        self.selector_menu_coverage = OptionMenu(self, self.selector_coverage, *self.coverage_options.names())
        self.selector_menu_coverage.set_max_width(*self.coverage_options.names())
        self.selector_menu_coverage.grid(row=0, column=2, sticky="nws", padx=10)
        self.selector_menu_coverage.grid_remove()

        self.btn_cover_all = tk.Button(self, text="Cover all", command=self.cover_all)
        self.btn_cover_all.grid(row=0, column=3, sticky="nws", pady=10, padx=10)
        self.btn_cover_all.grid_remove()

        self.item_options = self.selector_options.of_type(self.DRAW_MODE_ITEMS)
        self.selector_items = tk.StringVar(self)
        self.selector_items.set(self.item_options[0].name)
        self.selector_menu_items = OptionMenu(self, self.selector_items, *self.item_options.names(), command=self.selector_menu_items_selection_event)
        self.selector_menu_items.set_max_width(*self.item_options.names())
        self.selector_menu_items.grid(row=0, column=2, sticky="nws", padx=10)
        self.selector_menu_items.grid_remove()

        self.num_selector = tk.StringVar(self)
        self.num_selector.set(1)
        self.num_selector_menu = tk.OptionMenu(self, self.num_selector, *range(1,9))
        self.num_selector_menu.grid(row=0, column=3, sticky="nws", padx=10)
        self.num_selector_menu.grid_remove()

        self.btn_toggle_display_mode = tk.Button(self, text="show coverage check", command=self.do_coverage_check)
        self.btn_toggle_display_mode.grid(row=0, column=3, sticky="nes", pady=10)
        self.btn_toggle_display_mode.grid_remove()

    def click_toggle_draw_mode(self):
        if self.draw_mode == self.DRAW_MODE_COVERAGE:
            self.set_draw_mode(self.DRAW_MODE_ITEMS)
        else:
            self.set_draw_mode(self.DRAW_MODE_COVERAGE)

    def selector_menu_items_selection_event(self, event=None):
        if self.draw_mode == self.DRAW_MODE_ITEMS and self.selector_items.get() == "cable":
            self.num_selector_menu.grid()
        else:
            self.num_selector_menu.grid_remove()

    def set_draw_mode(self, mode):
        """
        Switch between coverage and item placing modes
        :param mode:
        :return:
        """
        self.draw_mode = mode

        if mode == self.DRAW_MODE_COVERAGE:
            tk.Misc.lift(self.canvas_coverage)  # activate coverage canvas

            self.selector_menu_items.grid_remove()
            self.btn_cover_all.grid()
            self.selector_menu_coverage.grid()
            self.btn_toggle_draw_mode['text'] = f"{self.DRAW_MODE_ITEMS} mode"
            self.selector_menu_items_selection_event()
            self.btn_toggle_display_mode.grid_remove()

        elif mode == self.DRAW_MODE_ITEMS:
            tk.Misc.lift(self.canvas_items)

            self.selector_menu_coverage.grid_remove()
            self.btn_cover_all.grid_remove()
            self.selector_menu_items.grid()
            self.btn_toggle_draw_mode['text'] = f"{self.DRAW_MODE_COVERAGE} mode"
            self.selector_menu_items_selection_event()
            self.btn_toggle_display_mode.grid()

            box = (self.canvas_coverage.winfo_rootx(),
                   self.canvas_coverage.winfo_rooty(),
                   self.canvas_coverage.winfo_rootx() + self.canvas_coverage.winfo_width(),
                   self.canvas_coverage.winfo_rooty() + self.canvas_coverage.winfo_height() )

            fp = BytesIO()
            ImageGrab.grab(bbox=box).save(fp, 'PNG')
            self.canvas_items.background = ImageTk.PhotoImage(Image.open(fp))
            bg_image = self.canvas_items.create_image(0, 0, image=self.canvas_items.background, anchor=tk.NW)
            self.canvas_items.tag_lower(bg_image)

        if hasattr(self, "canvas_legend"):
            tk.Misc.lift(self.canvas_legend)

    def create_map_canvas(self):
        """
        Generate the canvasses on which user can design the map
        :return:
        """
        with Trial(): self.canvas_coverage.destroy()  # remove canvas_coverage if it exists
        with Trial(): self.canvas_items.destroy()  # remove canvas_items if it exists

        self.canvas_coverage = tk.Canvas(self, height=self.square_size*self.dim_y + 1)
        self.canvas_coverage.grid(column=0, row=1, sticky="new", columnspan=5)

        for x in range(self.squares_x):
            for y in range(self.squares_y):
                self.canvas_coverage.create_rectangle(self.square_size * x + 1,
                                                      self.square_size * y + 1,
                                                      self.square_size * x + self.square_size + 1,
                                                      self.square_size * y + self.square_size + 1,
                                                      tags="square")

        self.canvas_items = tk.Canvas(self, height=self.square_size*self.dim_y + 1)
        self.canvas_items.grid(column=0, row=1, sticky="new", columnspan=5)

        for canv in [self.canvas_coverage, self.canvas_items]:
            canv.bind("<ButtonPress-1>", self.on_click)
            canv.bind("<B1-Motion>", self.on_move)
            canv.bind("<ButtonRelease-1>", self.on_release)

        self.set_draw_mode(self.DRAW_MODE_COVERAGE)

    def create_map_legend(self):
        """
        Generate the legend on the right side of the interface
        :return:
        """
        self.canvas_legend = tk.Canvas(self, width=self.legend_width, bg='white', bd=3, relief='ridge')
        self.canvas_legend.grid(column=4, row=1, sticky="ne")
        self.canvas_legend.create_text(10,10, text="Legend:", anchor=tk.NW, font=("Tahoma", 14))

        x_offset, y_offset, x_space, y_space = (10, 40, 30, 30)
        font = ("Tahoma", 11)
        for i, option in enumerate(self.selector_options):
            if option.type == self.selector_options.TYPE_COVERAGE:
                self.canvas_legend.create_rectangle(x_offset, y_space*i + y_offset, x_offset+self.square_size, y_space*i + y_offset+ self.square_size, fill=option.repr)
            elif option.type == self.selector_options.TYPE_ITEM:
                self.canvas_legend.create_text(x_offset, y_space*i + y_offset, text=f'{option.repr}:', anchor=tk.NW, font=font)
            self.canvas_legend.create_text(x_offset+x_space, y_space*i + y_offset, text=f'{option.name}', anchor=tk.NW, font=font)

        self.canvas_legend.create_rectangle(x_offset, y_space * len(self.selector_options) + y_offset, x_offset + self.square_size, y_space * len(self.selector_options) + y_offset + self.square_size)
        self.canvas_legend.create_line(x_offset, y_space * len(self.selector_options) + y_offset, x_offset+self.square_size, y_space * len(self.selector_options) + y_offset + self.square_size)
        self.canvas_legend.create_line(x_offset + self.square_size, y_space * len(self.selector_options) + y_offset, x_offset, y_space * len(self.selector_options) + y_offset + self.square_size)
        self.canvas_legend.create_text(x_offset+x_space, y_space*len(self.selector_options)+y_offset, text=f'Insufficient coverage', anchor=tk.NW, font=font)

        self.canvas_legend.create_text(x_offset, y_space*(len(self.selector_options)+1)+y_offset, text=f'Scale: 1:{self.meter_per_square} (sq:m)', anchor=tk.NW, font=font, fill="red" if self.meter_per_square > 1 else "black")

        self.canvas_legend.configure(height=y_space * 10 + y_offset)

    def on_click(self, event):
        self._dragging = True
        self.on_move(event)

    def on_move(self, event):
        """
        Action when clicked in canvas.
        :param event:
        :return:
        """
        if self.dislay_coverage_mode:
            return

        cursor_in_map = event.x < self.dim_x * self.square_size
        if cursor_in_map and self._dragging:
            if self.draw_mode == self.DRAW_MODE_COVERAGE:
                self.set_square_coverage(event.x, event.y, self.coverage_options.get_by_name(self.selector_coverage.get()).repr)
            elif self.draw_mode == self.DRAW_MODE_ITEMS:
                selector = self.item_options.get_by_name(self.selector_items.get())
                self.set_square_item(event.x, event.y, f'{selector.repr}{self.num_selector.get() if selector.repr=="C" else ""}')
                self._dragging = False

    def set_square_coverage(self, pos_x, pos_y, repr):
        """
        Apply coverage to a square
        :param pos_x:
        :param pos_y:
        :param repr:
        :return:
        """
        def sq_offset(c, ss=self.square_size):  # used to correct mismatching of closest element.
            return max(0, (c - ss // 2) if c % ss > ss // 2 else c)

        items = self.canvas_coverage.find_closest(sq_offset(pos_x), sq_offset(pos_y))
        if items:
            self.canvas_coverage.itemconfigure(items[0], fill=repr)

    def set_square_item(self, pos_x, pos_y, repr):
        """
        Apply item to a square
        :param pos_x:
        :param pos_y:
        :param repr:
        :return:
        """
        def get_text_xy(x, y, repr):
            ofset_x, ofset_y = {"U": [6, 7], "C": [11, 17], "A": [17, 7]}[repr[:1]]
            return [((x - 1) // self.square_size) * self.square_size + ofset_x, \
                   ((y - 1) // self.square_size) * self.square_size + ofset_y]

        items = self.canvas_items.find_closest(*get_text_xy(pos_x, pos_y, repr), halo=0)
        if items and self.canvas_items.type(items[0]) == "text" and [int(c) for c in self.canvas_items.coords(items[0])] == get_text_xy(pos_x, pos_y, repr):
            self.canvas_items.delete(items[0])
        else:
            self.canvas_items.create_text(*get_text_xy(pos_x, pos_y, repr),
                                          text=repr,
                                          font=("Tahoma", self.text_size),
                                          tags=repr[:1])

    def on_release(self, event):
        self._dragging = False

    def cover_all(self):
        """
        Apply current selector to entire map
        :return:
        """
        selector = self.coverage_options.get_by_name(self.selector_coverage.get())
        if tk.messagebox.askyesno("Cover all?", f"Would you like to apply {selector.name} to the entire map?"):
            for x in range(self.squares_x):
                for y in range(self.squares_y):
                    self.set_square_coverage(x*self.square_size+1, y*self.square_size+1, selector.repr)

    def do_coverage_check(self):
        """
        Check if all the required coverage is met. If met: show gear report, else activate display_coverage_mode
        :return:
        """
        if self.dislay_coverage_mode:
            check_lines = self.canvas_items.find_withtag("check_line")
            for check_line in check_lines:
                self.canvas_items.delete(check_line)
            self.dislay_coverage_mode = False
            self.btn_toggle_display_mode['text'] = "show coverage check"
            return

        ena_map = self.get_map_info()
        ena_map.check_squares()

        uncharted_squares_count = ena_map.count_uncharted_squares()
        if uncharted_squares_count > 0:
            Helper.message_box("warning", "Map not done", f'You still have {uncharted_squares_count} squares that have not been filled in yet.')
            return

        if len(ena_map.get_squares_with_uplinks()) == 0:
            Helper.message_box("warning", "Map not done", f'You have no uplinks in your map.')
            return

        uncovered_squares = ena_map.get_uncovered_squares()
        if not uncovered_squares:
            # Helper.message_box("info", "All squares covered", "All squares are sufficiently covered by the AP's")
            # Helper.message_box("info", "Gear Requirements", f'Needed gear:\n{ena_map.calculate_gear(format=True)}')
            self.show_gear_report(ena_map.calculate_gear(format=True))
            return

        for square in uncovered_squares:
            self.canvas_items.create_line((square.x / ena_map.meters_per_square) * self.square_size,
                                          (square.y / ena_map.meters_per_square) * self.square_size,
                                          (square.x / ena_map.meters_per_square) * self.square_size + self.square_size,
                                          (square.y / ena_map.meters_per_square) * self.square_size + self.square_size,
                                          tags="check_line")
            self.canvas_items.create_line((square.x / ena_map.meters_per_square) * self.square_size + self.square_size,
                                          (square.y / ena_map.meters_per_square) * self.square_size,
                                          (square.x / ena_map.meters_per_square) * self.square_size,
                                          (square.y / ena_map.meters_per_square) * self.square_size + self.square_size,
                                          tags="check_line")
        self.dislay_coverage_mode = True
        self.btn_toggle_display_mode['text'] = "close coverage check"

    def show_gear_report(self, gear_report):
        """
        Display a popup with the gear report
        :param gear_report:
        :return:
        """
        top = tk.Toplevel()
        top.title("Gear Requirements")

        msg = tk.Message(top, text=f'Gear Requirements Report:\n\n{gear_report}')
        msg.pack(expand=True, fill='both')

        # TODO make pdf export
        btn = tk.Button(top, text="Export to PDF", command=lambda: [top.destroy(), time.sleep(.1), self.create_pdf_report(gear_report)])
        btn.pack(side=tk.LEFT)

        btn2 = tk.Button(top, text="Dismiss", command=top.destroy)
        btn2.pack(side=tk.RIGHT)

    def get_map_info(self):
        """
        Parse the map
        :return: dict with all info in the map
        """
        ena_map = ENAMap(self.squares_x, self.squares_y, self.meter_per_square)

        for item_id in self.canvas_coverage.find_withtag("square"):
            ena_map.set_square_coverage(
                int(self.canvas_coverage.coords(item_id)[0] // self.square_size),
                int(self.canvas_coverage.coords(item_id)[1] // self.square_size),
                self.canvas_coverage.itemcget(item_id, "fill")
            )

        for option in self.item_options:
            for item_id in self.canvas_items.find_withtag(option.repr):
                x, y = [int(c // self.square_size) for c in self.canvas_items.coords(item_id)[:2]]
                ena_map.add_square_feature(x, y, self.canvas_items.itemcget(item_id, 'text'))

        return ena_map

    def create_pdf_report(self, gear_report):
        """
        Generate a pdf file with the required gear and map
        :param gear_report: String with the required gear
        :return:
        """
        box = (self.canvas_items.winfo_rootx(),
               self.canvas_items.winfo_rooty(),
               self.canvas_items.winfo_rootx() + self.squares_x * self.square_size + 2,
               self.canvas_items.winfo_rooty() + self.squares_y * self.square_size + 2)

        fp = BytesIO()
        ImageGrab.grab(bbox=box).save(fp, 'PNG')
        image_file = Image.open(fp)
        event_map = ImageReader(image_file)

        filename = tk.filedialog.asksaveasfilename(filetypes=[("Gear Requirement Report", ".pdf")],
                                                   defaultextension=".pdf")
        time.sleep(.1)
        if filename is () or filename is None or filename == '':
            return

        c = pdfcanvas.Canvas(filename)
        doc_width, doc_height = A4

        c.setFont('Helvetica-Bold', 16)
        c.drawString(30, doc_height - 30, "Gear Requirement Report")

        c.setFont('Helvetica', 12)
        text_object = c.beginText(30, doc_height - 30 - 16*2)
        for line in gear_report.split("\n"):
            text_object.textLine(line)
        c.drawText(text_object)

        image_width, image_height = image_file.size

        print(A4)
        max_width, max_height = doc_width - 60, int(text_object.getY()) - 40
        ratio = max(image_width / max_width, image_height / max_height, 1)
        c.drawImage(event_map, 30, 20 + (max_height - int(image_height / ratio)), width=int(image_width / ratio), height=int(image_height / ratio))
        c.save()

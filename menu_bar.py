import tkinter as tk
from tkinter import filedialog
import pickle
import time
from util import Helper


class MenuBar(tk.Menu):
    EXTENSION = ".ena"

    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        self.parent = parent
        self.make_filemenu()
        self.make_editmenu()
        self.make_helpmenu()

    def make_filemenu(self):
        self.filemenu = tk.Menu(self, tearoff=0)
        self.filemenu.add_command(label="New", command=self.file_new)
        self.filemenu.add_command(label="Open", command=self.file_open)
        self.filemenu.add_command(label="Save", command=self.file_save)
        self.filemenu.add_command(label="Save as...", command=self.file_save)
        self.filemenu.add_command(label="Close", command=self.file_close)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quit)
        self.add_cascade(label="File", menu=self.filemenu)

    def make_editmenu(self):
        self.editmenu = tk.Menu(self, tearoff=0)
        self.editmenu.add_command(label="Clear", command=self.edit_clear)
        self.editmenu.add_separator()
        # TODO Contemplate whether making undo functionality is worth the time and effort
        self.editmenu.add_command(label="Undo", command=self.do_nothing)
        self.editmenu.add_command(label="Cut", command=self.do_nothing)
        self.editmenu.add_command(label="Copy", command=self.do_nothing)
        self.editmenu.add_command(label="Paste", command=self.do_nothing)
        self.editmenu.add_command(label="Delete", command=self.do_nothing)
        self.editmenu.add_command(label="Select All", command=self.do_nothing)
        self.add_cascade(label="Edit", menu=self.editmenu)

    def make_helpmenu(self):
        self.helpmenu = tk.Menu(self, tearoff=0)
        self.helpmenu.add_command(label="Help Index", command=self.help_index)
        self.helpmenu.add_command(label="About...", command=self.help_about)
        self.add_cascade(label="Help", menu=self.helpmenu)

    def do_nothing(self):
        Helper.message_box("info", "Under Construction", "This functionality has not been implemented yet. Sorry.")

    #### File methods
    def file_new(self):
        if tk.messagebox.askyesno("New project", "Would you like to start a new assistant?"):
            self.parent.reinitialize()

    def file_open(self):
        if hasattr(self.parent.center_frame, "canvas_coverage"):
            if not tk.messagebox.askyesno("Load project", "This will clear your current map, are you sure?"):
                return

        filename = tk.filedialog.askopenfilename(filetypes=[("ENA Files", self.EXTENSION)])
        time.sleep(.1)
        if filename == ():
            return

        with open(filename, 'rb') as infile:
            dim_x, dim_y, ena_map = pickle.load(infile)

        self.parent.load(dim_x, dim_y, ena_map)

    def file_save(self):
        if not hasattr(self.parent.center_frame, "canvas_coverage"):
            Helper.message_box("info", "Unable to save", "You cannot save if you haven't made anything yet.")
            return

        filename = tk.filedialog.asksaveasfilename(filetypes=[("ENA Files", self.EXTENSION)], defaultextension=self.EXTENSION)
        time.sleep(.1)
        if filename is () or filename is None or filename == '':
            return

        ena_map = self.parent.center_frame.get_map_info()
        with open(filename, 'wb') as outfile:
            pickle.dump((self.parent.dim_x, self.parent.dim_y, ena_map), outfile)

    def file_close(self):
        self.file_new()

    #### Edit methods
    def edit_clear(self):
        if tk.messagebox.askyesno("New assistant", "Would you like to clear the map?"):
            self.parent.start()

    #### Help methods
    def help_index(self):
        # TODO
        self.do_nothing()

    def help_about(self):
        top = tk.Toplevel()
        top.title("About")

        msg = tk.Message(top, text=(
                    "Events Network Assistant v0.1\n\n"
                    "An application that helps plan the required hardware for network at an event\n\n"
                    "Authors:\n- Robin Vergouwen\n- Rick van Rheenen\n"
                )
            )
        msg.pack(expand=True, fill='both')

        btn = tk.Button(top, text="Dismiss", command=top.destroy)
        btn.pack()

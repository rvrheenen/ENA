import tkinter as tk


class MenuBar(tk.Menu):
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
        self.filemenu.add_command(label="Close", command=self.do_nothing)
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
        self.parent.message_box("info", "Under Construction", "This functionality has not been implemented yet. Sorry.")

    #### File methods
    def file_new(self):
        if tk.messagebox.askyesno("New assistant", "Would you like to start a new assistant?"):
            self.parent.reinitialize()

    def file_open(self):
        # TODO
        self.do_nothing()

    def file_save(self):
        # TODO
        self.do_nothing()

    def file_load(self):
        # TODO
        self.do_nothing()

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

from tkinter import *
from HomePanel import HomePanel
from LoginPanel import LoginPanel
from RegisterPanel import RegisterPanel


class Pilot(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.title("Home Pilot")
        self.configure(background='white')
        self.geometry("800x600")
        self.resizable(False, False)

        self.container = Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=5)
        self.container.grid_columnconfigure(0, weight=5)

        self.frames = {}

        for page in (HomePanel, LoginPanel, RegisterPanel):
            page_name = page.__name__
            frame = page(self.container, self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("HomePanel")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


p = Pilot()
p.mainloop()

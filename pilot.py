from tkinter import *
from HomePanel import HomePanel
from LoginPanel import LoginPanel
from RegisterPanel import RegisterPanel
from DevicesPanel import DevicesPanel
from RoomPanel import RoomPanel
import json

rooms = []
PILOT_CONFIG = []
with open("pilot_config.json") as conf:
    PILOT_CONFIG = json.load(conf)
    for x in PILOT_CONFIG:
        if 'name' in x:
            rooms.append(x['name'])


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
        # self.show_frame("HomePanel")
        self.display_devices_panel()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def display_devices_panel(self):
        frame = DevicesPanel(self.container, self, rooms)
        self.frames["DevicesPanel"] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def display_room_panel(self, name, index):
        frame = RoomPanel(self.container, self, name, PILOT_CONFIG, index)
        self.frames["RoomPanel"] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()


p = Pilot()
p.mainloop()

import tkinter as tk
from tkinter import *
from my_frames import Example, ExampleQR
from functools import partial
import json
from const import COLOR


class DevicesPanel(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=COLOR)
        left = Frame(self, width=400, relief="solid")
        left.propagate(0)
        right = Frame(self, width=400, relief="solid")
        right.propagate(0)
        left.configure(background=COLOR)
        container_right = Example(right)
        container_right.pack(side="left", expand=True, fill="both")
        container = Frame(left,  relief="solid")
        container.configure(background=COLOR)
        label1 = Label(
            container, text="WITAJ", font="helvetica 30")

        label1.configure(background=COLOR)
        label1.pack()
        label2 = Label(
            container, text="Wybierz z menu pokoj!", font="helvetica 15")

        label2.configure(background=COLOR)
        label2.pack()
        left.pack(side="left", expand=True, fill="both")
        right.pack(side="right", expand=True, fill="both")
        container.pack(expand=True, fill="both", padx=90, pady=15)
        menubar = Menu(self)
        rooms = []

        with open("pilot_config.json") as conf:
            PILOT_CONFIG = json.load(conf)
            for x in PILOT_CONFIG:
                if 'name' in x:
                    rooms.append(x['name'])
        for i, item in enumerate(rooms):
            menubar.add_command(label=item, command=partial(
                self.display_for_room, item, i))

        # display the menu
        self.controller.config(menu=menubar)

    def display_for_room(self, name, index):
        print(name)

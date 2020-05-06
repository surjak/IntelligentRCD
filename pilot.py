import threading
from tkinter import *
from HomePanel import HomePanel
from LoginPanel import LoginPanel
from RegisterPanel import RegisterPanel
from DevicesPanel import DevicesPanel
from RoomPanel import RoomPanel
import json
from mqtt_connect import subscriber

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
        self.show_frame("HomePanel")
        # self.display_devices_panel()

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


def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    mess = str(message.payload.decode("utf-8"))
    print("message topic ", message.topic)
    data = message.topic.split('/')

    for x in PILOT_CONFIG:

        if 'name' in x:
            if x['name'] == data[0]:
                if 'devices' in x:
                    for dev in x['devices']:
                        if dev['device'] == data[1]:
                            if 'options' in dev:
                                if 'mode' in dev['options']:
                                    if data[2] == 'mode':
                                        dev['options']['mode'] = mess
                                if 'power' in dev['options']:
                                    if data[2] == 'power':
                                        pass

                                if 'color' in dev['options']:
                                    if data[2] == "color":
                                        pass


x = threading.Thread(target=subscriber, args=(on_message,))
try:
    x.start()
except:
    print("Error in thread, starting thread again")
    x.start()


def on_closing():
    import os
    os.kill(os.getpid(), 9)


p = Pilot()
p.protocol("WM_DELETE_WINDOW", on_closing)
try:
    p.mainloop()
except:
    p.mainloop()

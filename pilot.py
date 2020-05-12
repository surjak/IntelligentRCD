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
    # nazwa obecnego pokoju
    room = None
    # obecne urządznie
    device = None
    # Obiekt obecnego pokoju
    ROOM = None

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
        """
        Pokazywanie innego ekranu
        """
        frame = self.frames[page_name]
        frame.tkraise()

    def display_devices_panel(self):
        """
        Wyświetlenie panelu urządzeń
        """
        frame = DevicesPanel(self.container, self, rooms)
        self.frames["DevicesPanel"] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def display_room_panel(self, name, index):
        """
        Wyświetlenie pomieszczenia
        """
        frame = RoomPanel(self.container, self, name,
                          PILOT_CONFIG, index, Pilot)
        self.frames["RoomPanel"] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
        Pilot.room = name
        Pilot.ROOM = frame

    @staticmethod
    def on_message(client, userdata, message):
        """
        Metoda wykonująca się gdy przyjdzie wiadomość od brokera MQTT
        """
        mess = str(message.payload.decode("utf-8"))
        print("SUBSCRIBER --> ", message.topic,
              str(message.payload.decode("utf-8")))
        print("\n")
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
                                            if Pilot.room == data[0] and Pilot.device == data[1]:
                                                # poinformowanie pokoju o tym że chcemy zmienić jego stan
                                                Pilot.ROOM.change(mess)


def on_closing():
    """
    Zakończenie aplikacji
    """
    import os
    os.kill(os.getpid(), 9)


p = Pilot()
# Wątek od nasłuchiwania na informacje od Brokera MQTT
x = threading.Thread(target=subscriber, args=(p.on_message,))
# Czasem wątek napotyka problem z wystartowaniem
try:
    x.start()
except:
    print("Error in thread, starting thread again")
    x.start()

p.protocol("WM_DELETE_WINDOW", on_closing)
try:
    p.mainloop()
except:
    p.mainloop()

import tkinter as tk
from tkinter import *
from my_frames import Example, ExampleQR
from functools import partial
import json
from const import COLOR
from publisher import Publisher
publisher = Publisher()


class RoomPanel(tk.Frame):
    def __init__(self, parent, controller, name, PILOT_CONFIG, index):
        self.index = index
        self.PILOT_CONFIG = PILOT_CONFIG
        self.btn_var = StringVar()
        self.name = name
        self.DEVICE = None
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
        self.container = Frame(left,  relief="solid")
        self.container.configure(background=COLOR)
        label1 = Label(
            self.container, text=name, font="helvetica 15")

        label1.configure(background=COLOR)
        label1.pack()

        left.pack(side="left", expand=True, fill="both")
        right.pack(side="right", expand=True, fill="both")
        self.container.pack(expand=True, fill="both", pady=10)
        if 'devices' in PILOT_CONFIG[index]:
            lbl = Label(self.container, text="Select device:",
                        font="helvetica 8")
            height = len(PILOT_CONFIG[index]['devices'])
            if height > 8:
                height = 8
            listbox = Listbox(self.container, width=56, height=height)
            listbox.bind('<Double-Button-1>', self.onselect)
            for i, d in enumerate(PILOT_CONFIG[index]['devices']):
                listbox.insert(i, d['device'])
            lbl.pack()
            listbox.pack()

    def onselect(self, evt):
        children = self.container.winfo_children()
        for i in range(3, len(children)):
            children[i].destroy()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)

        label1 = Label(
            self.container, text=value, font="helvetica 15")

        label1.configure(background=COLOR)
        label1.pack()
        self.DEVICE = value

        if 'mode' in self.PILOT_CONFIG[self.index]['devices'][index]['options']:
            opt = Label(
                self.container, text="Mode", font="helvetica 10")

            opt.configure(background=COLOR)
            opt.pack()
            text = self.PILOT_CONFIG[self.index]['devices'][index]['options']['mode']
            if text == "OFF":
                text = "ON"
            else:
                text = "OFF"
            self.btn_var.set(text)
            btn = Button(self.container, textvariable=self.btn_var,
                         command=partial(self.change_mode))

            btn.pack()
        if 'power' in self.PILOT_CONFIG[self.index]['devices'][index]['options']:
            opt = Label(
                self.container, text="Power", font="helvetica 10")

            opt.configure(background=COLOR)
            opt.pack()
            slider = Scale(self.container, from_=0, to=100,
                           tickinterval=10, orient=HORIZONTAL, length=300)
            slider.set(0)
            slider.bind("<ButtonRelease-1>", self.update_value)
            slider.pack()
        if 'color' in self.PILOT_CONFIG[self.index]['devices'][index]['options']:
            opt = Label(
                self.container, text="Color", font="helvetica 10")

            opt.configure(background=COLOR)
            opt.pack()
            height = len(self.PILOT_CONFIG[self.index]['devices']
                         [index]['options']['color'])
            if height > 8:
                height = 8
            listbox = Listbox(self.container, width=56, height=height)
            listbox.bind('<Double-Button-1>', self.on_color_change)
            for i, d in enumerate(self.PILOT_CONFIG[self.index]['devices'][index]['options']['color']):
                listbox.insert(i, d)
            listbox.pack()

    def change_mode(self):
        publisher.publish(
            f'{self.name}/{self.DEVICE}/mode', self.btn_var.get())

    def update_value(self, evt):
        w = evt.widget
        publisher.publish(f'{self.name}/{self.DEVICE}/power', w.get())

    def on_color_change(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        publisher.publish(f'{self.name}/{self.DEVICE}/color', value)

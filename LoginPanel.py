import tkinter as tk
from tkinter import *
from my_frames import Example, ExampleQR
from functools import partial
import json
from pymongo import MongoClient
import bcrypt
import pyotp
from const import COLOR

DB_PASSWORD = ''

with open("private.json") as private_config:
    private = json.loads(private_config.read())
    DB_PASSWORD = private['password']

client = MongoClient(
    f"mongodb+srv://test:{DB_PASSWORD}@cluster0-pncd0.mongodb.net/test?retryWrites=true&w=majority")

db = client.get_database('pilot')


class LoginPanel(tk.Frame):
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
        self.container = Frame(left,  relief="solid")
        self.container.configure(background=COLOR)
        label1 = Label(
            self.container, text="Login", font="helvetica 30")
        label1.configure(background=COLOR)
        label1.pack()

        label_email = Label(self.container, text="Email:",
                            font="helvetica 12", pady=15)
        entry_email = Entry(self.container, borderwidth=8, relief=FLAT)
        label_email.configure(background=COLOR)
        label_email.pack()
        entry_email.pack()
        label_password = Label(self.container, text="Password:",
                               font="helvetica 12", pady=15)
        entry_password = Entry(
            self.container, borderwidth=8, relief=FLAT, show="*")
        label_password.configure(background=COLOR)
        label_password.pack()
        entry_password.pack()

        login_button = Button(self.container, text='Login',
                              command=partial(self.login_handler, entry_email, entry_password), font="helvetica 12", padx=20, pady=5)
        login_button.pack(pady=15)

        left.pack(side="left", expand=True, fill="both")
        right.pack(side="right", expand=True, fill="both")
        self.container.pack(expand=True, fill="both", padx=90, pady=15)
        register_button = Button(left, text='Menu',
                                 command=self.navigate_to_menu, font="helvetica 12", padx=20, pady=5)
        register_button.pack(pady=15)

    def navigate_to_menu(self):
        self.controller.show_frame("HomePanel")

    def login_handler(self, entry_email, entry_password):
        email = entry_email.get()
        password = entry_password.get()
        users = db.users
        user = users.find_one({"email": email})
        if not user:
            print("User doesn't exist, register!")
            return
        if bcrypt.checkpw(password.encode("utf-8"), user['password']):
            label_key = Label(self.container, text="KEY:",
                              font="helvetica 12", pady=10)
            label_key.configure(background=COLOR)
            label_key.pack()
            entry_key = Entry(self.container, borderwidth=8, relief=FLAT)
            entry_key.pack()
            btn_key = Button(self.container, text='Submit',
                             command=partial(self.confirm, entry_key, user['TOTP']), font="helvetica 12", padx=20, pady=5)
            btn_key.pack(pady=15)
        else:
            print("Password is incorrent!")
            return

    def confirm(self, entry_key, totpp):
        print(entry_key.get(), totpp)
        totp = pyotp.TOTP(totpp)
        if entry_key.get() == totp.now():
            LOGIN = True
            print("You are in!")
            self.controller.display_devices_panel()
        else:
            print("Invalid key")

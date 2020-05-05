import tkinter as tk
from tkinter import *
from my_frames import Example, ExampleQR
from functools import partial
import json
from pymongo import MongoClient
import bcrypt
import pyotp
from const import COLOR
import qrcode
from bson.binary import Binary

DB_PASSWORD = ''

with open("private.json") as private_config:
    private = json.loads(private_config.read())
    DB_PASSWORD = private['password']

client = MongoClient(
    f"mongodb+srv://test:{DB_PASSWORD}@cluster0-pncd0.mongodb.net/test?retryWrites=true&w=majority")

db = client.get_database('pilot')


class RegisterPanel(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=COLOR)
        self.left = Frame(self, relief="solid")

        self.right = Frame(self,  relief="solid")

        self.left.configure(background=COLOR)
        self.container_right = Example(self.right)
        self.container_right.pack(side="left", expand=True, fill="both")
        self.container = Frame(self.left,  relief="solid")
        self.container.configure(background=COLOR)
        label1 = Label(
            self.container, text="Register", font="helvetica 30")
        label1.configure(background=COLOR)
        label1.pack()
        ####
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
        label_password_confirm = Label(self.container, text="Confirm Password:",
                                       font="helvetica 12", pady=15)
        entry_password_confirm = Entry(
            self.container, borderwidth=8, relief=FLAT, show="*")
        label_password_confirm.configure(background=COLOR)
        label_password_confirm.pack()
        entry_password_confirm.pack()

        btn1 = Button(self.container, text='Register',
                      command=partial(self.click, entry_email, entry_password, entry_password_confirm), font="helvetica 12", padx=20, pady=5)
        btn1.pack(pady=15)

        ####
        self.left.pack(side="left", expand=True, fill="both")
        self.right.pack(side="right", expand=True, fill="both")
        self.container.pack(expand=True, fill="both", padx=90, pady=15)
        login_button = Button(self.left, text='Menu',
                              command=self.navigate_to_menu, font="helvetica 12", padx=20, pady=5)
        login_button.pack(pady=15)

    def navigate_to_menu(self):
        self.controller.show_frame("HomePanel")

    def click(self, entry_email, entry_password, entry_password_confirm):

        email = entry_email.get()
        password = entry_password.get()
        password2 = entry_password_confirm.get()
        if len(email) < 7 or len(password) < 5:
            print("length pass / email")
            return
            # todo
        print(password)
        if password == password2:
            users = db.users
            existing_user = users.find_one({"email": email})
            if existing_user:
                print("already exists")
                return
                # todo
            totp = pyotp.random_base32()
            a = pyotp.totp.TOTP(totp).provisioning_uri(
                email, issuer_name="HOME_PILOT")
            qr = qrcode.make(a)
            qr.save('qr.png')
            TOTP = totp
            data = open('qr.png', 'rb').read()
            hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            user = {"email": email,
                    "password": hashed,
                    "TOTP": totp,
                    "img": Binary(data)}
            users.insert_one(user)
            # self.right.pack_forget()
            self.container_right.pack_forget()
            self.container_right = ExampleQR(self.right)
            self.container_right.pack(side="left", expand=True, fill="both")
            # self.right.pack()

            label_key = Label(self.container, text="KEY:",
                              font="helvetica 12", pady=10)
            label_key.configure(background=COLOR)
            label_key.pack()
            entry_key = Entry(self.container, borderwidth=8, relief=FLAT)
            entry_key.pack()
            btn_key = Button(self.container, text='Submit',
                             command=partial(self.confirm, entry_key, TOTP), font="helvetica 12", padx=20, pady=5)
            btn_key.pack(pady=15)
        else:
            return

    def confirm(self, entry_key, totpp):
        print(entry_key.get(), totpp)
        totp = pyotp.TOTP(totpp)
        if entry_key.get() == totp.now():
            LOGIN = True
            print("LOGIN!")
            self.controller.display_devices_panel()

from bson.binary import Binary
from functools import partial
from tkinter import *
import json
import pyotp
import time
import qrcode
from pymongo import MongoClient
import bcrypt
from PIL import Image, ImageTk
from my_frames import Example, ExampleQR
COLOR = "#e1e8e8"

client = MongoClient('localhost', 27017)
db = client.get_database('pilot')


root = Tk()
root.title("Home Polit")
root.configure(background='white')
root.geometry("800x600")


def confirm(entry_key, totpp, right, left):
    print(entry_key.get(), totpp)
    totp = pyotp.TOTP(totpp)
    if entry_key.get() == totp.now():
        print("LOGIN!")
        right.pack_forget()
        left.pack_forget()
        pass
        # todo


def click(entry_email, entry_password, entry_password_confirm, right, container_right, container, left):

    email = entry_email.get()
    password = entry_password.get()
    password2 = entry_password_confirm.get()
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
        right.pack_forget()
        container_right.pack_forget()
        container_right = ExampleQR(right)
        container_right.pack(side="left", expand=True, fill="both")
        right.pack()
        label_key = Label(container, text="KEY:",
                          font="helvetica 12", pady=10)
        label_key.configure(background=COLOR)
        label_key.pack()
        entry_key = Entry(container, borderwidth=8, relief=FLAT)
        entry_key.pack()
        btn_key = Button(container, text='Submit',
                         command=partial(confirm, entry_key, TOTP, right, left), font="helvetica 12", padx=20, pady=5)
        btn_key.pack(pady=15)
    else:
        return
        # todo


def register(root):

    left = Frame(root, relief="solid")

    right = Frame(root, relief="solid")
    left.configure(background=COLOR)
    container_right = Example(right)
    container_right.pack(side="left", expand=True, fill="both")
    container = Frame(left,  relief="solid")
    container.configure(background=COLOR)
    label1 = Label(
        container, text="Register", font="helvetica 30")
    label1.configure(background=COLOR)
    label1.pack()
    ####
    label_email = Label(container, text="Email:",
                        font="helvetica 12", pady=15)
    entry_email = Entry(container, borderwidth=8, relief=FLAT)
    label_email.configure(background=COLOR)
    label_email.pack()
    entry_email.pack()
    label_password = Label(container, text="Password:",
                           font="helvetica 12", pady=15)
    entry_password = Entry(container, borderwidth=8, relief=FLAT, show="*")
    label_password.configure(background=COLOR)
    label_password.pack()
    entry_password.pack()
    label_password_confirm = Label(container, text="Confirm Password:",
                                   font="helvetica 12", pady=15)
    entry_password_confirm = Entry(
        container, borderwidth=8, relief=FLAT, show="*")
    label_password_confirm.configure(background=COLOR)
    label_password_confirm.pack()
    entry_password_confirm.pack()

    btn1 = Button(container, text='Register',
                  command=partial(click, entry_email, entry_password, entry_password_confirm, right, container_right, container, left), font="helvetica 12", padx=20, pady=5)
    btn1.pack(pady=15)

    ####
    left.pack(side="left", expand=True, fill="both")
    right.pack(side="right", expand=True, fill="both")
    container.pack(expand=True, fill="both", padx=90, pady=15)


register(root)
root.mainloop()

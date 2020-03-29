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
DB_PASSWORD = ''

with open("private.json") as private_config:
    private = json.loads(private_config.read())
    DB_PASSWORD = private['password']

client = MongoClient(
    f"mongodb+srv://test:{DB_PASSWORD}@cluster0-pncd0.mongodb.net/test?retryWrites=true&w=majority")

db = client.get_database('pilot')
rooms = []
with open("pilot_config.json") as conf:
    a = json.load(conf)
    for x in a:
        if 'name' in x:
            rooms.append(x['name'])


root = Tk()
root.title("Home Polit")
root.configure(background='white')
root.geometry("800x600")


left = None
right = None
LOGIN = False


def display_for_room(root, name):
    print(name)
    pass


def devices_screen(root):
    global left, right
    if left:
        left.pack_forget()
    if right:
        right.pack_forget()
    left = Frame(root, relief="solid")

    right = Frame(root, relief="solid")
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
    menubar = Menu(root)
    for item in rooms:
        menubar.add_command(label=item, command=partial(
            display_for_room, root, item))

    # display the menu
    root.config(menu=menubar)


def confirm(entry_key, totpp, right, left):
    print(entry_key.get(), totpp)
    totp = pyotp.TOTP(totpp)
    # uncomment
    LOGIN = True
    devices_screen(root)
    # if entry_key.get() == totp.now():
    #     LOGIN = True
    #     print("LOGIN!")
    #     devices_screen(root)
    #     pass
    # todo


def click(entry_email, entry_password, entry_password_confirm, right, container_right, container, left):

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
    global left, right
    if left:
        left.pack_forget()
    if right:
        right.pack_forget()
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


def login_handler(entry_email, entry_password, right, container_right, container, left):
    email = entry_email.get()
    password = entry_password.get()
    users = db.users
    user = users.find_one({"email": email})
    if not user:
        print("nie ma takiego usera")
        return
        pass
    if bcrypt.checkpw(password.encode("utf-8"), user['password']):
        print("git")
        label_key = Label(container, text="KEY:",
                          font="helvetica 12", pady=10)
        label_key.configure(background=COLOR)
        label_key.pack()
        entry_key = Entry(container, borderwidth=8, relief=FLAT)
        entry_key.pack()
        btn_key = Button(container, text='Submit',
                         command=partial(confirm, entry_key, user['TOTP'], right, left), font="helvetica 12", padx=20, pady=5)
        btn_key.pack(pady=15)
    else:
        print("NIE")
        return
    # todo


def login(root):
    global left, right
    if left:
        left.pack_forget()
    if right:
        right.pack_forget()
    left = Frame(root, relief="solid")

    right = Frame(root, relief="solid")
    left.configure(background=COLOR)
    container_right = Example(right)
    container_right.pack(side="left", expand=True, fill="both")
    container = Frame(left,  relief="solid")
    container.configure(background=COLOR)
    label1 = Label(
        container, text="Login", font="helvetica 30")
    label1.configure(background=COLOR)
    label1.pack()


#
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

    login_button = Button(container, text='Login',
                          command=partial(login_handler, entry_email, entry_password, right, container_right, container, left), font="helvetica 12", padx=20, pady=5)
    login_button.pack(pady=15)
#

    left.pack(side="left", expand=True, fill="both")
    right.pack(side="right", expand=True, fill="both")
    container.pack(expand=True, fill="both", padx=90, pady=15)


def welcome(root):
    global left, right
    if left:
        left.pack_forget()
    if right:
        right.pack_forget()
    left = Frame(root, relief="solid")

    right = Frame(root, relief="solid")
    left.configure(background=COLOR)
    container_right = Example(right)
    container_right.pack(side="left", expand=True, fill="both")
    container = Frame(left,  relief="solid")
    container.configure(background=COLOR)
    label1 = Label(
        container, text="Login", font="helvetica 30")
    label1.configure(background=COLOR)
    label1.pack()
    login_button = Button(container, text='Login',
                          command=partial(login, root), font="helvetica 12", padx=20, pady=5)
    login_button.pack(pady=15)

    label_register = Label(
        container, text="Register", font="helvetica 30")
    label_register.configure(background=COLOR)
    label_register.pack()
    register_button = Button(container, text='Register',
                             command=partial(register, root), font="helvetica 12", padx=20, pady=5)
    register_button.pack(pady=15)

    left.pack(side="left", expand=True, fill="both")
    right.pack(side="right", expand=True, fill="both")
    container.pack(expand=True, fill="both", padx=90, pady=15)


# create a toplevel menu
# menubar = Menu(root)
# menubar.add_command(label="Menu", command=partial(welcome, root))
# menubar.add_command(label="Quit!", command=root.quit)

# # display the menu
# root.config(menu=menubar)

# login(root)
# register(root)
welcome(root)
root.mainloop()

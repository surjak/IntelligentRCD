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
import paho.mqtt.client as mqtt
import threading
import sys
from mqtt_connect import subscriber
from publisher import Publisher
# COLOR = "#e1e8e8"
COLOR = "#f0f0f0"
DB_PASSWORD = ''

publisher = Publisher()

with open("private.json") as private_config:
    private = json.loads(private_config.read())
    DB_PASSWORD = private['password']

client = MongoClient(
    f"mongodb+srv://test:{DB_PASSWORD}@cluster0-pncd0.mongodb.net/test?retryWrites=true&w=majority")
PILOT_CONFIG = []
db = client.get_database('pilot')
rooms = []
with open("pilot_config.json") as conf:
    PILOT_CONFIG = json.load(conf)
    for x in PILOT_CONFIG:
        if 'name' in x:
            rooms.append(x['name'])


root = Tk()
root.title("Home Polit")
root.configure(background='white')
root.geometry("800x600")
root.resizable(False, False)


left = None
right = None
LOGIN = False

CONTAINER = None
INDEX = None

ROOM = None
DEVICE = None

btn_var = StringVar()


def on_color_change(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    print(f'{ROOM}/{DEVICE}/color             {value}')
    publisher.publish(f'{ROOM}/{DEVICE}/color', value)


def update_value(evt):
    w = evt.widget
    print(f'{ROOM}/{DEVICE}/power             {w.get()}')
    publisher.publish(f'{ROOM}/{DEVICE}/power', w.get())


def change_mode():

    publisher.publish(f'{ROOM}/{DEVICE}/mode', btn_var.get())

    pass


def onselect(evt):
    global DEVICE
    children = CONTAINER.winfo_children()
    for i in range(3, len(children)):
        children[i].destroy()
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)

    label1 = Label(
        CONTAINER, text=value, font="helvetica 15")

    label1.configure(background=COLOR)
    label1.pack()
    DEVICE = value

    if 'mode' in PILOT_CONFIG[INDEX]['devices'][index]['options']:
        opt = Label(
            CONTAINER, text="Mode", font="helvetica 10")

        opt.configure(background=COLOR)
        opt.pack()
        text = PILOT_CONFIG[INDEX]['devices'][index]['options']['mode']
        if text == "OFF":
            text = "ON"
        else:
            text = "OFF"
        btn_var.set(text)
        btn = Button(CONTAINER, textvariable=btn_var,
                     command=partial(change_mode))

        btn.pack()
    if 'power' in PILOT_CONFIG[INDEX]['devices'][index]['options']:
        opt = Label(
            CONTAINER, text="Power", font="helvetica 10")

        opt.configure(background=COLOR)
        opt.pack()
        slider = Scale(CONTAINER, from_=0, to=100,
                       tickinterval=10, orient=HORIZONTAL, length=300)
        slider.set(0)
        slider.bind("<ButtonRelease-1>", update_value)
        slider.pack()
    if 'color' in PILOT_CONFIG[INDEX]['devices'][index]['options']:
        opt = Label(
            CONTAINER, text="Color", font="helvetica 10")

        opt.configure(background=COLOR)
        opt.pack()
        height = len(PILOT_CONFIG[INDEX]['devices'][index]['options']['color'])
        if height > 8:
            height = 8
        listbox = Listbox(CONTAINER, width=56, height=height)
        listbox.bind('<Double-Button-1>', on_color_change)
        for i, d in enumerate(PILOT_CONFIG[INDEX]['devices'][index]['options']['color']):
            listbox.insert(i, d)
        listbox.pack()


def display_for_room(root, name, index):
    global left, right, CONTAINER, INDEX, ROOM
    if left:
        left.pack_forget()
    if right:
        right.pack_forget()
    left = Frame(root, width=400, relief="solid")
    left.propagate(0)
    right = Frame(root, width=400, relief="solid")
    right.propagate(0)
    left.configure(background=COLOR)
    container_right = Example(right)
    container_right.pack(side="left", expand=True, fill="both")
    container = Frame(left,  relief="solid")
    container.configure(background=COLOR)
    label1 = Label(
        container, text=name, font="helvetica 15")

    label1.configure(background=COLOR)
    label1.pack()

    left.pack(side="left", expand=True, fill="both")
    right.pack(side="right", expand=True, fill="both")
    container.pack(expand=True, fill="both", pady=10)
    if 'devices' in PILOT_CONFIG[index]:
        lbl = Label(container, text="Select device:", font="helvetica 8")
        height = len(PILOT_CONFIG[index]['devices'])
        if height > 8:
            height = 8
        listbox = Listbox(container, width=56, height=height)
        listbox.bind('<Double-Button-1>', onselect)
        for i, d in enumerate(PILOT_CONFIG[index]['devices']):
            listbox.insert(i, d['device'])
        lbl.pack()
        listbox.pack()

    CONTAINER = container
    INDEX = index
    ROOM = name

    pass


def devices_screen(root):
    global left, right
    if left:
        left.pack_forget()
    if right:
        right.pack_forget()
    left = Frame(root, width=400, relief="solid")
    left.propagate(0)
    right = Frame(root, width=400, relief="solid")
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
    menubar = Menu(root)
    for i, item in enumerate(rooms):
        menubar.add_command(label=item, command=partial(
            display_for_room, root, item, i))

    # display the menu
    root.config(menu=menubar)


def confirm(entry_key, totpp, right, left):
    print(entry_key.get(), totpp)
    totp = pyotp.TOTP(totpp)
    # uncomment
    # LOGIN = True
    # devices_screen(root)
    if entry_key.get() == totp.now():
        LOGIN = True
        print("LOGIN!")
        devices_screen(root)
        pass
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

    right = Frame(root,  relief="solid")

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
    login_button = Button(left, text='Login',
                          command=partial(login, root), font="helvetica 12", padx=20, pady=5)
    login_button.pack(pady=15)


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
    left = Frame(root, width=400, relief="solid")
    left.propagate(0)
    right = Frame(root, width=400, relief="solid")
    right.propagate(0)
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
    register_button = Button(left, text='Register',
                             command=partial(register, root), font="helvetica 12", padx=20, pady=5)
    register_button.pack(pady=15)


def welcome(root):
    global left, right
    if left:
        left.pack_forget()
    if right:
        right.pack_forget()
    left = Frame(root, width=400, relief="solid")
    left.propagate(0)
    right = Frame(root, width=400, relief="solid")
    right.propagate(0)
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


def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    mess = str(message.payload.decode("utf-8"))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)
    data = message.topic.split('/')
    print(data)

    for x in PILOT_CONFIG:

        if 'name' in x:
            if x['name'] == data[0]:
                if 'devices' in x:
                    for dev in x['devices']:
                        if dev['device'] == data[1]:
                            if 'options' in dev:
                                if 'mode' in dev['options']:
                                    if data[2] == 'mode':
                                        print("JESTEM")
                                        dev['options']['mode'] = mess
                                        if data[0] == ROOM:
                                            if mess == "OFF":
                                                btn_var.set("ON")
                                            else:
                                                btn_var.set("OFF")

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

welcome(root)
root.mainloop()

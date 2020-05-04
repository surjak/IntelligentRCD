import tkinter as tk
from PIL import ImageTk, Image
from tkinter import Frame, Label
from my_frames import Example, ExampleQR
from functools import partial
from const import COLOR


class HomePanel(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=COLOR)
        self.left = Frame(self, width=400, relief="solid")
        self.left.propagate(0)
        self.right = Frame(self, width=400, relief="solid")
        self.right.propagate(0)
        self.left.configure(background=COLOR)
        container_right = Example(self.right)
        container_right.pack(side="left", expand=True, fill="both")
        container = Frame(self.left,  relief="solid")
        container.configure(background=COLOR)
        label1 = Label(
            container, text="Login", font="helvetica 30")
        label1.configure(background=COLOR)
        label1.pack()

        login_button = tk.Button(container, text='Login',
                                 command=partial(self.login, self), font="helvetica 12", padx=20, pady=5)
        login_button.pack(pady=15)

        label_register = Label(
            container, text="Register", font="helvetica 30")
        label_register.configure(background=COLOR)
        label_register.pack()
        register_button = tk.Button(container, text='Register',
                                    command=partial(self.register, self), font="helvetica 12", padx=20, pady=5)
        register_button.pack(pady=15)

        self.left.pack(side="left", expand=True, fill="both")
        self.right.pack(side="right", expand=True, fill="both")
        container.pack(expand=True, fill="both", padx=90, pady=15)

    def login(self, root):
        self.controller.show_frame("LoginPanel")

    def register(self, root):
        print("login")

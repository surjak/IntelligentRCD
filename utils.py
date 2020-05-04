import os


def on_closing():
    os.kill(os.getpid(), 9)

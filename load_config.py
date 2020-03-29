import tkinter as tk
import json
rooms = []
with open("pilot_config.json") as conf:
    a = json.load(conf)
    for x in a:
        if 'name' in x:
            rooms.append(x['name'])
print(rooms)


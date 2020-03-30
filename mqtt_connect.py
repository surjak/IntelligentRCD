import paho.mqtt.client as mqtt
import time
import threading
import sys
import json


def subscriber(func):
    routes = []

    with open("pilot_config.json") as conf:
        a = json.load(conf)
        for x in a:
            if 'name' in x:
                if 'devices' in x:
                    for dev in x['devices']:
                        if 'options' in dev:
                            if 'mode' in dev['options']:
                                routes.append(
                                    f"{x['name']}/{dev['device']}/mode")
                            if 'power' in dev['options']:
                                routes.append(
                                    f"{x['name']}/{dev['device']}/power")
                            if 'color' in dev['options']:
                                routes.append(
                                    f"{x['name']}/{dev['device']}/color")
    print("creating new instance")
    client = mqtt.Client("P1", clean_session=False)
    client.on_message = func
    print("connecting to broker")
    client.connect("localhost", 1883, 300)
    try:
        client.loop_start()
    except:
        sys.exit()

    print("Subscribing to routes")
    for route in routes:
        print(route)
        client.subscribe(route)

    try:
        client.loop_forever()
    except:
        print("Error in thread, starting subscriber again")
        subscriber(func)
        # sys.exit()

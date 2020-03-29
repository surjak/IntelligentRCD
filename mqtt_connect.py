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
    client.loop_start()
    print("Subscribing to routes")
    for route in routes:
        print(route)
        client.subscribe(route)

    try:
        client.loop_forever()
    except Exception:
        client.loop_forever()


# def publisher():
#     print("Publishing message to topic", "house/bulbs/bulb1")
#     client = mqtt.Client("P2")
#     client.connect("localhost", 1883, 60)
#     client.publish("house/bulbs/bulb1", "OFF")
#     client.publish("house/bulbs/bulb2", "On")

    # time.sleep(4)  # wait
    # client.loop_stop()  # stop the loop


# x = threading.Thread(target=subscriber)

# # y = threading.Thread(target=publisher)
# try:
#     x.start()
# except Exception:  # Wiem wiem... ale to sa narazie testy XD
#     x.start()
# time.sleep(2)
# y.start()
# time.sleep(2)
# sys.exit()

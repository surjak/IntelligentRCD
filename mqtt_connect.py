import paho.mqtt.client as mqtt
import time
import threading
import sys


# def on_message(client, userdata, message):
#     print("message received ", str(message.payload.decode("utf-8")))
#     print("message topic=", message.topic)
#     print("message qos=", message.qos)
#     print("message retain flag=", message.retain)


def subscriber(func):
    print("creating new instance")
    client = mqtt.Client("P1", clean_session=False)  # create new instance
    client.on_message = func  # attach function to callback
    print("connecting to broker")
    client.connect("localhost", 1883, 300)
    client.loop_start()  # start the loop
    print("Subscribing to topic", "house/bulbs/bulb1")
    client.subscribe("house/bulbs/bulb1")
    client.subscribe("house/bulbs/bulb2")
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

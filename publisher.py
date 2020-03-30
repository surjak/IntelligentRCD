import paho.mqtt.client as mqtt


class Publisher:
    def __init__(self):
        print("Connecting to MQQT Server")
        self.client = mqtt.Client("P2")
        self.client.connect("localhost", 1883, 60)

    def publish(self, route, value):
        print("PUBLISHER", route, value)
        self.client.publish(route, value)

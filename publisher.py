import paho.mqtt.client as mqtt


class Publisher:
    """
        Publikowanie zdarzeń do brokera
    """

    def __init__(self):
        self.client = mqtt.Client("P2")
        self.client.connect("localhost", 1883, 60)

    def publish(self, route, value):
        print("PUBLISHER", route, value)
        result = self.client.publish(route, value)
        if result[1] > 10:
            self = Publisher()
            self.client.publish(route, value)

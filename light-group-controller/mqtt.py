import ubinascii
import machine
from umqtt.simple import MQTTClient

led = machine.Pin("LED", machine.Pin.OUT)
led.off()  # Start with LED off

CLIENT_ID = b"pico-client-" + ubinascii.hexlify(machine.unique_id())

class MqttLightSync:
    def __init__(self, broker, username, password, state_topic, on_update):
        self.broker = broker
        self.username = username
        self.password = password
        self.state_topic = state_topic.encode()
        self.on_update = on_update
        self.client = None
        self.ignore_next = False

    def _callback(self, topic, msg):
        print("MQTT Received:", topic, msg)
        if self.ignore_next:
            self.ignore_next = False
            return

        try:
            import ujson
            data = ujson.loads(msg)
            state = data.get("state", "OFF")
            color_temp = int(data.get("color_temp", 370))
            self.on_update(state == "ON", color_temp)
        except Exception as e:
            print("MQTT parse error:", e)

    def connect(self):
        print(f"Connecting to MQTT @ {self.broker} as {CLIENT_ID.decode()}")
        try:
            temp_client = MQTTClient(
                client_id=CLIENT_ID,
                server=self.broker,
                user=self.username,
                password=self.password,
                keepalive=60
            )
            temp_client.set_callback(self._callback)
            temp_client.connect()
            temp_client.subscribe(self.state_topic)
            self.client = temp_client
            print("Connected to MQTT and subscribed to", self.state_topic.decode())
            led.on()
        except Exception as e:
            import sys
            print("MQTT connection failed:")
            sys.print_exception(e)

    def check(self):
        if self.client:
            self.client.check_msg()

    def publish_state(self, state, color_temp):
        import ujson
        payload = ujson.dumps({
            "state": "ON" if state else "OFF",
            "color_temp": color_temp
        })
        self.ignore_next = True
        self.client.publish(b"home/living_room_lamps/set", payload)
        print("Published →", payload)

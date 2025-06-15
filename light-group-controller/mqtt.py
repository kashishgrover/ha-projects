import ubinascii
import machine
from umqtt.simple import MQTTClient
import ujson
import config
from led_controller import LedController

# Generate unique client ID based on device ID
CLIENT_ID = b"pico-client-" + ubinascii.hexlify(machine.unique_id())

class MqttLightSync:
    def __init__(self, broker, username, password, state_topic, on_update):
        """
        Initialize MQTT client for light synchronization.
        
        Args:
            broker: MQTT broker address
            username: MQTT username
            password: MQTT password
            state_topic: Topic to subscribe for light state updates
            on_update: Callback for state updates (receives state(bool), color_temp(int))
        """
        self.broker = broker
        self.username = username
        self.password = password
        self.state_topic = state_topic.encode()
        self.command_topic = config.MQTT_TOPIC_SET.encode()
        self.scene_command_topic = config.MQTT_TOPIC_SCENE_SET.encode()
        self.on_update = on_update
        self.client = None
        self.ignore_next = False
        self.led = LedController()  # Initialize LED controller
        self.led.off()  # Start with LED off

    def _callback(self, topic, msg):
        """Process incoming MQTT messages."""
        print("MQTT Received:", topic, msg)
        if self.ignore_next:
            self.ignore_next = False
            return

        try:
            data = ujson.loads(msg)
            state = data.get("state", "OFF")
            color_temp = int(data.get("color_temp", config.DEFAULT_COLOR_TEMP))
            self.on_update(state == "ON", color_temp)
        except Exception as e:
            print("MQTT parse error:", e)

    def connect(self):
        """Connect to MQTT broker and subscribe to state topic."""
        print(f"Connecting to MQTT @ {self.broker} as {CLIENT_ID.decode()}")
        try:
            temp_client = MQTTClient(
                client_id=CLIENT_ID,
                server=self.broker,
                user=self.username,
                password=self.password,
                keepalive=config.MQTT_KEEPALIVE
            )
            temp_client.set_callback(self._callback)
            temp_client.connect()
            temp_client.subscribe(self.state_topic)
            self.client = temp_client
            print("Connected to MQTT and subscribed to", self.state_topic.decode())
            self.led.on()  # Turn on LED to indicate successful connection
        except Exception as e:
            import sys
            print("MQTT connection failed:")
            sys.print_exception(e)
            self.led.off()

    def check(self):
        """Check for new MQTT messages."""
        if self.client:
            try:
                self.client.check_msg()
            except Exception as e:
                print("MQTT check error:", e)
                self.led.off()  # Indicate connection issue
                self._try_reconnect()

    def _try_reconnect(self):
        """Try to reconnect to MQTT broker."""
        try:
            self.client.disconnect()
        except:
            pass
        try:
            self.connect()
        except:
            print("Reconnection failed")

    def publish_state(self, state, color_temp):
        """Publish light state update to MQTT."""
        if not self.client:
            return
            
        payload = ujson.dumps({
            "state": "ON" if state else "OFF",
            "color_temp": color_temp
        })
        
        try:
            # Ignore the next message since we'll receive our own update
            self.ignore_next = True
            self.client.publish(self.command_topic, payload)
            print("Published: ", payload)
        except Exception as e:
            print("MQTT publish error:", e)
            self.led.off()  # Indicate connection issue
            self._try_reconnect()
            
    def publish_scene(self, scene_name):
        """Publish scene activation to MQTT."""
        if not self.client:
            return
            
        payload = ujson.dumps({
            "scene": scene_name
        })
        
        try:
            self.ignore_next = True
            self.client.publish(self.scene_command_topic, payload)
            print("Published scene: ", payload)
        except Exception as e:
            print("MQTT scene publish error:", e)
            self.led.off()
            self._try_reconnect()

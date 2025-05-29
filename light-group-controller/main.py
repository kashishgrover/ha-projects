import time
from machine import Pin
from wifi import connect as connect_wifi
from mqtt import MqttLightSync
from secrets import MQTT_BROKER, MQTT_USER, MQTT_PASSWORD

TOPIC_STATE = 'home/living_room_lamps/state'

# Rotary encoder pins
clk = Pin(13, Pin.IN, Pin.PULL_UP)
dt = Pin(12, Pin.IN, Pin.PULL_UP)
sw = Pin(14, Pin.IN, Pin.PULL_UP)

# ==== STATE ====
led_on = True
color_temp = 370
min_temp = 200
max_temp = 454
step = 10

last_clk = clk.value()
last_sw = sw.value()

def on_mqtt_update(state, temp):
    global led_on, color_temp
    led_on = state
    color_temp = temp
    print("HA State updated → led_on:", led_on, "color_temp:", color_temp)

# ==== MAIN ====
connect_wifi()

mqtt = MqttLightSync(
    broker=MQTT_BROKER,
    username=MQTT_USER,
    password=MQTT_PASSWORD,
    state_topic=TOPIC_STATE,
    on_update=on_mqtt_update
)
mqtt.connect()

while True:
    mqtt.check()

    current_clk = clk.value()
    if last_clk and not current_clk:  # falling edge
        if dt.value() != current_clk:
            color_temp += step
        else:
            color_temp -= step
        color_temp = max(min_temp, min(max_temp, color_temp))
        if led_on:
            mqtt.publish_state(led_on, color_temp)
    last_clk = current_clk

    current_sw = sw.value()
    if last_sw and not current_sw:
        led_on = not led_on
        mqtt.publish_state(led_on, color_temp)
    last_sw = current_sw

    time.sleep(0.01)
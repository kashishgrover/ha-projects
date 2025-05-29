import time
from wifi import WiFiManager
from mqtt import MqttLightSync
from encoder import RotaryEncoder
from light_state import LightState
from led_controller import LedController
from secrets import MQTT_BROKER, MQTT_USER, MQTT_PASSWORD
import config

def main():
    # Initialize LED controller
    led = LedController()
    
    # Initialize WiFi connection
    wifi = WiFiManager()
    wifi.connect(max_wait=config.WIFI_MAX_WAIT, retry_count=config.WIFI_RETRY_COUNT)
    
    # Setup MQTT client and define callbacks
    mqtt = None
    
    def publish_state_change(on_state, color_temp):
        if mqtt:
            mqtt.publish_state(on_state, color_temp)
    
    # Create light state controller with callback
    light_state = LightState(
        min_temp=config.MIN_COLOR_TEMP,
        max_temp=config.MAX_COLOR_TEMP,
        default_temp=config.DEFAULT_COLOR_TEMP,
        step=config.COLOR_TEMP_STEP,
        on_state_change=publish_state_change,
        batch_delay_ms=config.BATCH_DELAY_MS
    )
    
    def on_mqtt_update(state, temp):
        if light_state.update_from_external(state, temp):
            print("HA State updated → led_on:", state, "color_temp:", temp)
    
    # Initialize MQTT client after callbacks are defined
    mqtt = MqttLightSync(
        broker=MQTT_BROKER,
        username=MQTT_USER,
        password=MQTT_PASSWORD,
        state_topic=config.MQTT_TOPIC_STATE,
        on_update=on_mqtt_update
    )
    mqtt.connect()
    
    # Setup rotary encoder with callbacks
    encoder = RotaryEncoder(
        clk_pin=config.ENCODER_CLK_PIN,
        dt_pin=config.ENCODER_DT_PIN,
        sw_pin=config.ENCODER_SW_PIN,
        on_rotate=lambda direction: light_state.adjust_temp(direction) if light_state.on else None,
        on_press=light_state.toggle
    )
    
    # Signal that setup is complete by blinking the LED
    for _ in range(3):
        led.toggle()
        time.sleep(0.2)
        led.toggle()
        time.sleep(0.2)
    
    print("Light controller ready!")
    
    # Main loop
    while True:
        # mqtt.check()
        encoder.check()
        
        # Check if any batched updates need to be sent
        light_state.check_pending_updates()
        
        time.sleep(0.01)

if __name__ == "__main__":
    main()
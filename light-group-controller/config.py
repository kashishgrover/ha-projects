# Light settings
DEFAULT_COLOR_TEMP = 370
MIN_COLOR_TEMP = 200
MAX_COLOR_TEMP = 454
COLOR_TEMP_STEP = 5

# Hardware pins
ENCODER_CLK_PIN = 13
ENCODER_DT_PIN = 12
ENCODER_SW_PIN = 14

# MQTT Topics
MQTT_TOPIC_STATE = 'home/living_room_lamps/state'
MQTT_TOPIC_SET = 'home/living_room_lamps/set'

# Connection settings
WIFI_RETRY_COUNT = 3
WIFI_MAX_WAIT = 20  # seconds
MQTT_KEEPALIVE = 60  # seconds

# Performance settings
BATCH_DELAY_MS = 100  # milliseconds to wait before sending batched updates 
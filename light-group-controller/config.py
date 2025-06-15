# Hardware pins
ENCODER_CLK_PIN = 13
ENCODER_DT_PIN = 12
ENCODER_SW_PIN = 14

# Connection settings
WIFI_RETRY_COUNT = 3
WIFI_MAX_WAIT = 20  # seconds
MQTT_KEEPALIVE = 60  # seconds

# Encoder settings
DOUBLE_PRESS_TIMEOUT_MS = 400  # Maximum time between presses to count as double press

# Performance settings
BATCH_DELAY_MS = 100  # milliseconds to wait before sending batched updates 

# Light settings
DEFAULT_COLOR_TEMP = 370
MIN_COLOR_TEMP = 200
MAX_COLOR_TEMP = 454
COLOR_TEMP_STEP = 5

# Scene settings
AVAILABLE_SCENES = ['scene.bright_day', 'scene.warm_evening', 'scene.warmest_night', 'scene.tv_time']

# MQTT Topics
MQTT_TOPIC_STATE = 'home/living_room_lamps/temp/state'
MQTT_TOPIC_SET = 'home/living_room_lamps/temp/set'
MQTT_TOPIC_SCENE_SET = 'home/living_room_lamps/scene/set'

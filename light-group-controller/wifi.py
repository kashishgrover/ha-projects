import network
import time
import machine
from secrets import WIFI_SSID, WIFI_PASSWORD

def connect(max_wait=20):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        for i in range(max_wait):
            if wlan.isconnected():
                break
            time.sleep(0.5)
            print(f"Waiting for connection... {i+1}/{max_wait}")

    if not wlan.isconnected():
        print("Failed to connect to Wi-Fi. Rebooting.")
        time.sleep(2)
        machine.reset()

    print("Wi-Fi connected!")
    print("IP address:", wlan.ifconfig()[0])

    return wlan

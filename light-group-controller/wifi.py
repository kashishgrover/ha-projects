import network
import time
import machine
from secrets import WIFI_SSID, WIFI_PASSWORD
from led_controller import LedController

class WiFiManager:
    def __init__(self, ssid=WIFI_SSID, password=WIFI_PASSWORD):
        """Initialize WiFi manager with credentials."""
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.led = LedController()
        
    def connect(self, max_wait=20, retry_count=3):
        """
        Connect to WiFi with retries.
        
        Args:
            max_wait: Maximum wait time in seconds for each connection attempt
            retry_count: Number of connection retries before rebooting
            
        Returns:
            WLAN interface object if connected
        """
        if self.wlan.isconnected():
            print("Already connected to WiFi")
            print("IP address:", self.wlan.ifconfig()[0])
            self.led.on()  # Indicate successful connection
            return self.wlan
            
        for attempt in range(retry_count):
            print(f"WiFi connection attempt {attempt+1}/{retry_count}")
            
            try:
                self.led.off()  # LED off during connection attempt
                self.wlan.connect(self.ssid, self.password)
                
                # Wait for connection with timeout
                for i in range(max_wait * 2):  # 0.5 second intervals
                    if self.wlan.isconnected():
                        print("WiFi connected!")
                        print("IP address:", self.wlan.ifconfig()[0])
                        self.led.on()  # Indicate successful connection
                        return self.wlan
                    time.sleep(0.5)
                    # Blink LED while connecting
                    if i % 2 == 0:
                        self.led.on()
                    else:
                        self.led.off()
                    print(f"Waiting for connection... {i+1}/{max_wait*2}")
                
                print(f"Connection attempt {attempt+1} timed out")
                self.led.off()  # LED off on timeout
            except Exception as e:
                print(f"Connection error: {e}")
                self.led.off()  # LED off on error
                
        # If we've exhausted all retries, reboot
        print("Failed to connect to WiFi after multiple attempts. Rebooting.")
        # Rapidly blink LED to indicate reboot
        for _ in range(5):
            self.led.toggle()
            time.sleep(0.1)
        time.sleep(2)
        machine.reset()

# For backward compatibility
def connect(max_wait=20):
    """Legacy connect function for backward compatibility."""
    wifi = WiFiManager()
    return wifi.connect(max_wait=max_wait)

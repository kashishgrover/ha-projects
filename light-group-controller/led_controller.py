import machine

class LedController:
    def __init__(self, pin_name="LED"):
        """Initialize the LED controller.
        
        Args:
            pin_name: The name or number of the pin connected to the LED
        """
        self.led = machine.Pin(pin_name, machine.Pin.OUT)
        self.off()  # Start with LED off
    
    def on(self):
        """Turn on the LED."""
        self.led.on()
    
    def off(self):
        """Turn off the LED."""
        self.led.off()
    
    def toggle(self):
        """Toggle the LED state."""
        self.led.toggle()
    
    def set_state(self, state):
        """Set the LED state based on a boolean value.
        
        Args:
            state: True to turn on, False to turn off
        """
        if state:
            self.on()
        else:
            self.off() 
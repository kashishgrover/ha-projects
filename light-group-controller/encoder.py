from machine import Pin

class RotaryEncoder:
    def __init__(self, clk_pin, dt_pin, sw_pin, on_rotate=None, on_press=None):
        """Initialize the rotary encoder with the specified pins and callbacks."""
        self.clk = Pin(clk_pin, Pin.IN, Pin.PULL_UP)
        self.dt = Pin(dt_pin, Pin.IN, Pin.PULL_UP)
        self.sw = Pin(sw_pin, Pin.IN, Pin.PULL_UP)
        
        self.last_clk = self.clk.value()
        self.last_sw = self.sw.value()
        
        self.on_rotate = on_rotate
        self.on_press = on_press
    
    def check(self):
        """Check for rotation or button press events."""
        # Check for rotation
        current_clk = self.clk.value()
        if self.last_clk and not current_clk:
            direction = 1 if self.dt.value() != current_clk else -1
            if self.on_rotate:
                self.on_rotate(direction)
        self.last_clk = current_clk
        
        # Check for button press
        current_sw = self.sw.value()
        if self.last_sw and not current_sw:  # Button pressed
            if self.on_press:
                self.on_press()
        self.last_sw = current_sw 
from machine import Pin
import time
from config import DOUBLE_PRESS_TIMEOUT_MS

class RotaryEncoder:
    def __init__(self, clk_pin, dt_pin, sw_pin, on_rotate=None, on_press=None, on_double_press=None):
        """Initialize the rotary encoder with the specified pins and callbacks."""
        self.clk = Pin(clk_pin, Pin.IN, Pin.PULL_UP)
        self.dt = Pin(dt_pin, Pin.IN, Pin.PULL_UP)
        self.sw = Pin(sw_pin, Pin.IN, Pin.PULL_UP)
        
        self.last_clk = self.clk.value()
        self.last_sw = self.sw.value()
        
        self.on_rotate = on_rotate
        self.on_press = on_press
        self.on_double_press = on_double_press
        
        # Double press detection
        self.last_press_time = 0
        self.press_count = 0
        self.pending_single_press = False
        self.pending_press_time = 0
    
    def check(self):
        """Check for rotation or button press events."""
        current_time = time.ticks_ms()
        
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
            time_since_last_press = time.ticks_diff(current_time, self.last_press_time)
            
            if time_since_last_press < DOUBLE_PRESS_TIMEOUT_MS:
                # This is a double press
                self.press_count = 0
                self.pending_single_press = False  # Cancel any pending single press
                if self.on_double_press:
                    self.on_double_press()
            else:
                # This might be first press of a double press
                self.press_count = 1
                self.pending_single_press = True
                self.pending_press_time = current_time
            
            self.last_press_time = current_time
            
        self.last_sw = current_sw
        
        # Check if pending single press should be executed
        if self.pending_single_press:
            time_since_press = time.ticks_diff(current_time, self.pending_press_time)
            if time_since_press >= DOUBLE_PRESS_TIMEOUT_MS:
                if self.on_press:
                    self.on_press()
                self.pending_single_press = False
                self.press_count = 0 
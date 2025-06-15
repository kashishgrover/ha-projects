import time
from config import AVAILABLE_SCENES

class LightState:
    # Mode constants
    TEMPERATURE_MODE = 'temperature'
    SCENES_MODE = 'scenes'
    
    def __init__(self, min_temp=200, max_temp=454, default_temp=370, step=10, on_state_change=None, on_scene_change=None, batch_delay_ms=300):
        """Initialize the light state with the specified parameters.
        
        Args:
            min_temp: Minimum color temperature value
            max_temp: Maximum color temperature value
            default_temp: Default color temperature
            step: Step size for temperature adjustments
            on_state_change: Callback for state changes
            on_scene_change: Callback for scene changes
            batch_delay_ms: Delay in ms before sending updates (for batching)
        """
        self.on = True
        self.color_temp = default_temp
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.step = step
        self.on_state_change = on_state_change
        self.on_scene_change = on_scene_change
        self.batch_delay_ms = batch_delay_ms
        
        # Mode and scene state
        self.current_mode = self.TEMPERATURE_MODE
        self.current_scene_index = 0
        
        # Batching state
        self.last_change_time = 0
        self.pending_update = False
        self.last_notified_state = (self.on, self.color_temp)
    
    def toggle(self):
        """Toggle the light on/off state."""
        self.on = not self.on
        # Toggle changes should be immediate, not batched
        self._notify_change(force=True)
        return self.on
    
    def toggle_mode(self):
        """Toggle between temperature and scenes mode."""
        if self.current_mode == self.TEMPERATURE_MODE:
            self.current_mode = self.SCENES_MODE
            if self.on_scene_change:
                self.on_scene_change(AVAILABLE_SCENES[self.current_scene_index])
        else:
            self.current_mode = self.TEMPERATURE_MODE
            if self.on_state_change:
                self.on_state_change(self.on, self.color_temp)
        return self.current_mode
    
    def adjust(self, direction):
        """Adjust either temperature or scene based on current mode."""
        if self.current_mode == self.TEMPERATURE_MODE:
            return self.adjust_temp(direction)
        else:
            return self.adjust_scene(direction)
    
    def adjust_temp(self, direction):
        """Adjust the color temperature by the step size in the given direction."""
        self.color_temp += direction * self.step
        self.color_temp = max(self.min_temp, min(self.max_temp, self.color_temp))
        # Mark as pending but don't send immediately
        self._notify_change(force=False)
        return self.color_temp
    
    def adjust_scene(self, direction):
        """Adjust the scene selection."""
        num_scenes = len(AVAILABLE_SCENES)
        self.current_scene_index = (self.current_scene_index + direction) % num_scenes
        if self.on_scene_change:
            self.on_scene_change(AVAILABLE_SCENES[self.current_scene_index])
        return AVAILABLE_SCENES[self.current_scene_index]
    
    def update_from_external(self, on_state, color_temp):
        """Update state from external source (like MQTT)."""
        changed = False
        if self.on != on_state:
            self.on = on_state
            changed = True
        
        if self.color_temp != color_temp:
            self.color_temp = max(self.min_temp, min(self.max_temp, color_temp))
            changed = True
        
        if changed:
            # Update last notified state to match current state
            self.last_notified_state = (self.on, self.color_temp)
            self.pending_update = False
            
        return changed
    
    def check_pending_updates(self):
        """Check if there are pending updates to be sent after the batch delay."""
        if not self.pending_update:
            return False
            
        current_time = time.ticks_ms()
        elapsed = time.ticks_diff(current_time, self.last_change_time)
        
        if elapsed >= self.batch_delay_ms:
            # If enough time has passed, send the update
            current_state = (self.on, self.color_temp)
            if current_state != self.last_notified_state:
                if self.on_state_change:
                    self.on_state_change(self.on, self.color_temp)
                self.last_notified_state = current_state
            self.pending_update = False
            return True
        
        return False
    
    def _notify_change(self, force=False):
        """Notify callback of state change if registered.
        
        Args:
            force: If True, send update immediately; otherwise batch it
        """
        self.last_change_time = time.ticks_ms()
        self.pending_update = True
        
        if force:
            current_state = (self.on, self.color_temp)
            if current_state != self.last_notified_state:
                if self.on_state_change:
                    self.on_state_change(self.on, self.color_temp)
                self.last_notified_state = current_state
                self.pending_update = False 
"""
Hardware simulator for the Fridge Monitor system
Used when running on non-Raspberry Pi hardware
"""
import time
import random
import logging
import sys
from datetime import datetime

logger = logging.getLogger(__name__)

# Create a GPIO module to simulate RPi.GPIO
class GPIO:
    """Simulated GPIO module to replace RPi.GPIO"""
    # Constants for GPIO simulation
    BCM = "BCM"
    BOARD = "BOARD"
    IN = "IN"
    OUT = "OUT"
    HIGH = True
    LOW = False
    RISING = "RISING"
    FALLING = "FALLING"
    BOTH = "BOTH"
    PUD_UP = "PUD_UP"
    PUD_DOWN = "PUD_DOWN"
    
    @staticmethod
    def setmode(mode):
        """Simulate GPIO.setmode"""
        logger.debug(f"Simulated GPIO.setmode({mode})")
        pass
    
    @staticmethod
    def setwarnings(flag):
        """Simulate GPIO.setwarnings"""
        logger.debug(f"Simulated GPIO.setwarnings({flag})")
        pass
    
    @staticmethod
    def setup(pin, mode, pull_up_down=None):
        """Simulate GPIO.setup"""
        logger.debug(f"Simulated GPIO.setup(pin={pin}, mode={mode})")
        pass
    
    @staticmethod
    def input(pin):
        """Simulate GPIO.input"""
        # This will be replaced by read_door_sensor for our use case
        pass
    
    @staticmethod
    def output(pin, state):
        """Simulate GPIO.output"""
        # This will be replaced by set_relay_state for our use case
        pass
    
    @staticmethod
    def add_event_detect(pin, edge, callback=None, bouncetime=None):
        """Simulate GPIO.add_event_detect"""
        logger.debug(f"Simulated GPIO.add_event_detect for pin {pin}")
        pass

# Simulated hardware state
class SimulatedHardwareState:
    """Class to maintain state for simulated hardware"""
    def __init__(self):
        # Default temperature and humidity for fridges
        self.temperatures = {
            # fridge_id: (temperature, humidity)
            1: (4.5, 45.0),  # Main refrigerator
            2: (-18.2, 30.0)  # Freezer
        }
        
        # Door states (True = open, False = closed)
        self.door_states = {
            1: False,  # Main refrigerator door closed
            2: False   # Freezer door closed
        }
        
        # Compressor states (True = on, False = off)
        self.compressor_states = {
            1: False,  # Main refrigerator compressor off
            2: False   # Freezer compressor off
        }
        
        # Time when doors were last opened
        self.door_open_times = {}
        
        # Start simulation with some random fluctuations
        self._start_simulation()
        
    def _start_simulation(self):
        """Initialize with some random variations"""
        # Slightly randomize initial temperatures
        for fridge_id in self.temperatures:
            temp, humidity = self.temperatures[fridge_id]
            # Add small random variation
            temp += random.uniform(-0.5, 0.5)
            humidity += random.uniform(-5, 5)
            self.temperatures[fridge_id] = (temp, humidity)

# Create a single instance to maintain state
simulated_state = SimulatedHardwareState()

# Simulated DHT22
def read_dht22(pin):
    """Simulate reading temperature and humidity from DHT22 sensor"""
    # Determine which fridge based on pin
    fridge_id = 1 if pin == 4 else 2
    
    # Get current simulated temperature and humidity
    temp, humidity = simulated_state.temperatures[fridge_id]
    
    # Add small random fluctuations to simulate sensor readings
    temp += random.uniform(-0.2, 0.2)
    humidity += random.uniform(-1, 1)
    
    # Update stored values
    simulated_state.temperatures[fridge_id] = (temp, humidity)
    
    # Simulate compressor effect - if compressor is on, temperature should decrease
    if simulated_state.compressor_states[fridge_id]:
        cooling_effect = random.uniform(0.1, 0.3)
        new_temp = temp - cooling_effect
        simulated_state.temperatures[fridge_id] = (new_temp, humidity)
    
    # If door is open, temperature should increase
    if simulated_state.door_states[fridge_id]:
        warming_effect = random.uniform(0.1, 0.3)
        new_temp = temp + warming_effect
        simulated_state.temperatures[fridge_id] = (new_temp, humidity)
    
    logger.debug(f"Simulated DHT22 reading for fridge {fridge_id}: {temp:.1f}°C, {humidity:.1f}%")
    return temp, humidity

# Simulated door sensor
def setup_door_sensor(pin):
    """Simulate setup of door sensor"""
    logger.debug(f"Simulated door sensor setup on pin {pin}")
    pass

def read_door_sensor(pin):
    """Simulate reading door sensor state"""
    # Determine which fridge based on pin
    fridge_id = 1 if pin == 17 else 2
    
    # Return current door state
    return simulated_state.door_states[fridge_id]

# Simulated relay
def setup_relay(pin):
    """Simulate setup of relay"""
    logger.debug(f"Simulated relay setup on pin {pin}")
    pass

def set_relay_state(pin, state):
    """Simulate setting relay state"""
    # Determine which fridge based on pin
    fridge_id = 1 if pin == 18 else 2
    
    # Update compressor state
    simulated_state.compressor_states[fridge_id] = state
    
    logger.debug(f"Simulated relay for fridge {fridge_id} set to {'ON' if state else 'OFF'}")
    return True

# Simulated buzzer
def activate_buzzer(duration=1.0):
    """Simulate activating buzzer"""
    logger.debug(f"Simulated buzzer activated for {duration} seconds")
    pass

# These functions are now implemented in the GPIO class above

# Function to simulate door events
def simulate_door_event(fridge_id, event_type):
    """
    Simulate a door open/close event
    
    Args:
        fridge_id: The ID of the fridge (1 or 2)
        event_type: Either 'open' or 'close'
    """
    pin = 17 if fridge_id == 1 else 23  # Door sensor pins
    
    if event_type == 'open':
        simulated_state.door_states[fridge_id] = True
        simulated_state.door_open_times[fridge_id] = datetime.utcnow()
    else:  # close
        simulated_state.door_states[fridge_id] = False
        if fridge_id in simulated_state.door_open_times:
            del simulated_state.door_open_times[fridge_id]
    
    # Find the callback in the sys.modules and call it
    # This is a bit of a hack, but it allows us to trigger the door events
    from sys import modules
    if hasattr(modules['sensor_handlers'], 'door_callback'):
        logger.debug(f"Triggering door callback for fridge {fridge_id}, event {event_type}")
        modules['sensor_handlers'].door_callback(pin, fridge_id)
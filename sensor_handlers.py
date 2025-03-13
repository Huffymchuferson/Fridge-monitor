import time
import logging
import threading
import platform
from datetime import datetime, timedelta
from config import Config

logger = logging.getLogger(__name__)

# Check if we're running on a Raspberry Pi
is_raspberry_pi = platform.system() == 'Linux' and platform.machine().startswith(('arm', 'aarch'))

if is_raspberry_pi:
    logger.info("Running on Raspberry Pi hardware")
    import Adafruit_DHT
    import RPi.GPIO as GPIO
    
    # Use BCM GPIO references
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Constants
    DHT_SENSOR = Adafruit_DHT.DHT22
    BUZZER_PIN = Config.DEFAULT_BUZZER_PIN
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
else:
    logger.info("Running in simulation mode")
    # Import simulation module
    from hardware_simulator import GPIO, read_dht22, setup_door_sensor, read_door_sensor, setup_relay, set_relay_state, activate_buzzer

from app import db
from models import Fridge, TemperatureReading, DoorEvent, Alert

# Dictionary to keep track of door open timestamps
door_open_times = {}
# Lock for thread safety
lock = threading.Lock()

if is_raspberry_pi:
    # Real hardware implementations for Raspberry Pi
    def read_dht22(pin):
        """Read temperature and humidity from DHT22 sensor"""
        try:
            humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, pin)
            if humidity is not None and temperature is not None:
                return temperature, humidity
            else:
                logger.error(f"Failed to read from DHT22 sensor on pin {pin}")
                return None, None
        except Exception as e:
            logger.error(f"Error reading DHT22 sensor: {e}")
            return None, None

    def setup_door_sensor(pin):
        """Setup door sensor pin as input with pull-up resistor"""
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def read_door_sensor(pin):
        """Read door sensor state (True = open, False = closed)"""
        try:
            # Depending on your sensor, you might need to invert this logic
            return GPIO.input(pin) == GPIO.HIGH
        except Exception as e:
            logger.error(f"Error reading door sensor: {e}")
            return False

    def setup_relay(pin):
        """Setup relay pin as output"""
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)  # Ensure relay starts in OFF position

    def set_relay_state(pin, state):
        """Set relay state (True = ON, False = OFF)"""
        try:
            GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)
            return True
        except Exception as e:
            logger.error(f"Error setting relay state: {e}")
            return False

    def activate_buzzer(duration=1.0):
        """Activate buzzer for specified duration in seconds"""
        try:
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(duration)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
        except Exception as e:
            logger.error(f"Error activating buzzer: {e}")
# Simulation implementations are imported at the top when not on Raspberry Pi

def door_callback(channel, fridge_id):
    """Callback function for door sensor state change"""
    try:
        is_open = read_door_sensor(channel)
        with lock:
            fridge = Fridge.query.get(fridge_id)
            if not fridge:
                logger.error(f"Fridge with ID {fridge_id} not found")
                return
                
            logger.debug(f"Door sensor triggered: Fridge {fridge.name}, Door {'Open' if is_open else 'Closed'}")
            
            # Record door event
            event = DoorEvent(
                fridge_id=fridge_id,
                event_type='open' if is_open else 'close',
                timestamp=datetime.utcnow()
            )
            db.session.add(event)
            
            # Handle door open/close
            if is_open:
                door_open_times[fridge_id] = datetime.utcnow()
            else:
                # Clear door open time when closed
                if fridge_id in door_open_times:
                    del door_open_times[fridge_id]
                    
                # Clear any active door open alerts
                active_alerts = Alert.query.filter_by(
                    fridge_id=fridge_id,
                    alert_type='door_open',
                    acknowledged=False
                ).all()
                
                for alert in active_alerts:
                    alert.acknowledged = True
            
            db.session.commit()
    except Exception as e:
        logger.error(f"Error in door callback: {e}")

def check_fridges():
    """Check all fridges for temperature, door status, and alerts"""
    try:
        with lock:
            fridges = Fridge.query.all()
            
            for fridge in fridges:
                # Read temperature and humidity
                temperature, humidity = read_dht22(fridge.dht22_pin)
                if temperature is not None and humidity is not None:
                    # Store reading
                    reading = TemperatureReading(
                        fridge_id=fridge.id,
                        temperature=temperature,
                        humidity=humidity
                    )
                    db.session.add(reading)
                    
                    # Check temperature against thresholds
                    if temperature > fridge.max_temp_threshold:
                        create_alert(fridge.id, 'temp_high', f"Temperature too high: {temperature:.1f}°C")
                        activate_buzzer(0.5)
                    elif temperature < fridge.min_temp_threshold:
                        create_alert(fridge.id, 'temp_low', f"Temperature too low: {temperature:.1f}°C")
                        activate_buzzer(0.5)
                    
                    # Control compressor based on temperature
                    should_compressor_run = temperature > fridge.target_temp
                    if should_compressor_run != fridge.compressor_status:
                        fridge.compressor_status = should_compressor_run
                        set_relay_state(fridge.relay_pin, should_compressor_run)
                    
                    # Check for defrosting (rapid temperature increase)
                    recent_readings = TemperatureReading.query.filter_by(
                        fridge_id=fridge.id
                    ).order_by(TemperatureReading.timestamp.desc()).limit(5).all()
                    
                    if len(recent_readings) >= 5:
                        oldest_temp = recent_readings[-1].temperature
                        if temperature > oldest_temp + 3.0:  # 3°C increase in short time suggests defrosting
                            create_alert(fridge.id, 'defrosting', "Rapid temperature increase detected, possible defrosting")
                            activate_buzzer(0.5)
                
                # Check door status (from saved state)
                if fridge.id in door_open_times:
                    door_open_duration = (datetime.utcnow() - door_open_times[fridge.id]).total_seconds()
                    if door_open_duration > fridge.door_open_alert_seconds:
                        # Check if alert already exists
                        existing_alert = Alert.query.filter_by(
                            fridge_id=fridge.id,
                            alert_type='door_open',
                            acknowledged=False
                        ).first()
                        
                        if not existing_alert:
                            create_alert(
                                fridge.id, 
                                'door_open', 
                                f"Door has been open for {int(door_open_duration)} seconds"
                            )
                            activate_buzzer(1.0)
                
                # Check if maintenance is due
                days_until_maintenance = fridge.days_until_maintenance()
                if days_until_maintenance <= 0:
                    # Check if alert already exists
                    existing_alert = Alert.query.filter_by(
                        fridge_id=fridge.id,
                        alert_type='maintenance_due',
                        acknowledged=False
                    ).first()
                    
                    if not existing_alert:
                        create_alert(
                            fridge.id, 
                            'maintenance_due', 
                            "Annual maintenance is due"
                        )
            
            db.session.commit()
    except Exception as e:
        logger.error(f"Error checking fridges: {e}")

def create_alert(fridge_id, alert_type, message):
    """Create a new alert in the database"""
    try:
        alert = Alert(
            fridge_id=fridge_id,
            alert_type=alert_type,
            message=message
        )
        db.session.add(alert)
        logger.info(f"Created alert: {alert_type} - {message}")
        return alert
    except Exception as e:
        logger.error(f"Error creating alert: {e}")
        return None

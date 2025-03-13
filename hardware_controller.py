import logging
import time
import threading
import platform
from datetime import datetime, timedelta

from flask import current_app

# Check if we're running on a Raspberry Pi
is_raspberry_pi = platform.system() == 'Linux' and platform.machine().startswith(('arm', 'aarch'))

# Import hardware modules based on platform
if is_raspberry_pi:
    import RPi.GPIO as GPIO
else:
    # Use our simulator module when not on Raspberry Pi
    from hardware_simulator import GPIO

from app import db
from models import Fridge
from sensor_handlers import (
    setup_door_sensor, setup_relay, read_door_sensor, 
    door_callback, check_fridges
)

logger = logging.getLogger(__name__)

def setup_hardware_monitoring(app, scheduler):
    """
    Initialize hardware monitoring for all fridges
    Sets up GPIO pins and registers event detection
    """
    try:
        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        
        with app.app_context():
            # Get all fridges
            fridges = Fridge.query.all()
            
            # If no fridges exist, create default ones
            if not fridges:
                logger.info("No fridges found, creating default fridges")
                create_default_fridges()
                fridges = Fridge.query.all()
            
            # Setup hardware for each fridge
            for fridge in fridges:
                # Setup door sensor with callback
                setup_door_sensor(fridge.door_sensor_pin)
                
                # Add event detection for door sensor (both rising and falling edge)
                GPIO.add_event_detect(
                    fridge.door_sensor_pin, 
                    GPIO.BOTH, 
                    callback=lambda channel, fid=fridge.id: door_callback(channel, fid),
                    bouncetime=300
                )
                
                # Setup relay for compressor control
                setup_relay(fridge.relay_pin)
                
                logger.info(f"Hardware setup complete for Fridge {fridge.name}")
            
            # Schedule regular checks (every 30 seconds)
            scheduler.add_job(
                check_fridges_wrapper,
                'interval',
                seconds=30,
                args=[app],
                id='check_fridges',
                replace_existing=True
            )
            
            # Schedule daily cleanup job (remove old readings to save space)
            scheduler.add_job(
                cleanup_old_data_wrapper,
                'cron',
                hour=2,  # 2 AM
                minute=0,
                args=[app],
                id='cleanup_data',
                replace_existing=True
            )
            
            logger.info("Hardware monitoring setup complete")
    
    except Exception as e:
        logger.error(f"Error setting up hardware monitoring: {e}")
        raise

def check_fridges_wrapper(app):
    """Wrapper function to provide app context for the scheduler"""
    with app.app_context():
        from sensor_handlers import check_fridges
        check_fridges()

def cleanup_old_data_wrapper(app):
    """Wrapper function to clean up old data with app context"""
    with app.app_context():
        from utils import cleanup_old_data
        cleanup_old_data()

def create_default_fridges():
    """Create default fridge configurations if none exist"""
    try:
        # Create Fridge 1
        fridge1 = Fridge(
            name="Main Refrigerator",
            description="Kitchen main refrigerator",
            target_temp=4.0,
            min_temp_threshold=2.0,
            max_temp_threshold=8.0,
            door_open_alert_seconds=60,
            dht22_pin=4,  # GPIO4
            door_sensor_pin=17,  # GPIO17
            relay_pin=18,  # GPIO18
            created_at=datetime.utcnow(),
            last_maintenance_date=datetime.utcnow() - timedelta(days=300)  # 300 days ago
        )
        
        # Create Fridge 2
        fridge2 = Fridge(
            name="Freezer",
            description="Kitchen freezer",
            target_temp=-18.0,
            min_temp_threshold=-22.0,
            max_temp_threshold=-15.0,
            door_open_alert_seconds=30,
            dht22_pin=22,  # GPIO22
            door_sensor_pin=23,  # GPIO23
            relay_pin=24,  # GPIO24
            created_at=datetime.utcnow(),
            last_maintenance_date=datetime.utcnow() - timedelta(days=250)  # 250 days ago
        )
        
        db.session.add(fridge1)
        db.session.add(fridge2)
        db.session.commit()
        
        logger.info("Default fridges created")
        
    except Exception as e:
        logger.error(f"Error creating default fridges: {e}")
        db.session.rollback()

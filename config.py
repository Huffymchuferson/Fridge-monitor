import os

class Config:
    """Base configuration settings"""
    # Flask app settings
    SECRET_KEY = os.environ.get('SESSION_SECRET', 'dev_secret_key')
    DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 't')
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///fridge_monitor.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Fridge monitoring settings
    DEFAULT_TARGET_TEMP = 4.0  # Default target temperature in Celsius
    DEFAULT_MIN_TEMP = 2.0     # Default minimum temperature threshold
    DEFAULT_MAX_TEMP = 8.0     # Default maximum temperature threshold
    DOOR_OPEN_ALERT_SECONDS = 60  # Alert after door open for 60 seconds
    
    # Hardware pin defaults (BCM mode)
    DEFAULT_BUZZER_PIN = 27    # Default buzzer pin (changed from 17 to avoid conflict)
    
    # Fridge 1 default pins
    DEFAULT_FRIDGE1_DHT22_PIN = 4     # DHT22 data pin for fridge 1
    DEFAULT_FRIDGE1_DOOR_PIN = 17     # Door sensor pin for fridge 1
    DEFAULT_FRIDGE1_RELAY_PIN = 18    # Relay control pin for fridge 1
    
    # Fridge 2 default pins
    DEFAULT_FRIDGE2_DHT22_PIN = 22    # DHT22 data pin for fridge 2
    DEFAULT_FRIDGE2_DOOR_PIN = 23     # Door sensor pin for fridge 2
    DEFAULT_FRIDGE2_RELAY_PIN = 24    # Relay control pin for fridge 2
    
    # Data retention settings (in days)
    TEMP_DATA_RETENTION_DAYS = 30     # Keep temperature data for 30 days
    DOOR_EVENT_RETENTION_DAYS = 60    # Keep door events for 60 days
    ALERT_RETENTION_DAYS = 90         # Keep acknowledged alerts for 90 days

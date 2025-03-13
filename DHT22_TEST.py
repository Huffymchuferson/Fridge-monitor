#!/usr/bin/python3
"""
Simple DHT22 test script for Raspberry Pi
This script attempts to read from a DHT22 sensor using multiple methods
to help troubleshoot connection issues.
"""

import time
import sys
import board
import adafruit_dht

# IMPORTANT: Change this to the actual GPIO pin you're using
# For GPIO 4, use board.D4
# For GPIO 22, use board.D22
SENSOR_PIN = board.D4  # Change to your pin

# Initialize the DHT22 sensor
dht = adafruit_dht.DHT22(SENSOR_PIN, use_pulseio=False)

print("DHT22 Test Script")
print("-----------------")
print(f"Using pin: GPIO {SENSOR_PIN}")
print("Press CTRL+C to exit")
print()

# Keep track of consecutive errors
error_count = 0
max_errors = 10

try:
    while True:
        try:
            # Attempt to get reading
            temperature = dht.temperature
            humidity = dht.humidity
            
            # If we get here, reading was successful
            print(f"Temperature: {temperature:.1f}°C")
            print(f"Humidity: {humidity:.1f}%")
            print("-----------------")
            
            # Reset error count on success
            error_count = 0
            
        except RuntimeError as e:
            # Common errors during reading
            error_count += 1
            print(f"Reading failed: {e}")
            print(f"Error count: {error_count}/{max_errors}")
            
            if error_count >= max_errors:
                print("\nToo many consecutive errors. Troubleshooting tips:")
                print("1. Check your wiring connections")
                print("2. Verify you're using the correct GPIO pin number")
                print("3. Make sure the pull-up resistor is properly connected")
                print("4. Try a different DHT22 sensor if possible")
                print("5. Try a shorter cable or different breadboard")
                print("\nResetting error count and continuing...")
                error_count = 0
        
        # DHT22 needs about 2 seconds between readings
        time.sleep(2)
        
except KeyboardInterrupt:
    print("\nTest ended by user")
    
finally:
    # Clean up
    dht.exit()
    print("Test complete")
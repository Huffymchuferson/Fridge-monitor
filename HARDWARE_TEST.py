#!/usr/bin/env python3
"""
Raspberry Pi Fridge Monitor Hardware Test Script

This script tests each hardware component individually to ensure proper setup:
- DHT22 temperature/humidity sensor
- Door magnetic sensor
- Relay control
- Buzzer
"""

import time
import platform
import sys

print("Raspberry Pi Fridge Monitor - Hardware Test")
print("==========================================")

# Check if running on Raspberry Pi
is_raspberry_pi = platform.system() == 'Linux' and platform.machine().startswith(('arm', 'aarch'))
if not is_raspberry_pi:
    print("ERROR: This script should be run on a Raspberry Pi!")
    print("If you are on a Raspberry Pi, this detection error might be unusual.")
    user_input = input("Continue anyway? (y/n): ")
    if user_input.lower() != 'y':
        sys.exit(1)

print("Loading GPIO libraries...")
try:
    import RPi.GPIO as GPIO
    import board
    import adafruit_dht
    print("GPIO libraries loaded successfully!")
except ImportError as e:
    print(f"ERROR: Failed to load GPIO libraries. {e}")
    print("Please install required libraries using:")
    print("pip3 install RPi.GPIO adafruit-circuitpython-dht")
    sys.exit(1)

# Default pin configuration
DEFAULT_BUZZER_PIN = 27
DEFAULT_FRIDGE1_DHT22_PIN = 4
DEFAULT_FRIDGE1_DOOR_PIN = 17
DEFAULT_FRIDGE1_RELAY_PIN = 18
DEFAULT_FRIDGE2_DHT22_PIN = 22
DEFAULT_FRIDGE2_DOOR_PIN = 23
DEFAULT_FRIDGE2_RELAY_PIN = 24

# Setup GPIO
print("Initializing GPIO...")
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def test_dht22(pin):
    """Test DHT22 sensor"""
    print(f"\nTesting DHT22 sensor on pin {pin}...")
    dht_device = None
    try:
        # Create a DHT22 object
        if pin == 4:
            dht_device = adafruit_dht.DHT22(board.D4)
        elif pin == 22:
            dht_device = adafruit_dht.DHT22(board.D22)
        else:
            print(f"ERROR: Pin {pin} not directly supported in this test script.")
            print("Please modify the script to support this pin.")
            return False
        
        # Try to read 3 times (DHT sensors can be flaky)
        success = False
        for attempt in range(3):
            try:
                temperature = dht_device.temperature
                humidity = dht_device.humidity
                print(f"  Reading {attempt+1}: Temperature = {temperature:.1f}°C, Humidity = {humidity:.1f}%")
                success = True
                break
            except RuntimeError as e:
                print(f"  Reading {attempt+1} failed: {e}")
                time.sleep(2)
                
        if success:
            print("DHT22 sensor test PASSED!")
            return True
        else:
            print("DHT22 sensor test FAILED after 3 attempts.")
            print("Check wiring and ensure the pull-up resistor is properly connected.")
            return False
            
    except Exception as e:
        print(f"ERROR testing DHT22: {e}")
        return False
    finally:
        if dht_device:
            dht_device.exit()

def test_door_sensor(pin):
    """Test door magnetic sensor"""
    print(f"\nTesting door sensor on pin {pin}...")
    try:
        # Setup the pin with pull-up resistor
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Read initial state
        initial_state = GPIO.input(pin)
        print(f"  Initial state: {'OPEN' if initial_state == GPIO.HIGH else 'CLOSED'}")
        
        print("  Please open and close the door/sensor within the next 10 seconds...")
        
        # Monitor for changes over 10 seconds
        start_time = time.time()
        state_changed = False
        last_state = initial_state
        
        while time.time() - start_time < 10:
            current_state = GPIO.input(pin)
            if current_state != last_state:
                state = "OPEN" if current_state == GPIO.HIGH else "CLOSED"
                print(f"  Door sensor state changed: {state}")
                state_changed = True
                last_state = current_state
            time.sleep(0.1)
            
        if state_changed:
            print("Door sensor test PASSED!")
            return True
        else:
            print("Door sensor test FAILED: No state change detected.")
            print("Try manually triggering the sensor or check wiring.")
            return False
            
    except Exception as e:
        print(f"ERROR testing door sensor: {e}")
        return False

def test_relay(pin):
    """Test relay control"""
    print(f"\nTesting relay on pin {pin}...")
    try:
        # Setup the pin as output
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        
        # Cycle the relay
        print("  Turning relay ON...")
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(2)
        
        print("  Turning relay OFF...")
        GPIO.output(pin, GPIO.LOW)
        
        print("Relay test PASSED!")
        return True
        
    except Exception as e:
        print(f"ERROR testing relay: {e}")
        return False

def test_buzzer(pin):
    """Test buzzer"""
    print(f"\nTesting buzzer on pin {pin}...")
    try:
        # Setup the pin as output
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        
        # Beep pattern
        print("  Buzzer should beep 3 times...")
        for _ in range(3):
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.2)
            
        print("Buzzer test PASSED!")
        return True
        
    except Exception as e:
        print(f"ERROR testing buzzer: {e}")
        return False

def main():
    """Main test function"""
    try:
        # Display pin configuration
        print("\nCurrent pin configuration:")
        print(f"Buzzer: GPIO {DEFAULT_BUZZER_PIN}")
        print("\nFridge 1:")
        print(f"- DHT22: GPIO {DEFAULT_FRIDGE1_DHT22_PIN}")
        print(f"- Door Sensor: GPIO {DEFAULT_FRIDGE1_DOOR_PIN}")
        print(f"- Relay: GPIO {DEFAULT_FRIDGE1_RELAY_PIN}")
        print("\nFridge 2:")
        print(f"- DHT22: GPIO {DEFAULT_FRIDGE2_DHT22_PIN}")
        print(f"- Door Sensor: GPIO {DEFAULT_FRIDGE2_DOOR_PIN}")
        print(f"- Relay: GPIO {DEFAULT_FRIDGE2_RELAY_PIN}")
        
        print("\nPress Enter to start each test, or type 'skip' to skip a test.")
        
        # Test Fridge 1 components
        print("\n===== TESTING FRIDGE 1 COMPONENTS =====")
        
        input("\nPress Enter to test Fridge 1 DHT22 sensor, or type 'skip': ")
        if input().lower() != 'skip':
            test_dht22(DEFAULT_FRIDGE1_DHT22_PIN)
        
        input("\nPress Enter to test Fridge 1 door sensor, or type 'skip': ")
        if input().lower() != 'skip':
            test_door_sensor(DEFAULT_FRIDGE1_DOOR_PIN)
        
        input("\nPress Enter to test Fridge 1 relay, or type 'skip': ")
        if input().lower() != 'skip':
            test_relay(DEFAULT_FRIDGE1_RELAY_PIN)
        
        # Test Fridge 2 components
        print("\n===== TESTING FRIDGE 2 COMPONENTS =====")
        
        input("\nPress Enter to test Fridge 2 DHT22 sensor, or type 'skip': ")
        if input().lower() != 'skip':
            test_dht22(DEFAULT_FRIDGE2_DHT22_PIN)
        
        input("\nPress Enter to test Fridge 2 door sensor, or type 'skip': ")
        if input().lower() != 'skip':
            test_door_sensor(DEFAULT_FRIDGE2_DOOR_PIN)
        
        input("\nPress Enter to test Fridge 2 relay, or type 'skip': ")
        if input().lower() != 'skip':
            test_relay(DEFAULT_FRIDGE2_RELAY_PIN)
        
        # Test buzzer
        print("\n===== TESTING BUZZER =====")
        
        input("\nPress Enter to test buzzer, or type 'skip': ")
        if input().lower() != 'skip':
            test_buzzer(DEFAULT_BUZZER_PIN)
        
        print("\nHardware tests completed!")
        
    except KeyboardInterrupt:
        print("\nTests interrupted by user.")
    finally:
        print("\nCleaning up GPIO...")
        GPIO.cleanup()
        print("Done!")

if __name__ == "__main__":
    main()
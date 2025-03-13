#!/usr/bin/python3
"""
Alternative DHT22 test script using direct GPIO access
This script uses a different method to read the DHT22 sensor
"""

import time
import RPi.GPIO as GPIO

# Configuration
DHT_PIN = 4  # Change this to your GPIO pin number (BCM numbering)
MAX_RETRIES = 15

def read_dht22(pin):
    """
    Read temperature and humidity from DHT22 sensor using direct GPIO method
    Returns (temperature, humidity) tuple or (None, None) on failure
    """
    # Initialize GPIO
    GPIO.setmode(GPIO.BCM)
    
    # Prepare data buffer
    data = [0] * 40
    
    # Start by setting pin as output and sending start signal
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.05)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.02)  # Hold low for 20ms to signal DHT22
    GPIO.output(pin, GPIO.HIGH)
    
    # Switch to input mode with pullup
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Wait for response from sensor (low, then high, then data)
    count = 0
    while GPIO.input(pin) == GPIO.HIGH:
        count += 1
        if count > 1000:  # Timeout
            return None, None
    
    # Read data (40 bits: 16 bits for humidity, 16 bits for temperature, 8 bits for checksum)
    for i in range(40):
        count = 0
        while GPIO.input(pin) == GPIO.LOW:
            count += 1
            if count > 1000:  # Timeout
                return None, None
        
        count = 0
        start = time.time()
        while GPIO.input(pin) == GPIO.HIGH:
            count += 1
            if count > 1000:  # Timeout
                return None, None
        
        duration = time.time() - start
        data[i] = 0 if duration < 0.00005 else 1  # If high pulse is >50us, bit is 1
    
    # Convert bits to bytes
    humidity = 0
    temperature = 0
    checksum = 0
    
    for i in range(16):
        humidity = (humidity << 1) | data[i]
    for i in range(16, 32):
        temperature = (temperature << 1) | data[i]
    for i in range(32, 40):
        checksum = (checksum << 1) | data[i]
    
    # Verify checksum (lower 8 bits of sum)
    calc_checksum = ((humidity & 0xFF) + (humidity >> 8) + 
                    (temperature & 0xFF) + (temperature >> 8)) & 0xFF
    
    if calc_checksum != checksum:
        return None, None
    
    # Convert integer readings to actual values
    humidity = humidity / 10.0
    
    # For negative temperatures, check most significant bit of temperature
    if temperature & 0x8000:
        temperature = -(temperature & 0x7FFF)
    temperature = temperature / 10.0
    
    return temperature, humidity

def main():
    """Main test function"""
    print("DHT22 Alternative Test")
    print("---------------------")
    print(f"Using GPIO pin: {DHT_PIN}")
    print("Press CTRL+C to exit")
    print("")
    
    try:
        for i in range(MAX_RETRIES):
            print(f"Reading attempt {i+1}/{MAX_RETRIES}...")
            
            temp, humidity = read_dht22(DHT_PIN)
            
            if temp is not None and humidity is not None:
                print(f"Temperature: {temp:.1f}°C")
                print(f"Humidity: {humidity:.1f}%")
                print("Success!")
                break
            else:
                print("Reading failed, retrying...")
            
            # Wait before trying again
            time.sleep(2)
        else:
            print("\nFailed after maximum retries.")
            print("\nTroubleshooting tips:")
            print("1. Check your wiring connections")
            print("2. Verify you're using the correct GPIO pin number")
            print("3. Make sure the pull-up resistor is properly connected")
            print("4. Try a different DHT22 sensor if possible")
    
    finally:
        # Clean up GPIO
        GPIO.cleanup()
        print("Test complete")

if __name__ == "__main__":
    main()
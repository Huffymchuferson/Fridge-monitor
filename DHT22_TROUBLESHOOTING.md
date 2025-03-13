# DHT22 Sensor Troubleshooting Guide

## Common DHT22 Problems and Solutions

### 1. Correct Wiring Diagram

Here's the proper wiring for the DHT22 with a 10kΩ resistor:

```
Raspberry Pi                  DHT22 Sensor
-------------                 ------------
3.3V         ----------------- Pin 1 (VCC)
                    |
                   10kΩ 
                    |
GPIO 4/22   ----------------- Pin 2 (DATA)
GND         ----------------- Pin 4 (GND)
```

### 2. Cable Length and Quality

- **Keep wires short**: Any wires connecting DHT22 to Raspberry Pi should ideally be under 20cm
- **Use good quality wires**: Cheap jumper wires can cause reliability issues
- **Try direct connections**: If using a breadboard, try connecting directly to GPIO pins

### 3. Power Supply Issues

- **Stable power**: Ensure your Raspberry Pi has a stable, adequate power supply (at least 2.5A)
- **Voltage check**: If possible, use a multimeter to verify 3.3V is reaching the sensor
- **Separate power**: In some cases, powering the DHT22 from a separate regulated 3.3V supply can help

### 4. Environmental Factors

- **Wait between readings**: DHT22 needs at least 2 seconds between reading attempts
- **Avoid interference**: Keep away from EMI sources (motors, power supplies)
- **Adequate ventilation**: Ensure air can freely circulate around the sensor

### 5. Testing with Simplified Code

Two test scripts are included:
- `DHT22_TEST.py` - Uses Adafruit library
- `DHT22_ALT_TEST.py` - Uses direct GPIO access

To run them:

```bash
# First test (uses Adafruit library)
python3 DHT22_TEST.py

# Second test (direct GPIO access)
python3 DHT22_ALT_TEST.py
```

### 6. Library-Specific Issues

If you get specific errors from the Adafruit library:

- "Checksum failure" - Likely a wiring or timing issue
- "Timed out waiting for PulseIn start" - Poor connection or timing issue
- "Timed out waiting for PulseIn end" - Possible interference or wiring issue

### 7. Hardware Substitution Test

If possible, try:
- A different DHT22 sensor
- A different GPIO pin
- A different resistor
- A different Raspberry Pi

### 8. Simplified Test Circuit

For a bare minimum test:

1. Connect only the DHT22 (remove all other components from the circuit)
2. Use the shortest possible wires
3. Use a breadboard with good connections
4. Run the DHT22_TEST.py script with appropriate pin number

### 9. Sensor Verification

If nothing works, verify your sensor is functioning with this quick test:

1. Disconnect everything
2. Connect DHT22 VCC to 3.3V
3. Connect DHT22 GND to GND
4. Connect a small LED with resistor to the DATA pin
5. The LED should flicker occasionally if the sensor is active
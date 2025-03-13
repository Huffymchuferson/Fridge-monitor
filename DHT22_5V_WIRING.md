# 5V DHT22 Sensor Wiring Guide

## Correct Wiring for 5V DHT22 Sensors

When using a 5V DHT22 sensor with Raspberry Pi, the correct wiring requires special attention to the data line voltage levels:

### Materials Needed
- DHT22 sensor (5V version)
- 10kΩ resistor (for pull-up)
- 4.7kΩ or 10kΩ resistor (for voltage divider)
- Jumper wires

### Connection Diagram with Level Shifting

```
Raspberry Pi                           DHT22 Sensor (5V)
-------------                          ----------------
5V           -------------------------- Pin 1 (VCC)
                         |
                        10kΩ (Pull-up)
                         |
3.3V          ---|      |
                 |      |
                4.7kΩ   |
                 |      |
GPIO 4/22   ----|------- Pin 2 (DATA)
GND         -------------------------- Pin 4 (GND)
```

### Step-by-Step Instructions

1. **Power Connection**:
   - Connect the VCC pin (Pin 1) of the DHT22 to the 5V pin on the Raspberry Pi
   - Connect the GND pin (Pin 4) of the DHT22 to any GND pin on the Raspberry Pi

2. **Data Line with Voltage Divider (IMPORTANT)**:
   - Connect a 4.7kΩ resistor between the 3.3V pin of the Raspberry Pi and the DATA pin (Pin 2) of the DHT22
   - Connect the DATA pin (Pin 2) to the GPIO pin (GPIO 4 or 22)
   - Connect a 10kΩ pull-up resistor between the VCC (5V) and the DATA pin of the DHT22

3. **Why This Works**:
   - The 5V DHT22 outputs 5V logic levels which are too high for the Raspberry Pi (which uses 3.3V logic)
   - The voltage divider created by the 4.7kΩ resistor brings the voltage down to a safe level for the Pi
   - The 10kΩ pull-up resistor ensures proper signal levels for the DHT22

## Alternative Simple Method

If you don't have the resistors for the voltage divider, a simpler (but less reliable) approach is:

```
Raspberry Pi                           DHT22 Sensor (5V)
-------------                          ----------------
5V           -------------------------- Pin 1 (VCC)
                         |
                        10kΩ (Pull-up)
                         |
GPIO 4/22   ------------------ Pin 2 (DATA)
GND         -------------------------- Pin 4 (GND)
```

**WARNING**: This method works in many cases but carries a small risk of damaging your Pi's GPIO pins over time due to the voltage mismatch.

## Testing Your Connection

After wiring, use the provided test scripts:

```bash
# Make sure you're in the installation directory
cd /home/pi/fridge-monitor

# Run the test script
python3 DHT22_TEST.py
```

## Troubleshooting 5V DHT22 Issues

1. **Intermittent readings**: This is often due to inadequate voltage level shifting. Ensure your voltage divider is properly connected.

2. **No readings at all**: Double-check that you're supplying 5V to the sensor, not 3.3V.

3. **Unstable readings**: Increase capacitance by adding a 1μF capacitor between VCC and GND close to the sensor.

4. **Short wires**: Keep wires as short as possible to minimize noise.
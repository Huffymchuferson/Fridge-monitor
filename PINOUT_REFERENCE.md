# Raspberry Pi GPIO Pinout Reference

This quick reference guide shows the GPIO pin assignments for the Fridge Monitoring System. All pin numbers are in BCM mode.

## Default Pin Configuration

| Component | Fridge 1 | Fridge 2 | Notes |
|-----------|----------|----------|-------|
| DHT22 Sensor | GPIO 4 | GPIO 22 | Requires 10K pull-up resistor |
| Door Sensor | GPIO 17 | GPIO 23 | Connect to ground |
| Relay Control | GPIO 18 | GPIO 24 | Active high |
| Buzzer | GPIO 17 | - | Shared component |

## Raspberry Pi GPIO Header (40-pin)

```
                  +-----+
                  | USB |
                  +-----+
                +--------+
                | HDMI 0 |
                +--------+
                  +---+
                  |ETH|
                  +---+
           +==============+
 +3.3V   1 | O        O | 2   +5V
 GPIO2   3 | O        O | 4   +5V
 GPIO3   5 | O        O | 6   GND
 GPIO4   7 | O        O | 8   GPIO14
   GND   9 | O        O | 10  GPIO15
GPIO17  11 | O        O | 12  GPIO18
GPIO27  13 | O        O | 14  GND
GPIO22  15 | O        O | 16  GPIO23
 +3.3V  17 | O        O | 18  GPIO24
GPIO10  19 | O        O | 20  GND
 GPIO9  21 | O        O | 22  GPIO25
GPIO11  23 | O        O | 24  GPIO8
   GND  25 | O        O | 26  GPIO7
 GPIO0  27 | O        O | 28  GPIO1
 GPIO5  29 | O        O | 30  GND
 GPIO6  31 | O        O | 32  GPIO12
GPIO13  33 | O        O | 34  GND
GPIO19  35 | O        O | 36  GPIO16
GPIO26  37 | O        O | 38  GPIO20
   GND  39 | O        O | 40  GPIO21
           +==============+
```

## System Pin Assignments (Highlighted)

- **Fridge 1 DHT22 Data**: GPIO 4 (Pin 7)
- **Fridge 1 Door Sensor**: GPIO 17 (Pin 11)
- **Fridge 1 Relay Control**: GPIO 18 (Pin 12)
- **Fridge 2 DHT22 Data**: GPIO 22 (Pin 15)
- **Fridge 2 Door Sensor**: GPIO 23 (Pin 16)
- **Fridge 2 Relay Control**: GPIO 24 (Pin 18)
- **Buzzer**: GPIO 17 (Pin 11) - Note: This conflicts with Fridge 1 Door Sensor

## Power and Ground Connections

- **DHT22 Sensors**: 
  - VCC: 3.3V (Pin 1 or 17) or 5V (Pin 2 or 4) - check sensor specifications
  - GND: Any GND pin (9, 14, 20, 25, 30, 34, or 39)
  
- **Door Sensors**:
  - One pin to GPIO pin
  - Other pin to any GND pin

- **Relay Modules**:
  - VCC: 5V (Pin 2 or 4)
  - GND: Any GND pin
  - IN: GPIO pin

- **Buzzer**:
  - Positive (+) to GPIO pin
  - Negative (-) to any GND pin

## Important Note About Pin Conflicts

In the default configuration, there is a conflict with GPIO 17 used for both the buzzer and Fridge 1 door sensor. There are two ways to resolve this:

1. **Change the buzzer pin** in `config.py`:
   ```python
   DEFAULT_BUZZER_PIN = 26  # Change to an unused GPIO pin
   ```

2. **Use a different pin for Fridge 1 door sensor** in `config.py`:
   ```python
   DEFAULT_FRIDGE1_DOOR_PIN = 27  # Change to an unused GPIO pin
   ```

## Customizing Pin Assignments

You can change any pin assignment in the `config.py` file:

```python
# Hardware pin defaults (BCM mode)
DEFAULT_BUZZER_PIN = 17    # Default buzzer pin

# Fridge 1 default pins
DEFAULT_FRIDGE1_DHT22_PIN = 4     # DHT22 data pin for fridge 1
DEFAULT_FRIDGE1_DOOR_PIN = 17     # Door sensor pin for fridge 1
DEFAULT_FRIDGE1_RELAY_PIN = 18    # Relay control pin for fridge 1

# Fridge 2 default pins
DEFAULT_FRIDGE2_DHT22_PIN = 22    # DHT22 data pin for fridge 2
DEFAULT_FRIDGE2_DOOR_PIN = 23     # Door sensor pin for fridge 2
DEFAULT_FRIDGE2_RELAY_PIN = 24    # Relay control pin for fridge 2
```
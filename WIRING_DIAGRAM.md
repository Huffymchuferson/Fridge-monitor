# Comprehensive Wiring Guide for Fridge Monitor System

## Component Wiring Instructions

### 1. DHT22 Temperature/Humidity Sensor

**Connections:**
- VCC pin → 3.3V pin on Raspberry Pi
- GND pin → GND pin on Raspberry Pi 
- DATA pin → GPIO pin (with 4.7kΩ pull-up resistor)
  - Fridge 1: GPIO 4
  - Fridge 2: GPIO 22

**Note:** The DHT22 requires a 4.7kΩ pull-up resistor between the DATA and VCC pins.

### 2. Door Magnetic Sensor (CRITICAL SAFETY COMPONENT)

**Correct Connections:**
- One wire → GPIO pin (with 1kΩ current-limiting resistor for safety)
  - Fridge 1: GPIO 17
  - Fridge 2: GPIO 23
- Other wire → GND pin on Raspberry Pi

**IMPORTANT SAFETY WARNING:** 
- Do NOT connect the door sensor to any power pin (3.3V or 5V)
- The door sensor acts as a simple switch that should only connect between GPIO and GND
- Always use a current-limiting resistor to protect your Pi from accidental shorts

### 3. Relay Module

**Connections:**
- VCC pin → 5V pin on Raspberry Pi
- GND pin → GND pin on Raspberry Pi
- IN pin → GPIO pin
  - Fridge 1: GPIO 18
  - Fridge 2: GPIO 24

**Note:** Most relay modules are active-LOW, meaning they trigger when the GPIO pin is set LOW.

### 4. Buzzer

**Connections:**
- Positive (+) pin → GPIO 27 (through a 330Ω resistor)
- Negative (-) pin → GND pin on Raspberry Pi

## Complete Wiring Diagram

```
Raspberry Pi                 Components
-------------                ----------
3.3V         ------------------- VCC (DHT22 Fridge 1)
GPIO 4       -[4.7kΩ]----------- DATA (DHT22 Fridge 1)
GND          ------------------- GND (DHT22 Fridge 1)

3.3V         ------------------- VCC (DHT22 Fridge 2)
GPIO 22      -[4.7kΩ]----------- DATA (DHT22 Fridge 2)
GND          ------------------- GND (DHT22 Fridge 2)

GPIO 17      -[1kΩ]------------- Door Sensor Fridge 1 - Terminal 1
GND          ------------------- Door Sensor Fridge 1 - Terminal 2

GPIO 23      -[1kΩ]------------- Door Sensor Fridge 2 - Terminal 1
GND          ------------------- Door Sensor Fridge 2 - Terminal 2

5V           ------------------- VCC (Relay Fridge 1)
GPIO 18      ------------------- IN (Relay Fridge 1)
GND          ------------------- GND (Relay Fridge 1)

5V           ------------------- VCC (Relay Fridge 2)
GPIO 24      ------------------- IN (Relay Fridge 2)
GND          ------------------- GND (Relay Fridge 2)

GPIO 27      -[330Ω]------------ Buzzer (+)
GND          ------------------- Buzzer (-)
```

## Testing Your Wiring

**SAFE TESTING SEQUENCE:**

1. Start with all components disconnected
2. Connect ONLY the DHT22 sensors and test with HARDWARE_TEST.py
3. Connect the buzzer and test
4. Connect the relay modules and test
5. ONLY AFTER all other tests succeed, connect the door sensors with the safety resistors installed
6. Run the full system

Follow this sequence to isolate problems and avoid damaging your Raspberry Pi.
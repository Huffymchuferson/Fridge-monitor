# Door Sensor Wiring Guide

## Important Safety Warning
If your Raspberry Pi is shutting down when the door closes, you have a dangerous wiring issue that must be corrected immediately.

## Correct Door Sensor Wiring

The magnetic door sensor is a simple switch that should be wired as follows:

### Materials Needed
- Magnetic door sensor
- 1kΩ resistor (for additional safety)
- Jumper wires

### Connection Steps

1. Connect one wire from the door sensor to the GPIO pin through a 1kΩ resistor:
   - For Fridge 1: GPIO 17
   - For Fridge 2: GPIO 23

2. Connect the other wire from the door sensor directly to any GND (ground) pin on the Raspberry Pi.

3. Do NOT connect any wires from the door sensor to the 3.3V or 5V pins. The needed pull-up is handled internally by the software.

## Wiring Diagram (ASCII)

```
Raspberry Pi                  Door Sensor
-------------                 -----------
GPIO 17/23  ----[1kΩ]----+---O    O---+
                          |             |
GND         -----------------------------
```

## How It Works

1. The internal pull-up resistor (enabled in software) keeps the GPIO pin HIGH when the door is open (switch open).

2. When the door closes, the magnetic sensor connects the GPIO pin to GND, making it read LOW.

3. The 1kΩ resistor provides protection in case of wiring errors, limiting current flow.

## Debugging Tips

If your Raspberry Pi shuts down when the door closes:
1. Disconnect the door sensor immediately
2. Check that you haven't connected any wires to the 3.3V or 5V pins
3. Verify you're using the correct GPIO pins
4. Add the 1kΩ protection resistor as shown above

The Raspberry Pi should NEVER shut down when the door sensor changes state. If it does, there is a wiring problem that must be fixed before continuing.
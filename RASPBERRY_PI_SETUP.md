# Raspberry Pi Setup Guide

This guide provides detailed instructions for setting up the Fridge Monitoring System on a Raspberry Pi.

## Hardware Setup

### Components Needed

- Raspberry Pi (3 or 4 recommended)
- 2× DHT22 temperature/humidity sensors
- 2× Magnetic door switches (any reed switch will work)
- 2× Relay modules (for compressor control)
- 1× Buzzer
- Jumper wires
- Breadboard (optional, for easier prototyping)
- 2× 10K ohm resistors (for DHT22 sensors)

### Wiring Diagram

#### DHT22 Sensor

```
DHT22 Pin | Raspberry Pi
----------|--------------
VCC       | 3.3V or 5V (check sensor specs)
Data      | GPIO 4 (fridge 1) / GPIO 22 (fridge 2)
GND       | Ground
```

Note: Connect a 10K ohm pull-up resistor between VCC and Data pins.

#### Magnetic Door Switch

```
Door Switch | Raspberry Pi
------------|--------------
Pin 1       | GPIO 17 (fridge 1) / GPIO 23 (fridge 2)
Pin 2       | Ground
```

#### Relay Module

```
Relay Module | Raspberry Pi
-------------|--------------
VCC          | 5V
GND          | Ground
IN           | GPIO 18 (fridge 1) / GPIO 24 (fridge 2)
```

#### Buzzer

```
Buzzer | Raspberry Pi
-------|--------------
+      | GPIO 17
-      | Ground
```

Note: If you're using the same pin (GPIO 17) for both a door sensor and the buzzer, you'll need to adjust the pin configuration in `config.py`.

## Software Installation

### 1. Update and Install System Dependencies

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y git python3-pip python3-dev
sudo apt install -y libgpiod2 python3-libgpiod
```

### 2. Clone the Repository

```bash
git clone https://github.com/yourusername/fridge-monitor.git
cd fridge-monitor
```

### 3. Copy Files to Raspberry Pi

If you're not cloning from a repository, you can transfer the files to your Raspberry Pi using:

- **SCP** (from your computer):
  ```bash
  scp -r /path/to/fridge-monitor pi@raspberry_pi_ip:/home/pi/
  ```

- **USB Drive**: Copy the files to a USB drive, connect to Raspberry Pi, and copy the files.

### 4. Install Python Dependencies

```bash
pip3 install adafruit-circuitpython-dht
pip3 install APScheduler
pip3 install email-validator
pip3 install Flask
pip3 install Flask-SQLAlchemy
pip3 install gunicorn
pip3 install psycopg2-binary
pip3 install RPi.GPIO
```

### 5. Configure the Application

1. The application automatically detects if it's running on a Raspberry Pi.
2. Ensure the correct pin assignments in `config.py`:

```python
# Default pin assignments in BCM mode
DEFAULT_BUZZER_PIN = 17
DEFAULT_FRIDGE1_DHT22_PIN = 4
DEFAULT_FRIDGE1_DOOR_PIN = 17
DEFAULT_FRIDGE1_RELAY_PIN = 18
DEFAULT_FRIDGE2_DHT22_PIN = 22
DEFAULT_FRIDGE2_DOOR_PIN = 23
DEFAULT_FRIDGE2_RELAY_PIN = 24
```

### 6. Run the Application

For testing:

```bash
python3 main.py
```

For production (using Gunicorn):

```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port main:app
```

### 7. Set Up Automatic Start on Boot

```bash
sudo nano /etc/systemd/system/fridge-monitor.service
```

Add the following content:

```
[Unit]
Description=Fridge Monitoring System
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/fridge-monitor
ExecStart=/usr/local/bin/gunicorn --bind 0.0.0.0:5000 --reuse-port main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable fridge-monitor.service
sudo systemctl start fridge-monitor.service
```

## Accessing the Web Interface

- **From the Raspberry Pi**: Open a browser and navigate to http://localhost:5000
- **From another device on the same network**: Open a browser and navigate to http://raspberry_pi_ip:5000

To find your Raspberry Pi's IP address:

```bash
hostname -I
```

## Troubleshooting

### GPIO Permission Issues

If you get permission errors when accessing GPIO:

```bash
sudo usermod -a -G gpio pi
sudo reboot
```

### DHT22 Sensor Issues

If you're having trouble with DHT22 readings:

1. Check wiring and ensure the 10K pull-up resistor is connected.
2. Try using the Adafruit test script:

```python
import time
import adafruit_dht
import board

dht_device = adafruit_dht.DHT22(board.D4)  # Change to your GPIO pin

while True:
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        print(f"Temp: {temperature:.1f}°C, Humidity: {humidity:.1f}%")
    except RuntimeError as e:
        print(f"Reading error: {e}")
    time.sleep(2)
```

### Check Service Status

If the service isn't starting properly:

```bash
sudo systemctl status fridge-monitor.service
```

To see detailed logs:

```bash
journalctl -u fridge-monitor.service -f
```
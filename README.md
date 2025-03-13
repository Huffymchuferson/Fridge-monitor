# Raspberry Pi Fridge Monitoring System

A comprehensive monitoring system for tracking temperature, humidity, and door status for two fridges simultaneously. This application includes features for temperature graphing, door status tracking, maintenance scheduling, and automated alerts.

## Features

- Monitor two separate fridges with independent sensors
- Real-time temperature and humidity monitoring via DHT22 sensors
- Door status tracking with magnetic switches
- Compressor control via relay
- Detailed temperature graphs
- Door open duration alerts
- Temperature anomaly detection
- Annual maintenance reminders
- Automatic buzzer alerts for critical conditions
- Works in both simulation mode (for development) and real hardware mode

## Hardware Requirements

- Raspberry Pi (3 or 4 recommended)
- 2× DHT22 temperature/humidity sensors
- 2× Magnetic door switches
- 2× Relay modules (for compressor control)
- 1× Buzzer
- Jumper wires
- Breadboard (optional)

## Pin Configuration

Default pin assignments (BCM mode):

- **Buzzer**: Pin 17
- **Fridge 1**:
  - DHT22 sensor: Pin 4
  - Door sensor: Pin 17
  - Relay: Pin 18
- **Fridge 2**:
  - DHT22 sensor: Pin 22
  - Door sensor: Pin 23
  - Relay: Pin 24

You can modify these pin assignments in `config.py` if needed.

## Installation Instructions

### Step 1: Set up Raspberry Pi

1. Install Raspberry Pi OS (Lite or Desktop)
2. Ensure your Raspberry Pi has internet connectivity
3. Update system packages:
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

### Step 2: Connect Hardware

1. **DHT22 Sensors**:
   - Connect VCC to 3.3V or 5V (check sensor specifications)
   - Connect GND to ground
   - Connect data pin to GPIO 4 (fridge 1) and GPIO 22 (fridge 2)
   - Add a 10K pull-up resistor between VCC and data pin

2. **Door Sensors**:
   - Connect one end to ground
   - Connect the other end to GPIO 17 (fridge 1) and GPIO 23 (fridge 2)

3. **Relay Modules**:
   - Connect VCC to 5V
   - Connect GND to ground
   - Connect IN pins to GPIO 18 (fridge 1) and GPIO 24 (fridge 2)

4. **Buzzer**:
   - Connect positive pin to GPIO 17
   - Connect negative pin to ground

### Step 3: Install Required Software

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/fridge-monitor.git
   cd fridge-monitor
   ```

2. Install system dependencies:
   ```bash
   sudo apt install -y python3-pip python3-dev
   sudo apt install -y libgpiod2  # Required for GPIO access
   ```

3. Install Python dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

### Step 4: Configure the Application

1. Review and edit `config.py` if needed to adjust:
   - Temperature thresholds
   - Pin assignments
   - Alert durations
   - Data retention periods

2. Set up the database (SQLite by default):
   ```bash
   python3 -c "from app import db; db.create_all()"
   ```

### Step 5: Run the Application

1. Start the application:
   ```bash
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

2. Access the web interface:
   - On the Raspberry Pi: http://localhost:5000
   - From another device on the same network: http://raspberry_pi_ip:5000

### Step 6: Set Up Autostart (Optional)

To automatically start the application when the Raspberry Pi boots:

1. Create a systemd service:
   ```bash
   sudo nano /etc/systemd/system/fridge-monitor.service
   ```

2. Add the following content:
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

3. Enable and start the service:
   ```bash
   sudo systemctl enable fridge-monitor.service
   sudo systemctl start fridge-monitor.service
   ```

## Usage

### Dashboard

The main dashboard displays:
- Current temperature and humidity for each fridge
- Door status (open/closed)
- Recent temperature graphs
- Active alerts
- Maintenance status

### Settings

On the settings page, you can adjust:
- Target temperature
- Temperature thresholds
- Door open alert duration
- Maintenance interval
- Log maintenance activities

### Alerts

The system generates alerts for:
- Door left open too long
- Temperature too high or too low
- Rapid temperature increase (possible defrosting)
- Maintenance due

## Files and Directory Structure

- `main.py`: Application entry point
- `app.py`: Flask application setup
- `config.py`: Configuration settings
- `models.py`: Database models
- `routes.py`: Web route definitions
- `sensor_handlers.py`: Sensor interaction logic
- `hardware_controller.py`: Hardware setup and control
- `hardware_simulator.py`: Simulation for development
- `utils.py`: Utility functions
- `static/`: Static assets (CSS, JavaScript)
- `templates/`: HTML templates
- `instance/`: SQLite database location

## Troubleshooting

### Hardware Issues

- **DHT22 Sensor Not Reading**: Check wiring and ensure pull-up resistor is connected correctly.
- **Door Sensor Not Triggering**: Verify wiring and GPIO pin assignment.
- **Relay Not Switching**: Check relay wiring and GPIO pin assignment.

### Software Issues

- **Database Errors**: Delete the database file in `instance/` folder and restart to recreate it.
- **Permission Errors**: Ensure the application has GPIO access with `sudo` or adding the user to the `gpio` group.
- **App Not Starting**: Check logs with `journalctl -u fridge-monitor.service -f`.

## Maintenance

- Database cleanup is performed automatically to prevent excessive disk usage.
- Temperature readings are kept for 30 days (configurable in `config.py`).
- Door events are kept for 60 days.
- Alert history is kept for 90 days.

## License

[MIT License](LICENSE)

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Adafruit DHT Library](https://github.com/adafruit/Adafruit_Python_DHT)
- [Chart.js](https://www.chartjs.org/)
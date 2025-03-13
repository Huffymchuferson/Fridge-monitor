# Manual Installation Guide for Raspberry Pi Fridge Monitor

If you prefer not to use the automated installation script, you can follow these manual steps:

## 1. Install System Dependencies

```bash
sudo apt update
sudo apt install -y python3-pip python3-dev
sudo apt install -y libgpiod2 python3-libgpiod
sudo apt install -y git
```

## 2. Create Application Directory

```bash
sudo mkdir -p /home/pi/fridge-monitor
sudo chown pi:pi /home/pi/fridge-monitor
```

## 3. Install Python Packages

For newer Raspberry Pi OS versions (that show "externally managed environment" errors):

```bash
sudo pip3 install --break-system-packages adafruit-circuitpython-dht
sudo pip3 install --break-system-packages APScheduler
sudo pip3 install --break-system-packages email-validator
sudo pip3 install --break-system-packages Flask
sudo pip3 install --break-system-packages Flask-SQLAlchemy
sudo pip3 install --break-system-packages gunicorn
sudo pip3 install --break-system-packages psycopg2-binary
sudo pip3 install --break-system-packages RPi.GPIO
```

For older Raspberry Pi OS versions:

```bash
sudo pip3 install adafruit-circuitpython-dht
sudo pip3 install APScheduler
sudo pip3 install email-validator
sudo pip3 install Flask
sudo pip3 install Flask-SQLAlchemy
sudo pip3 install gunicorn
sudo pip3 install psycopg2-binary
sudo pip3 install RPi.GPIO
```

## 4. Copy Application Files

Extract the zip file and copy all contents to the application directory:

```bash
# Assuming you're in the directory where you extracted the zip
cp -r ./* /home/pi/fridge-monitor/
sudo chown -R pi:pi /home/pi/fridge-monitor
```

## 5. Create Systemd Service

Create a service file to run the application at startup:

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

## 6. Enable and Start the Service

```bash
sudo systemctl enable fridge-monitor.service
sudo systemctl start fridge-monitor.service
```

## 7. Set GPIO Permissions

```bash
sudo usermod -a -G gpio pi
```

## 8. Testing the Installation

You can test your hardware setup before running the full application:

```bash
cd /home/pi/fridge-monitor
python3 HARDWARE_TEST.py
```

## 9. Accessing the Application

The web interface will be available at:

```
http://[raspberry_pi_ip]:5000
```

## 10. Reboot

It's recommended to reboot after installation:

```bash
sudo reboot
```
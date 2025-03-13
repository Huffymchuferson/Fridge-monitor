#!/bin/bash

# Raspberry Pi Fridge Monitor Installation Script

# Exit on error
set -e

echo "======================================================="
echo "Raspberry Pi Fridge Monitoring System - Installer"
echo "======================================================="

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root. Try 'sudo ./install.sh'"
    exit 1
fi

# Check if Raspberry Pi
PI_MODEL=$(grep -c "Raspberry Pi" /proc/cpuinfo || echo "0")
if [ "$PI_MODEL" -eq 0 ]; then
    echo "This script is intended to run on a Raspberry Pi."
    echo "Continue anyway? (y/n)"
    read -r response
    if [[ ! "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]; then
        echo "Installation canceled."
        exit 0
    fi
fi

echo "Updating package lists..."
apt update

echo "Installing system dependencies..."
apt install -y python3-pip python3-dev
apt install -y libgpiod2 python3-libgpiod
apt install -y git

# Create app directory if it doesn't exist
APP_DIR="/home/pi/fridge-monitor"
if [ ! -d "$APP_DIR" ]; then
    echo "Creating application directory..."
    mkdir -p "$APP_DIR"
    # Set correct ownership
    chown pi:pi "$APP_DIR"
fi

echo "Installing Python dependencies..."

# Handle the "externally managed environment" issue in newer Raspberry Pi OS versions
if python3 -m pip install --break-system-packages 2>&1 | grep -q "break-system-packages"; then
    # Newer Raspberry Pi OS - use --break-system-packages flag
    echo "Detected newer Raspberry Pi OS with externally managed environment"
    pip3 install --break-system-packages adafruit-circuitpython-dht
    pip3 install --break-system-packages APScheduler
    pip3 install --break-system-packages email-validator
    pip3 install --break-system-packages Flask
    pip3 install --break-system-packages Flask-SQLAlchemy
    pip3 install --break-system-packages gunicorn
    pip3 install --break-system-packages psycopg2-binary
    pip3 install --break-system-packages RPi.GPIO
else
    # Older Raspberry Pi OS without this restriction
    echo "Using standard pip installation"
    pip3 install adafruit-circuitpython-dht
    pip3 install APScheduler
    pip3 install email-validator
    pip3 install Flask
    pip3 install Flask-SQLAlchemy
    pip3 install gunicorn
    pip3 install psycopg2-binary
    pip3 install RPi.GPIO
fi

# Copy files from current directory to app directory
echo "Copying application files..."
cp -r ./* "$APP_DIR/"
chown -R pi:pi "$APP_DIR"

# Create systemd service file
echo "Creating systemd service..."
cat > /etc/systemd/system/fridge-monitor.service << EOL
[Unit]
Description=Fridge Monitoring System
After=network.target

[Service]
User=pi
WorkingDirectory=$APP_DIR
ExecStart=/usr/local/bin/gunicorn --bind 0.0.0.0:5000 --reuse-port main:app
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Enable and start the service
echo "Enabling and starting service..."
systemctl enable fridge-monitor.service
systemctl start fridge-monitor.service

echo "======================================================="
echo "Installation complete!"
echo "The fridge monitoring system is now running."
echo "You can access it in your browser at http://$(hostname -I | awk '{print $1}'):5000"
echo "======================================================="

# Add pi user to gpio group for permissions
usermod -a -G gpio pi
echo "Note: A reboot may be required for permission changes to take effect."
echo "Would you like to reboot now? (y/n)"
read -r reboot_response
if [[ "$reboot_response" =~ ^([yY][eE][sS]|[yY])+$ ]]; then
    echo "Rebooting system..."
    reboot
else
    echo "Please reboot your system later to ensure all changes take effect."
fi
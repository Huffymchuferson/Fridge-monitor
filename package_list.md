# Required Packages for Fridge Monitoring System

When setting up the system on your Raspberry Pi, you'll need to install the following Python packages:

```
adafruit-circuitpython-dht==3.7.8
APScheduler==3.10.1
email-validator==2.0.0
Flask==2.3.3
Flask-SQLAlchemy==3.1.1
gunicorn==23.0.0
psycopg2-binary==2.9.7
RPi.GPIO==0.7.1
SQLAlchemy==2.0.20
```

You can install these packages using pip:

```bash
pip3 install -r package_list.txt
```

Or install each package individually:

```bash
pip3 install adafruit-circuitpython-dht APScheduler email-validator Flask Flask-SQLAlchemy gunicorn psycopg2-binary RPi.GPIO SQLAlchemy
```

## System Dependencies

You may also need to install some system dependencies:

```bash
sudo apt update
sudo apt install -y python3-pip python3-dev
sudo apt install -y libgpiod2
```

For the Adafruit DHT library to work properly, you might need these additional dependencies:

```bash
sudo apt install -y libgpiod2 python3-libgpiod
```
# Raspberry Pi Fridge Monitor - Package Contents

This document lists all the files in this package and their purpose.

## Documentation Files

| File | Description |
|------|-------------|
| README.md | Main documentation with overview and features |
| GETTING_STARTED.md | Guide for using the system after installation |
| RASPBERRY_PI_SETUP.md | Detailed setup instructions for Raspberry Pi |
| PINOUT_REFERENCE.md | GPIO pin reference and wiring guide |
| PACKAGE_CONTENTS.md | This file - lists all package contents |
| package_list.md | List of required Python packages |

## Core Application Files

| File | Description |
|------|-------------|
| app.py | Flask application initialization and database setup |
| config.py | Configuration settings (pin assignments, thresholds, etc.) |
| hardware_controller.py | Hardware setup and monitoring logic |
| hardware_simulator.py | Simulation environment for non-Raspberry Pi usage |
| main.py | Application entry point |
| models.py | Database models (Fridge, TemperatureReading, etc.) |
| routes.py | Web route definitions and HTTP handlers |
| sensor_handlers.py | Sensor interaction and alert generation logic |
| utils.py | Utility functions (data cleanup, statistics, etc.) |

## Templates and Static Files

| Directory | Description |
|-----------|-------------|
| templates/ | HTML templates for the web interface |
| static/css/ | CSS stylesheets |
| static/js/ | JavaScript files for client-side functionality |

## Raspberry Pi Version

| Directory | Description |
|-----------|-------------|
| raspberry_pi_version/ | Contains files specifically for Raspberry Pi hardware |

## Utility Scripts

| File | Description |
|------|-------------|
| install.sh | Installation script for Raspberry Pi |
| HARDWARE_TEST.py | Script to test hardware components individually |

## Database

| Directory | Description |
|-----------|-------------|
| instance/ | Contains the SQLite database file |

## How to Use This Package

1. Read the README.md file first for an overview
2. Follow RASPBERRY_PI_SETUP.md for installation instructions
3. Use PINOUT_REFERENCE.md to connect your hardware
4. Run HARDWARE_TEST.py to verify hardware connections
5. Start the application using the instructions in README.md
6. Use GETTING_STARTED.md to learn how to use the system
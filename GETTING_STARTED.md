# Getting Started with Raspberry Pi Fridge Monitor

This guide will help you get started with your new Raspberry Pi Fridge Monitoring System. It covers the basic usage and features to help you understand how to make the most of your system.

## First-time Login

1. Once you've installed the system following the instructions in `RASPBERRY_PI_SETUP.md`, open a web browser.
2. Navigate to `http://[raspberry_pi_ip]:5000` (replace [raspberry_pi_ip] with your Raspberry Pi's IP address).
3. You'll be taken to the main dashboard showing your fridges.

## Dashboard Overview

The main dashboard displays:

![Dashboard Overview](https://i.imgur.com/YZfDpWT.png)

1. **Fridge Cards**: Each monitored fridge has its own card showing:
   - Current temperature
   - Current humidity
   - Door status (open/closed)
   - Compressor status (on/off)
   - Days until maintenance

2. **Alert Notifications**: Any active alerts will appear at the top of the dashboard.

3. **Navigation**: Use the navigation menu to access:
   - Dashboard (Home)
   - Fridge Details (click on any fridge card)
   - Settings

## Fridge Details

Click on any fridge card to see detailed information:

1. **Temperature Graph**: Shows temperature and humidity over time.
2. **Door Activity**: Shows door opening events and durations.
3. **Alerts**: Lists all alerts for this fridge.
4. **Statistics**: 
   - Average temperature
   - Door openings today
   - Average door open time
   - Recovery time (time to reach target temp after door close)

## Settings Page

The settings page allows you to configure each fridge:

1. **Fridge Settings**:
   - Name and description
   - Target temperature
   - Temperature thresholds (min/max)
   - Door open alert time
   - Maintenance interval

2. **Maintenance**:
   - Log maintenance activities
   - Reset maintenance date

## Managing Alerts

1. **Types of Alerts**:
   - **Door Open**: Door has been open too long
   - **Temperature High/Low**: Temperature is outside set thresholds
   - **Defrosting**: Rapid temperature increase detected
   - **Maintenance Due**: Annual maintenance reminder

2. **Acknowledging Alerts**:
   - Click the "Acknowledge" button next to any alert to dismiss it
   - The alert will be archived but still viewable in history

## Mobile Access

The web interface is mobile-responsive. You can bookmark the URL on your phone or tablet for easy access.

## What to Do When...

### Temperature is Too High

1. Check if the door is properly closed
2. Verify the compressor is running (status shown on dashboard)
3. Check if the fridge is in a defrost cycle
4. Reduce the target temperature in settings if needed

### Door Open Alert

1. Close the door
2. The alert will automatically clear
3. If false alarms occur, increase the door open alert time in settings

### Maintenance Due Alert

1. Perform recommended maintenance:
   - Clean condenser coils
   - Check door seals
   - Verify temperature accuracy with external thermometer
2. Log the maintenance activity in the settings page
3. The maintenance timer will reset

## Troubleshooting

### Sensor Readings Not Updating

1. Check if the application is running: `sudo systemctl status fridge-monitor.service`
2. Restart the service if needed: `sudo systemctl restart fridge-monitor.service`
3. Check wiring connections to the DHT22 sensors

### Door Status Incorrect

1. Check the magnetic sensor alignment
2. Verify wiring connections
3. Test the sensor using the included test script

### System Not Starting

If the system doesn't start properly, check the logs:
```bash
sudo journalctl -u fridge-monitor.service -f
```

## Maintenance Tips

1. **Regular Cleaning**: Keep sensors and relay contacts clean.
2. **Backup Database**: Periodically backup the SQLite database in the `instance` folder.
3. **Check Logs**: Review system logs occasionally to ensure everything is working properly.

## Customization

The system can be customized by editing files directly:

1. **Visual Theme**: Edit `static/css/style.css`
2. **Chart Settings**: Modify `static/js/chart_handler.js`
3. **System Configuration**: Update `config.py`
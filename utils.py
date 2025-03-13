import logging
from datetime import datetime, timedelta
from app import db
from models import Fridge, TemperatureReading, DoorEvent, Alert

logger = logging.getLogger(__name__)

def cleanup_old_data():
    """Remove old readings to keep the database size manageable"""
    try:
        # Keep temperature readings for 30 days
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        
        # Delete old temperature readings
        deleted_temp = db.session.query(TemperatureReading).filter(
            TemperatureReading.timestamp < cutoff_date
        ).delete()
        
        # Keep door events for 60 days
        cutoff_date = datetime.utcnow() - timedelta(days=60)
        deleted_door = db.session.query(DoorEvent).filter(
            DoorEvent.timestamp < cutoff_date
        ).delete()
        
        # Keep acknowledged alerts for 90 days
        cutoff_date = datetime.utcnow() - timedelta(days=90)
        deleted_alerts = db.session.query(Alert).filter(
            Alert.acknowledged == True,
            Alert.timestamp < cutoff_date
        ).delete()
        
        db.session.commit()
        
        logger.info(f"Cleanup complete: Removed {deleted_temp} temperature readings, "
                   f"{deleted_door} door events, and {deleted_alerts} acknowledged alerts")
        
    except Exception as e:
        logger.error(f"Error during data cleanup: {e}")
        db.session.rollback()

def get_temperature_data(fridge_id, days=1):
    """Get temperature data for charts"""
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        readings = TemperatureReading.query.filter(
            TemperatureReading.fridge_id == fridge_id,
            TemperatureReading.timestamp > cutoff_date
        ).order_by(TemperatureReading.timestamp.asc()).all()
        
        timestamps = [reading.timestamp.strftime('%Y-%m-%d %H:%M:%S') for reading in readings]
        temperatures = [round(reading.temperature, 1) for reading in readings]
        humidities = [round(reading.humidity, 1) for reading in readings]
        
        return {
            'timestamps': timestamps,
            'temperatures': temperatures,
            'humidities': humidities
        }
    except Exception as e:
        logger.error(f"Error getting temperature data: {e}")
        return {
            'timestamps': [],
            'temperatures': [],
            'humidities': []
        }

def get_door_events(fridge_id, days=1):
    """Get door events for the specified number of days"""
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        events = DoorEvent.query.filter(
            DoorEvent.fridge_id == fridge_id,
            DoorEvent.timestamp > cutoff_date
        ).order_by(DoorEvent.timestamp.asc()).all()
        
        return events
    except Exception as e:
        logger.error(f"Error getting door events: {e}")
        return []

def calculate_daily_stats(fridge_id):
    """Calculate daily statistics for a fridge"""
    today = datetime.utcnow().date()
    
    # Get door open count
    door_open_count = DoorEvent.query.filter(
        DoorEvent.fridge_id == fridge_id,
        DoorEvent.event_type == 'open',
        db.func.date(DoorEvent.timestamp) == today
    ).count()
    
    # Get average temperature for today
    today_readings = TemperatureReading.query.filter(
        TemperatureReading.fridge_id == fridge_id,
        db.func.date(TemperatureReading.timestamp) == today
    ).all()
    
    avg_temp = sum(reading.temperature for reading in today_readings) / len(today_readings) if today_readings else None
    avg_humidity = sum(reading.humidity for reading in today_readings) / len(today_readings) if today_readings else None
    
    # Calculate average recovery time
    recovery_times = []
    door_close_events = DoorEvent.query.filter(
        DoorEvent.fridge_id == fridge_id,
        DoorEvent.event_type == 'close',
        db.func.date(DoorEvent.timestamp) == today
    ).order_by(DoorEvent.timestamp.asc()).all()
    
    fridge = db.session.query(Fridge).get(fridge_id)
    target_temp = fridge.target_temp if fridge else 4.0
    
    for event in door_close_events:
        # Find the next temperature reading that is at or below the target
        recovery_reading = TemperatureReading.query.filter(
            TemperatureReading.fridge_id == fridge_id,
            TemperatureReading.temperature <= target_temp,
            TemperatureReading.timestamp > event.timestamp
        ).order_by(TemperatureReading.timestamp.asc()).first()
        
        if recovery_reading:
            recovery_time = (recovery_reading.timestamp - event.timestamp).total_seconds()
            recovery_times.append(recovery_time)
    
    avg_recovery_time = sum(recovery_times) / len(recovery_times) if recovery_times else None
    
    return {
        'door_open_count': door_open_count,
        'avg_temp': round(avg_temp, 1) if avg_temp is not None else None,
        'avg_humidity': round(avg_humidity, 1) if avg_humidity is not None else None,
        'avg_recovery_time': round(avg_recovery_time, 0) if avg_recovery_time is not None else None
    }

def acknowledge_alert(alert_id):
    """Mark an alert as acknowledged"""
    try:
        alert = Alert.query.get(alert_id)
        if alert:
            alert.acknowledged = True
            db.session.commit()
            return True
        return False
    except Exception as e:
        logger.error(f"Error acknowledging alert: {e}")
        db.session.rollback()
        return False

def log_maintenance(fridge_id, description, performed_by):
    """Log a maintenance record for a fridge"""
    from models import MaintenanceRecord, Fridge
    
    try:
        # Create maintenance record
        record = MaintenanceRecord(
            fridge_id=fridge_id,
            description=description,
            performed_by=performed_by,
            maintenance_date=datetime.utcnow()
        )
        
        # Update fridge's last maintenance date
        fridge = Fridge.query.get(fridge_id)
        if fridge:
            fridge.last_maintenance_date = datetime.utcnow()
            
            # Clear any maintenance due alerts
            alerts = Alert.query.filter_by(
                fridge_id=fridge_id,
                alert_type='maintenance_due',
                acknowledged=False
            ).all()
            
            for alert in alerts:
                alert.acknowledged = True
        
        db.session.add(record)
        db.session.commit()
        
        return True
    except Exception as e:
        logger.error(f"Error logging maintenance: {e}")
        db.session.rollback()
        return False

def reset_maintenance_date(fridge_id):
    """Reset the maintenance date for a fridge without creating a maintenance record"""
    from models import Fridge
    
    try:
        # Get the fridge
        fridge = Fridge.query.get(fridge_id)
        if fridge:
            # Update the last maintenance date
            fridge.last_maintenance_date = datetime.utcnow()
            
            # Clear any maintenance due alerts
            alerts = Alert.query.filter_by(
                fridge_id=fridge_id,
                alert_type='maintenance_due',
                acknowledged=False
            ).all()
            
            for alert in alerts:
                alert.acknowledged = True
                
            db.session.commit()
            return True
        return False
    except Exception as e:
        logger.error(f"Error resetting maintenance date: {e}")
        db.session.rollback()
        return False
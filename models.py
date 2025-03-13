from datetime import datetime
from app import db

class Fridge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(255))
    target_temp = db.Column(db.Float, default=4.0)  # Default target temp in Celsius
    min_temp_threshold = db.Column(db.Float, default=2.0)
    max_temp_threshold = db.Column(db.Float, default=8.0)
    door_open_alert_seconds = db.Column(db.Integer, default=60)  # Alert after 60 seconds
    compressor_status = db.Column(db.Boolean, default=False)
    maintenance_interval_days = db.Column(db.Integer, default=365)  # Annual maintenance by default
    last_maintenance_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Hardware configuration
    dht22_pin = db.Column(db.Integer, nullable=False)
    door_sensor_pin = db.Column(db.Integer, nullable=False)
    relay_pin = db.Column(db.Integer, nullable=False)
    
    # Relationships
    temperature_readings = db.relationship('TemperatureReading', backref='fridge', lazy=True, cascade="all, delete-orphan")
    door_events = db.relationship('DoorEvent', backref='fridge', lazy=True, cascade="all, delete-orphan")
    maintenance_records = db.relationship('MaintenanceRecord', backref='fridge', lazy=True, cascade="all, delete-orphan")
    alerts = db.relationship('Alert', backref='fridge', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Fridge {self.name}>'
    
    def get_today_door_openings(self):
        """Return count of door openings for today"""
        today = datetime.utcnow().date()
        return DoorEvent.query.filter(
            DoorEvent.fridge_id == self.id,
            DoorEvent.event_type == 'open',
            db.func.date(DoorEvent.timestamp) == today
        ).count()
    
    def is_door_open(self):
        """Determine if the door is currently open based on most recent door event"""
        latest_event = DoorEvent.query.filter_by(
            fridge_id=self.id
        ).order_by(DoorEvent.timestamp.desc()).first()
        
        if latest_event:
            return latest_event.event_type == 'open'
        return False
    
    def get_current_reading(self):
        """Get the most recent temperature reading"""
        return TemperatureReading.query.filter_by(
            fridge_id=self.id
        ).order_by(TemperatureReading.timestamp.desc()).first()
    
    def get_last_recovery_time(self):
        """Calculate the most recent recovery time (time to reach target temp after door close)"""
        # Find the most recent door close event
        last_door_close = DoorEvent.query.filter_by(
            fridge_id=self.id, 
            event_type='close'
        ).order_by(DoorEvent.timestamp.desc()).first()
        
        if not last_door_close:
            return None
        
        # Find the next temperature reading at or below target after door close
        recovery_reading = TemperatureReading.query.filter(
            TemperatureReading.fridge_id == self.id,
            TemperatureReading.temperature <= self.target_temp,
            TemperatureReading.timestamp > last_door_close.timestamp
        ).order_by(TemperatureReading.timestamp.asc()).first()
        
        if not recovery_reading:
            return None
            
        # Calculate recovery time in seconds
        recovery_time = (recovery_reading.timestamp - last_door_close.timestamp).total_seconds()
        return recovery_time
    
    def days_until_maintenance(self):
        """Calculate days until next maintenance is due"""
        if not self.last_maintenance_date:
            return 0
            
        next_maintenance = self.last_maintenance_date.replace(
            year=self.last_maintenance_date.year + (self.maintenance_interval_days // 365),
            day=self.last_maintenance_date.day,
            month=self.last_maintenance_date.month
        )
        days_remaining = (next_maintenance - datetime.utcnow()).days
        return max(0, days_remaining)


class TemperatureReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fridge_id = db.Column(db.Integer, db.ForeignKey('fridge.id'), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TemperatureReading {self.temperature}°C, {self.humidity}% at {self.timestamp}>'


class DoorEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fridge_id = db.Column(db.Integer, db.ForeignKey('fridge.id'), nullable=False)
    event_type = db.Column(db.String(10), nullable=False)  # 'open' or 'close'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DoorEvent {self.event_type} at {self.timestamp}>'


class MaintenanceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fridge_id = db.Column(db.Integer, db.ForeignKey('fridge.id'), nullable=False)
    maintenance_date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text)
    performed_by = db.Column(db.String(64))
    
    def __repr__(self):
        return f'<MaintenanceRecord {self.maintenance_date}>'


class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fridge_id = db.Column(db.Integer, db.ForeignKey('fridge.id'), nullable=False)
    alert_type = db.Column(db.String(32), nullable=False)  # 'door_open', 'temp_high', 'temp_low', 'maintenance_due', 'defrosting'
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    acknowledged = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Alert {self.alert_type}: {self.message}>'

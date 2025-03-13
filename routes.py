import logging
from datetime import datetime

from flask import render_template, request, jsonify, redirect, url_for, flash

from app import db
from models import Fridge, Alert, MaintenanceRecord
from utils import (
    get_temperature_data, calculate_daily_stats, 
    acknowledge_alert, log_maintenance, reset_maintenance_date
)

logger = logging.getLogger(__name__)

def register_routes(app):
    @app.route('/')
    def index():
        """Main dashboard showing all fridges"""
        fridges = Fridge.query.all()
        
        # Get current readings and status for each fridge
        fridge_data = []
        for fridge in fridges:
            # Get current temperature reading
            current_reading = fridge.get_current_reading()
            
            # Get daily stats
            stats = calculate_daily_stats(fridge.id)
            
            # Check if maintenance is due
            days_until_maintenance = fridge.days_until_maintenance()
            
            # Get active alerts
            active_alerts = Alert.query.filter_by(
                fridge_id=fridge.id,
                acknowledged=False
            ).order_by(Alert.timestamp.desc()).all()
            
            # Is door currently open?
            door_open = fridge.is_door_open()
            
            # Add fridge data
            fridge_data.append({
                'fridge': fridge,
                'current_reading': current_reading,
                'stats': stats,
                'days_until_maintenance': days_until_maintenance,
                'active_alerts': active_alerts,
                'door_open': door_open
            })
        
        return render_template('index.html', fridge_data=fridge_data)

    @app.route('/fridge/<int:fridge_id>')
    def fridge_detail(fridge_id):
        """Detailed view for a specific fridge"""
        fridge = Fridge.query.get_or_404(fridge_id)
        
        # Get current reading
        current_reading = fridge.get_current_reading()
        
        # Get temperature data for charts (default: 1 day)
        duration = request.args.get('duration', '1')
        try:
            duration = int(duration)
        except ValueError:
            duration = 1
        
        temp_data = get_temperature_data(fridge_id, days=duration)
        
        # Get daily stats
        stats = calculate_daily_stats(fridge_id)
        
        # Get maintenance history
        maintenance_history = MaintenanceRecord.query.filter_by(
            fridge_id=fridge_id
        ).order_by(MaintenanceRecord.maintenance_date.desc()).all()
        
        # Get active alerts
        active_alerts = Alert.query.filter_by(
            fridge_id=fridge_id,
            acknowledged=False
        ).order_by(Alert.timestamp.desc()).all()
        
        # Get recent alerts (last 10)
        recent_alerts = Alert.query.filter_by(
            fridge_id=fridge_id
        ).order_by(Alert.timestamp.desc()).limit(10).all()
        
        # Door open status
        door_open = fridge.is_door_open()
        
        # Recovery time
        recovery_time = fridge.get_last_recovery_time()
        
        return render_template(
            'fridge_detail.html',
            fridge=fridge,
            current_reading=current_reading,
            temp_data=temp_data,
            stats=stats,
            maintenance_history=maintenance_history,
            active_alerts=active_alerts,
            recent_alerts=recent_alerts,
            door_open=door_open,
            recovery_time=recovery_time,
            duration=duration
        )

    @app.route('/settings')
    def settings():
        """Settings page for all fridges"""
        fridges = Fridge.query.all()
        return render_template('settings.html', fridges=fridges)

    @app.route('/update_fridge/<int:fridge_id>', methods=['POST'])
    def update_fridge(fridge_id):
        """Update fridge settings"""
        fridge = Fridge.query.get_or_404(fridge_id)
        
        try:
            # Update basic info
            fridge.name = request.form.get('name', fridge.name)
            fridge.description = request.form.get('description', fridge.description)
            
            # Update temperature settings
            fridge.target_temp = float(request.form.get('target_temp', fridge.target_temp))
            fridge.min_temp_threshold = float(request.form.get('min_temp_threshold', fridge.min_temp_threshold))
            fridge.max_temp_threshold = float(request.form.get('max_temp_threshold', fridge.max_temp_threshold))
            
            # Update alert settings
            fridge.door_open_alert_seconds = int(request.form.get('door_open_alert_seconds', fridge.door_open_alert_seconds))
            
            # Update maintenance settings
            fridge.maintenance_interval_days = int(request.form.get('maintenance_interval_days', fridge.maintenance_interval_days))
            
            # Update hardware pins (be careful with this)
            fridge.dht22_pin = int(request.form.get('dht22_pin', fridge.dht22_pin))
            fridge.door_sensor_pin = int(request.form.get('door_sensor_pin', fridge.door_sensor_pin))
            fridge.relay_pin = int(request.form.get('relay_pin', fridge.relay_pin))
            
            db.session.commit()
            flash('Fridge settings updated successfully', 'success')
            
            # Note: Changing pins requires restarting the application to take effect
            if (int(request.form.get('dht22_pin')) != fridge.dht22_pin or
                int(request.form.get('door_sensor_pin')) != fridge.door_sensor_pin or
                int(request.form.get('relay_pin')) != fridge.relay_pin):
                flash('Hardware pin changes require restarting the application to take effect', 'warning')
                
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating fridge: {e}")
            flash(f'Error updating fridge: {str(e)}', 'danger')
        
        return redirect(url_for('settings'))

    @app.route('/log_maintenance/<int:fridge_id>', methods=['POST'])
    def log_maintenance_route(fridge_id):
        """Log maintenance for a fridge"""
        description = request.form.get('description', '')
        performed_by = request.form.get('performed_by', '')
        
        success = log_maintenance(fridge_id, description, performed_by)
        
        if success:
            flash('Maintenance logged successfully', 'success')
        else:
            flash('Error logging maintenance', 'danger')
        
        return redirect(url_for('fridge_detail', fridge_id=fridge_id))

    @app.route('/acknowledge_alert/<int:alert_id>')
    def acknowledge_alert_route(alert_id):
        """Acknowledge an alert"""
        alert = Alert.query.get_or_404(alert_id)
        fridge_id = alert.fridge_id
        
        success = acknowledge_alert(alert_id)
        
        if success:
            flash('Alert acknowledged', 'success')
        else:
            flash('Error acknowledging alert', 'danger')
        
        return redirect(request.referrer or url_for('fridge_detail', fridge_id=fridge_id))

    @app.route('/api/temperature_data/<int:fridge_id>')
    def api_temperature_data(fridge_id):
        """API endpoint to get temperature data for charts"""
        days = request.args.get('days', '1')
        try:
            days = int(days)
        except ValueError:
            days = 1
            
        data = get_temperature_data(fridge_id, days=days)
        return jsonify(data)

    @app.route('/api/stats/<int:fridge_id>')
    def api_stats(fridge_id):
        """API endpoint to get current stats"""
        stats = calculate_daily_stats(fridge_id)
        fridge = Fridge.query.get_or_404(fridge_id)
        current_reading = fridge.get_current_reading()
        
        if current_reading:
            stats['current_temp'] = round(current_reading.temperature, 1)
            stats['current_humidity'] = round(current_reading.humidity, 1)
        else:
            stats['current_temp'] = None
            stats['current_humidity'] = None
            
        stats['door_open'] = fridge.is_door_open()
        stats['compressor_status'] = fridge.compressor_status
        
        return jsonify(stats)

    @app.route('/api/alerts/<int:fridge_id>')
    def api_alerts(fridge_id):
        """API endpoint to get active alerts"""
        active_alerts = Alert.query.filter_by(
            fridge_id=fridge_id,
            acknowledged=False
        ).order_by(Alert.timestamp.desc()).all()
        
        alerts_data = [{
            'id': alert.id,
            'type': alert.alert_type,
            'message': alert.message,
            'timestamp': alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        } for alert in active_alerts]
        
        return jsonify(alerts_data)

    @app.route('/reset_maintenance/<int:fridge_id>', methods=['POST'])
    def reset_maintenance_route(fridge_id):
        """Reset maintenance date for a fridge without logging a maintenance record"""
        fridge = Fridge.query.get_or_404(fridge_id)
        
        success = reset_maintenance_date(fridge_id)
        
        if success:
            flash('Maintenance date reset successfully', 'success')
        else:
            flash('Error resetting maintenance date', 'danger')
        
        return redirect(url_for('settings'))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

import os
import logging
import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from apscheduler.schedulers.background import BackgroundScheduler

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

# Initialize database
db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///fridge_monitor.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with the extension
db.init_app(app)

# Create scheduler for periodic tasks
scheduler = BackgroundScheduler()

with app.app_context():
    # Import models to ensure they're registered with SQLAlchemy
    from models import Fridge, TemperatureReading, DoorEvent, MaintenanceRecord, Alert
    
    # Create tables
    db.create_all()
    logger.info("Database tables created")
    
    # Custom Jinja filters
    @app.template_filter('now')
    def filter_now(format_string):
        return datetime.datetime.now().strftime(format_string)
        
    # Register now("year") filter to get current year
    app.jinja_env.globals.update(year=lambda: datetime.datetime.now().year)
    
    # Import and register blueprints/routes after models to avoid circular imports
    from routes import register_routes
    register_routes(app)
    
    # Import hardware controllers
    from hardware_controller import setup_hardware_monitoring
    
    # Set up hardware monitoring in a background thread
    setup_hardware_monitoring(app, scheduler)
    
    # Start the scheduler
    if not scheduler.running:
        scheduler.start()
        logger.info("Background scheduler started")

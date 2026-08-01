import os

class Config:
    # Key for signing sessions and flash messages
    SECRET_KEY = os.environ.get('SECRET_KEY', 'smart_college_secret_key_129847')
    
    # Local MySQL Configuration (Targeted for phpMyAdmin / XAMPP control panel)
    # Default phpMyAdmin credentials: Username='root', Password='' (none)
    # Target Database name: scas_db
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        'mysql+pymysql://root:@localhost/scas_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AI Risk Prediction constants
    ATTENDANCE_WARNING_THRESHOLD = 75.0  # in percentage

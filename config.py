import os

class Config:
    # Key for signing sessions and flash messages
    SECRET_KEY = os.environ.get('SECRET_KEY', 'smart_college_secret_key_129847')
    
    # Define connection strings
    MYSQL_URI = 'mysql+pymysql://root:@localhost/scas_db'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', MYSQL_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SMTP Email Configuration (overridden by environment variables if set)
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    SMTP_USER = os.environ.get('SMTP_USER', 'your-email@gmail.com')
    SMTP_PASS = os.environ.get('SMTP_PASS', 'your-app-password')
    
    # AI Risk Prediction constants
    ATTENDANCE_WARNING_THRESHOLD = 75.0  # in percentage

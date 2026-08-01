import os

class Config:
    # Key for signing sessions and flash messages
    SECRET_KEY = os.environ.get('SECRET_KEY', 'smart_college_secret_key_129847')
    
    # SQLite Database Configuration (Temporary for local generation)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AI Risk Prediction constants
    ATTENDANCE_WARNING_THRESHOLD = 75.0  # in percentage

import os
import socket

class Config:
    # Key for signing sessions and flash messages
    SECRET_KEY = os.environ.get('SECRET_KEY', 'smart_college_secret_key_129847')
    
    # Define connection strings
    MYSQL_URI = 'mysql+pymysql://root:@localhost/scas_db'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLITE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
    
    # Check if MySQL server is listening on port 3306
    use_mysql = False
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5) # Fast 500ms timeout
        s.connect(('localhost', 3306))
        s.close()
        use_mysql = True
    except Exception:
        pass
        
    if use_mysql:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', MYSQL_URI)
        print("\nSCAS ENGINE: Local MySQL server detected. Running database on MySQL (phpMyAdmin).\n")
    else:
        SQLALCHEMY_DATABASE_URI = SQLITE_URI
        print("\nSCAS ENGINE WARNING: MySQL server not running on localhost:3306. Falling back to SQLite database.\n")
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AI Risk Prediction constants
    ATTENDANCE_WARNING_THRESHOLD = 75.0  # in percentage

import os

# Load .env if present
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                os.environ[key.strip()] = val.strip().strip("'").strip('"')

class Config:
    # Key for signing sessions and flash messages
    SECRET_KEY = os.environ.get('SECRET_KEY', 'smart_college_secret_key_129847')
    
    # Define connection strings
    MYSQL_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:@localhost:3306/scas_db')
    SQLITE_URI = 'sqlite:///scas.db'
    
    # Check if local MySQL server is active on localhost:3306; auto-start XAMPP if present
    xampp_mysqld = r"C:\xampp\mysql\bin\mysqld.exe"
    mysql_ready = False
    try:
        import pymysql
        conn = pymysql.connect(host='localhost', user='root', password='', port=3306, connect_timeout=1)
        with conn.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS `scas_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.commit()
        conn.close()
        mysql_ready = True
    except Exception:
        # Try auto-starting XAMPP MySQL if binary exists
        if os.path.exists(xampp_mysqld):
            try:
                import subprocess, time
                flags = 0x08000000 if os.name == 'nt' else 0  # CREATE_NO_WINDOW
                subprocess.Popen(
                    [xampp_mysqld, '--defaults-file=C:\\xampp\\mysql\\bin\\my.ini', '--basedir=C:\\xampp\\mysql', '--datadir=C:\\xampp\\mysql\\data', '--standalone'],
                    creationflags=flags
                )
                time.sleep(2.5)
                import pymysql
                conn = pymysql.connect(host='localhost', user='root', password='', port=3306, connect_timeout=2)
                with conn.cursor() as cursor:
                    cursor.execute("CREATE DATABASE IF NOT EXISTS `scas_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
                conn.commit()
                conn.close()
                mysql_ready = True
            except Exception:
                mysql_ready = False

    if mysql_ready:
        SQLALCHEMY_DATABASE_URI = MYSQL_URI
    else:
        SQLALCHEMY_DATABASE_URI = SQLITE_URI
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SMTP Email Configuration (overridden by environment variables if set)
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    SMTP_USER = os.environ.get('SMTP_USER', 'your-email@gmail.com')
    SMTP_PASS = os.environ.get('SMTP_PASS', 'your-app-password')
    
    # AI Risk Prediction constants
    ATTENDANCE_WARNING_THRESHOLD = 75.0  # in percentage

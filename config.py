import os

# Load .env if present (without overwriting existing environment variables)
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                k = key.strip()
                if k not in os.environ:
                    os.environ[k] = val.strip().strip("'").strip('"')

class Config:
    # Key for signing sessions and flash messages
    SECRET_KEY = os.environ.get('SECRET_KEY', 'smart_college_secret_key_129847')
    
    # Database connection resolution
    env_db = os.environ.get('DATABASE_URL') or os.environ.get('SQLALCHEMY_DATABASE_URI')
    is_vercel = bool(os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME'))
    
    # On Vercel serverless containers, localhost cannot be reached; ignore localhost DATABASE_URL
    if is_vercel and env_db and ('localhost' in env_db or '127.0.0.1' in env_db):
        env_db = None
    
    if env_db:
        # Standardize postgres:// to postgresql:// for SQLAlchemy 1.4/2.0+
        if env_db.startswith('postgres://'):
            env_db = env_db.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = env_db
    elif is_vercel:
        # On Vercel serverless environment without remote DB, use writable /tmp SQLite
        SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/scas.db'
    else:
        # Local development environment
        local_mysql_uri = 'mysql+pymysql://root:@localhost:3306/scas_db'
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
            SQLALCHEMY_DATABASE_URI = local_mysql_uri
        else:
            local_db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'scas.db')
            SQLALCHEMY_DATABASE_URI = f'sqlite:///{local_db_path}'
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SMTP Email Configuration (overridden by environment variables if set)
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    SMTP_USER = os.environ.get('SMTP_USER', 'your-email@gmail.com')
    SMTP_PASS = os.environ.get('SMTP_PASS', 'your-app-password')
    
    # AI Risk Prediction constants
    ATTENDANCE_WARNING_THRESHOLD = 75.0  # in percentage

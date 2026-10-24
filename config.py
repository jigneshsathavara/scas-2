import os
import tempfile

# Detect serverless environment (Vercel, AWS Lambda, or read-only container)
is_serverless = bool(
    os.environ.get('VERCEL') or 
    os.environ.get('VERCEL_ENV') or 
    os.environ.get('AWS_LAMBDA_FUNCTION_NAME') or 
    os.environ.get('LAMBDA_TASK_ROOT') or
    not os.access(os.path.dirname(os.path.abspath(__file__)), os.W_OK)
)

# Load local .env only in local environment
if not is_serverless:
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
    
    # Serverless flag
    IS_SERVERLESS = is_serverless
    
    # Database connection resolution
    raw_db = (
        os.environ.get('DATABASE_URL') or 
        os.environ.get('POSTGRES_URL') or 
        os.environ.get('POSTGRES_PRISMA_URL') or 
        os.environ.get('POSTGRES_URL_NON_POOLING') or 
        os.environ.get('MYSQL_URL') or 
        os.environ.get('SQLALCHEMY_DATABASE_URI')
    )
    
    # On Vercel/serverless containers, localhost cannot be reached; ignore localhost DATABASE_URL
    if is_serverless and raw_db and ('localhost' in raw_db or '127.0.0.1' in raw_db):
        raw_db = None
    
    # In local development, if localhost MySQL is specified, check if it's reachable or start XAMPP
    if raw_db and ('localhost' in raw_db or '127.0.0.1' in raw_db) and not is_serverless:
        mysql_reachable = False
        try:
            import pymysql
            conn = pymysql.connect(host='localhost', user='root', password='', port=3306, connect_timeout=1)
            conn.close()
            mysql_reachable = True
        except Exception:
            # Check if XAMPP MySQL binary exists to attempt startup
            xampp_mysqld = r"C:\xampp\mysql\bin\mysqld.exe"
            if os.path.exists(xampp_mysqld):
                try:
                    import subprocess, time
                    flags = 0x08000000 if os.name == 'nt' else 0
                    subprocess.Popen(
                        [xampp_mysqld, '--defaults-file=C:\\xampp\\mysql\\bin\\my.ini', '--basedir=C:\\xampp\\mysql', '--datadir=C:\\xampp\\mysql\\data', '--standalone'],
                        creationflags=flags
                    )
                    time.sleep(2)
                    conn = pymysql.connect(host='localhost', user='root', password='', port=3306, connect_timeout=1)
                    conn.close()
                    mysql_reachable = True
                except Exception:
                    mysql_reachable = False
        if not mysql_reachable:
            # Fallback to local SQLite file
            local_db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'scas.db').replace('\\', '/')
            raw_db = f'sqlite:///{local_db_path}'

    if raw_db:
        # Standardize postgres:// to postgresql:// for SQLAlchemy 1.4/2.0+
        if raw_db.startswith('postgres://'):
            raw_db = raw_db.replace('postgres://', 'postgresql://', 1)
        # Standardize mysql:// to mysql+pymysql://
        elif raw_db.startswith('mysql://'):
            raw_db = raw_db.replace('mysql://', 'mysql+pymysql://', 1)
        SQLALCHEMY_DATABASE_URI = raw_db
    elif is_serverless:
        # On Vercel serverless environment without remote DB, use writable temp directory SQLite
        tmp_db_path = os.path.join(tempfile.gettempdir(), 'scas.db').replace('\\', '/')
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{tmp_db_path}'
    else:
        local_db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'scas.db').replace('\\', '/')
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{local_db_path}'
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Engine connection pooling options for serverless stability
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
    }
    if 'sqlite' in SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_ENGINE_OPTIONS['connect_args'] = {'check_same_thread': False}
    else:
        SQLALCHEMY_ENGINE_OPTIONS['pool_recycle'] = 280
    
    # SMTP Email Configuration (overridden by environment variables if set)
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    SMTP_USER = os.environ.get('SMTP_USER', 'your-email@gmail.com')
    SMTP_PASS = os.environ.get('SMTP_PASS', 'your-app-password')
    
    # AI Risk Prediction constants
    ATTENDANCE_WARNING_THRESHOLD = 75.0  # in percentage

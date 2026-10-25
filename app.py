import os
import urllib.parse
from flask import Flask, redirect, url_for, session, render_template
from werkzeug.middleware.proxy_fix import ProxyFix
from config import Config
from models.models import db, User

# Detect serverless environment
is_serverless = bool(
    os.environ.get('VERCEL') or 
    os.environ.get('VERCEL_ENV') or 
    os.environ.get('AWS_LAMBDA_FUNCTION_NAME') or 
    os.environ.get('LAMBDA_TASK_ROOT') or
    not os.access(os.path.dirname(os.path.abspath(__file__)), os.W_OK)
)

# Manual .env loading on startup (in local development only)
if not is_serverless and os.path.exists('.env'):
    with open('.env', 'r', encoding='utf-8') as f: 
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                k = key.strip()
                if k not in os.environ:
                    val_clean = val.strip().strip("'").strip('"')
                    os.environ[k] = val_clean

# Robust template and static directories resolution
base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'templates')
if not os.path.isdir(template_dir):
    alt_dir = os.path.join(os.getcwd(), 'templates')
    if os.path.isdir(alt_dir):
        template_dir = alt_dir

static_dir = os.path.join(base_dir, 'static')
if not os.path.isdir(static_dir):
    alt_static = os.path.join(os.getcwd(), 'static')
    if os.path.isdir(alt_static):
        static_dir = alt_static

_db_initialized = False

def init_db(target_app=None):
    """Safely initialize database tables and seed demo accounts if needed."""
    global _db_initialized
    if _db_initialized:
        return True
    
    app_instance = target_app or app
    with app_instance.app_context():
        try:
            db.create_all()
            # If Users table is empty, seed demo accounts
            if not User.query.first():
                try:
                    from seed import seed_database
                    seed_database(drop_first=False)
                    app_instance.logger.info("[Database] Successfully seeded demo records.")
                except Exception as seed_err:
                    db.session.rollback()
                    app_instance.logger.warning(f"[Database Seed Warning] {seed_err}")
            _db_initialized = True
            return True
        except Exception as db_err:
            db.session.rollback()
            app_instance.logger.warning(f"[Database Init Warning] {db_err}")
            return False
        finally:
            db.session.remove()

class VercelPathMiddleware:
    """WSGI middleware ensuring clean PATH_INFO under Vercel serverless rewrites."""
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        # 1. Prefer client path captured via rewrite query parameter (__path=$1)
        query_string = environ.get('QUERY_STRING', '')
        params = urllib.parse.parse_qs(query_string, keep_blank_values=True)
        if '__path' in params:
            raw_path = params.pop('__path')[0]
            clean = '/' + raw_path.split('?')[0].lstrip('/')
            for prefix in ['/api/index.py', '/api/index', '/index.py']:
                if clean.startswith(prefix):
                    clean = clean[len(prefix):] or '/'
                    break
            environ['PATH_INFO'] = clean
            environ['QUERY_STRING'] = urllib.parse.urlencode([(k, v) for k, vs in params.items() for v in vs])
        else:
            # 2. Prefer original client path from Vercel edge proxy headers
            raw_uri = environ.get('HTTP_X_FORWARDED_URI') or environ.get('HTTP_X_MATCHED_PATH')
            if raw_uri and raw_uri.startswith('/'):
                environ['PATH_INFO'] = raw_uri.split('?')[0]
            else:
                path = environ.get('PATH_INFO', '')
                for prefix in ['/api/index.py', '/api/index', '/index.py']:
                    if path.startswith(prefix):
                        clean = path[len(prefix):]
                        environ['PATH_INFO'] = clean if clean else '/'
                        break
        return self.wsgi_app(environ, start_response)

def create_app(test_config=None):
    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir,
        static_url_path='/static'
    )
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    
    app.url_map.strict_slashes = False
    
    # Wrap WSGI app with ProxyFix (for HTTPS scheme & proxy headers) and Vercel path normalizer
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    app.wsgi_app = VercelPathMiddleware(app.wsgi_app)
    
    db.init_app(app)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.faculty import faculty_bp
    from routes.student import student_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(faculty_bp, url_prefix='/faculty')
    app.register_blueprint(student_bp, url_prefix='/student')
    
    @app.before_request
    def ensure_db():
        global _db_initialized
        if not _db_initialized:
            init_db(app)

    @app.route('/')
    def index():
        if 'user_id' in session:
            role = session.get('role')
            if role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif role == 'faculty':
                return redirect(url_for('faculty.dashboard'))
            elif role == 'student':
                return redirect(url_for('student.dashboard'))
        return redirect(url_for('auth.login'))

    @app.route('/favicon.ico')
    def favicon():
        return ('', 204)

    # Custom template filters for dashboard reporting
    @app.template_filter('datetimeformat')
    def datetimeformat(value, format='%d %b %Y, %I:%M %p'):
        if value is None:
            return ""
        return value.strftime(format)

    @app.template_filter('dateformat')
    def dateformat(value, format='%d %b %Y'):
        if value is None:
            return ""
        return value.strftime(format)
        
    @app.errorhandler(500)
    def handle_500(e):
        import traceback
        err_trace = traceback.format_exc()
        app.logger.error(f"500 Internal Server Error: {e}\n{err_trace}")
        try:
            return render_template('error.html', error=str(e), traceback=err_trace), 500
        except Exception:
            return (
                f"<!DOCTYPE html><html><head><title>500 Internal Server Error</title></head>"
                f"<body style='font-family:sans-serif;padding:2rem;background:#0d1117;color:#c9d1d9;'>"
                f"<h1 style='color:#f85149;'>500 Internal Server Error</h1>"
                f"<p>{e}</p>"
                f"<details style='background:#161b22;padding:1rem;border-radius:8px;'><summary>Traceback</summary><pre>{err_trace}</pre></details>"
                f"</body></html>",
                500
            )

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print(f"Server Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")

    app.run(debug=True, host='127.0.0.1', port=5000)

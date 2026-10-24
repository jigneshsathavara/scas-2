import os
from flask import Flask, redirect, url_for, session
from config import Config
from models.models import db, User

# Manual .env loading on startup (without overwriting existing environment variables)
if os.path.exists('.env'):
    with open('.env', 'r', encoding='utf-8') as f: 
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                k = key.strip()
                if k not in os.environ:
                    val_clean = val.strip().strip("'").strip('"')
                    os.environ[k] = val_clean

base_dir = os.path.abspath(os.path.dirname(__file__))

def create_app(test_config=None):
    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, 'templates'),
        static_folder=os.path.join(base_dir, 'static'),
        static_url_path='/static'
    )
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    
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
        
    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print(f"Server Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")

    app.run(debug=True, host='127.0.0.1', port=5000)

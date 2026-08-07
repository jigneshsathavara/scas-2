import os
from flask import Flask, redirect, url_for, session
from config import Config
from models.models import db, User

# Manual .env loading on startup
if os.path.exists('.env'):
    with open('.env', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                # Strip potential surrounding quotes
                val_clean = val.strip().strip("'").strip('"')
                os.environ[key.strip()] = val_clean


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
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
    # Build database tables if they do not exist
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='127.0.0.1', port=5000)

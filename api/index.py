import os
import sys

# Ensure the root project directory is on sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app import app
from models.models import db, User

# Auto-initialize database tables and seed initial demo accounts if DB is empty on Vercel
with app.app_context():
    try:
        db.create_all()
        if not User.query.first():
            try:
                from seed import seed_database
                seed_database(drop_first=False)
            except Exception as seed_err:
                app.logger.warning(f"[Vercel Init] Seed warning: {seed_err}")
    except Exception as db_err:
        app.logger.warning(f"[Vercel Init] DB setup warning: {db_err}")

# Vercel looks for the WSGI application instance named 'app'
__all__ = ['app']

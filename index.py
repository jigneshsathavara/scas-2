import os
import sys

# Ensure root directory is in sys.path
root_dir = os.path.abspath(os.path.dirname(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app import app, init_db

# Auto-initialize database tables and demo seed accounts on Vercel
try:
    init_db(app)
except Exception as e:
    app.logger.warning(f"[Vercel Init] Cold-start database init notice: {e}")

# Vercel's Python runtime checks for both 'app' and 'handler'
handler = app

__all__ = ['app', 'handler']

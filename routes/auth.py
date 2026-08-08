from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from functools import wraps
from models.models import db, User

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            if session.get('role') not in roles:
                flash('You do not have permission to view this page.', 'danger')
                # Redirect based on actual role
                actual_role = session.get('role')
                if actual_role == 'admin':
                    return redirect(url_for('admin.dashboard'))
                elif actual_role == 'faculty':
                    return redirect(url_for('faculty.dashboard'))
                elif actual_role == 'student':
                    return redirect(url_for('student.dashboard'))
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        role = session.get('role')
        if role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif role == 'faculty':
            return redirect(url_for('faculty.dashboard'))
        elif role == 'student':
            return redirect(url_for('student.dashboard'))
            
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')
        
        user = User.query.filter((User.username == username) | (User.email == username)).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            session['name'] = user.name
            
            flash(f'Welcome back, {user.name}!', 'success')
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'faculty':
                return redirect(url_for('faculty.dashboard'))
            elif user.role == 'student':
                return redirect(url_for('student.dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        user = User.query.filter_by(email=email).first()
        
        if user:
            import random
            import string
            from email_utils import send_credentials_email
            
            # Generate random temporary password
            temp_pass = "SCAS-RESET-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
            user.set_password(temp_pass)
            db.session.commit()
            
            # Send email
            send_credentials_email(email, user.name, user.role, user.username, temp_pass, is_reset=True)
            flash('A temporary password has been sent to your email. Check sent_emails.log!', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('No account registered with that email address.', 'danger')
            
    return render_template('forgot_password.html')

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        user = db.session.get(User, session['user_id'])
        
        if not user.check_password(current_password):
            flash('Incorrect current password.', 'danger')
            return redirect(url_for('auth.change_password'))
            
        if new_password != confirm_password:
            flash('New password and confirmation do not match.', 'danger')
            return redirect(url_for('auth.change_password'))
            
        if len(new_password) < 6:
            flash('New password must be at least 6 characters long.', 'danger')
            return redirect(url_for('auth.change_password'))
            
        user.set_password(new_password)
        db.session.commit()
        
        flash('Your password has been changed successfully.', 'success')
        # Redirect to appropriate dashboard
        if user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif user.role == 'faculty':
            return redirect(url_for('faculty.dashboard'))
        elif user.role == 'student':
            return redirect(url_for('student.dashboard'))
            
    return render_template('change_password.html')

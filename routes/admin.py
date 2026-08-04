from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
import csv
from io import StringIO, TextIOWrapper
import random
import string
from models.models import db, User, Course, Batch, Subject, StudentProfile, FacultyProfile, FeePayment
from routes.auth import role_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@role_required(['admin'])
def dashboard():
    # Gather aggregate metrics
    total_students = StudentProfile.query.count()
    total_faculty = FacultyProfile.query.count()
    total_courses = Course.query.count()
    
    # Financial statistics
    payments = FeePayment.query.all()
    total_collected = sum(p.amount for p in payments if p.status == 'Paid')
    total_pending = sum(p.amount for p in payments if p.status == 'Pending')
    
    # Recent users for activity feed
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    # JSON-like structures for Chart.js
    courses = Course.query.all()
    course_labels = [c.code for c in courses]
    course_student_counts = [len(c.students) for c in courses]
    
    return render_template(
        'admin/dashboard.html',
        total_students=total_students,
        total_faculty=total_faculty,
        total_courses=total_courses,
        total_collected=total_collected,
        total_pending=total_pending,
        recent_users=recent_users,
        course_labels=course_labels,
        course_student_counts=course_student_counts
    )

# ================= USER MANAGEMENT =================

@admin_bp.route('/users', methods=['GET', 'POST'])
@role_required(['admin'])
def users():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'create':
            username = request.form.get('username').strip()
            name = request.form.get('name').strip()
            email = request.form.get('email').strip()
            password = request.form.get('password')
            role = request.form.get('role')
            
            # Check duplicates
            if User.query.filter_by(username=username).first():
                flash('Username already exists.', 'danger')
                return redirect(url_for('admin.users'))
            if User.query.filter_by(email=email).first():
                flash('Email already exists.', 'danger')
                return redirect(url_for('admin.users'))
                
            new_user = User(username=username, name=name, email=email, role=role)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.flush() # Populate ID
            
            if role == 'faculty':
                dept = request.form.get('department').strip()
                desig = request.form.get('designation').strip()
                fac_profile = FacultyProfile(user_id=new_user.id, department=dept, designation=desig)
                db.session.add(fac_profile)
                
            elif role == 'student':
                roll_no = request.form.get('roll_no').strip()
                batch_id = request.form.get('batch_id')
                course_id = request.form.get('course_id')
                phone = request.form.get('phone').strip()
                
                if StudentProfile.query.filter_by(roll_no=roll_no).first():
                    db.session.rollback()
                    flash('Roll number already exists.', 'danger')
                    return redirect(url_for('admin.users'))
                    
                stud_profile = StudentProfile(
                    user_id=new_user.id, roll_no=roll_no, 
                    batch_id=batch_id, course_id=course_id, phone=phone
                )
                db.session.add(stud_profile)
                
                # Setup a default fee payment record for analytics testing
                fee_payment = FeePayment(
                    student_id=stud_profile.id, amount=45000.0, 
                    status='Pending', receipt_no=f"REC-{roll_no}-DEF"
                )
                db.session.add(fee_payment)
                
            db.session.commit()
            flash(f'Successfully created {role} user: {name}', 'success')
            
        elif action == 'edit':
            user_id = request.form.get('user_id')
            user = User.query.get(user_id)
            if user:
                user.name = request.form.get('name').strip()
                user.email = request.form.get('email').strip()
                
                new_password = request.form.get('password')
                if new_password:
                    user.set_password(new_password)
                    
                if user.role == 'faculty':
                    fac_prof = FacultyProfile.query.filter_by(user_id=user.id).first()
                    if fac_prof:
                        fac_prof.department = request.form.get('department').strip()
                        fac_prof.designation = request.form.get('designation').strip()
                elif user.role == 'student':
                    stud_prof = StudentProfile.query.filter_by(user_id=user.id).first()
                    if stud_prof:
                        stud_prof.roll_no = request.form.get('roll_no').strip()
                        stud_prof.batch_id = request.form.get('batch_id')
                        stud_prof.course_id = request.form.get('course_id')
                        stud_prof.phone = request.form.get('phone').strip()
                        
                db.session.commit()
                flash(f'Successfully updated details for {user.name}', 'success')
                
        elif action == 'delete':
            user_id = request.form.get('user_id')
            user = User.query.get(user_id)
            if user:
                # Student profiles need custom deletion cleanups (cascade will do it mostly)
                name = user.name
                db.session.delete(user)
                db.session.commit()
                flash(f'Successfully deleted user: {name}', 'success')
                
        return redirect(url_for('admin.users'))
        
    all_users = User.query.order_by(User.role, User.name).all()
    courses = Course.query.all()
    batches = Batch.query.all()
    
    return render_template(
        'admin/users.html',
        users=all_users,
        courses=courses,
        batches=batches
    )

# ================= ACADEMIC SETUP =================

@admin_bp.route('/courses', methods=['GET', 'POST'])
@role_required(['admin'])
def courses():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'create_course':
            name = request.form.get('name').strip()
            code = request.form.get('code').strip().upper()
            desc = request.form.get('description').strip()
            
            if Course.query.filter_by(code=code).first():
                flash('Course code already exists.', 'danger')
            else:
                new_course = Course(name=name, code=code, description=desc)
                db.session.add(new_course)
                db.session.commit()
                flash('Course created successfully.', 'success')
                
        elif action == 'create_batch':
            name = request.form.get('name').strip()
            course_id = request.form.get('course_id')
            year = request.form.get('year')
            
            new_batch = Batch(name=name, course_id=course_id, year=year)
            db.session.add(new_batch)
            db.session.commit()
            flash('Batch created successfully.', 'success')
            
        elif action == 'create_subject':
            name = request.form.get('name').strip()
            code = request.form.get('code').strip().upper()
            course_id = request.form.get('course_id')
            faculty_id = request.form.get('faculty_id')
            
            if Subject.query.filter_by(code=code).first():
                flash('Subject code already exists.', 'danger')
            else:
                new_sub = Subject(name=name, code=code, course_id=course_id, faculty_id=faculty_id)
                db.session.add(new_sub)
                db.session.commit()
                flash('Subject registered successfully.', 'success')
                
        elif action == 'delete_course':
            course_id = request.form.get('course_id')
            c = Course.query.get(course_id)
            if c:
                db.session.delete(c)
                db.session.commit()
                flash('Course deleted successfully.', 'success')
                
        elif action == 'delete_subject':
            subject_id = request.form.get('subject_id')
            s = Subject.query.get(subject_id)
            if s:
                db.session.delete(s)
                db.session.commit()
                flash('Subject deleted successfully.', 'success')
                
        return redirect(url_for('admin.courses'))
        
    all_courses = Course.query.all()
    all_batches = Batch.query.all()
    all_subjects = Subject.query.all()
    faculties = User.query.filter_by(role='faculty').all()
    
    return render_template(
        'admin/courses.html',
        courses=all_courses,
        batches=all_batches,
        subjects=all_subjects,
        faculties=faculties
    )

# ================= CSV REPORTS DOWNLOAD =================

@admin_bp.route('/reports/users')
@role_required(['admin'])
def download_users_report():
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Name', 'Username', 'Email', 'Role', 'Date Created'])
    
    users = User.query.order_by(User.role, User.name).all()
    for u in users:
        cw.writerow([u.id, u.name, u.username, u.email, u.role, u.created_at.strftime('%Y-%m-%d %H:%M')])
        
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=users_report.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@admin_bp.route('/reports/financials')
@role_required(['admin'])
def download_financials_report():
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Receipt No', 'Student Name', 'Roll No', 'Course', 'Amount', 'Date Paid', 'Status', 'Txn ID'])
    
    payments = FeePayment.query.join(StudentProfile).join(User).all()
    for p in payments:
        p_date = p.payment_date.strftime('%Y-%m-%d %H:%M') if p.payment_date else 'N/A'
        cw.writerow([
            p.receipt_no, p.student.user.name, p.student.roll_no, 
            p.student.course.code, p.amount, p_date, p.status, p.transaction_id or 'N/A'
        ])
        
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=fee_financials_report.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@admin_bp.route('/reports/users/print')
@role_required(['admin'])
def print_users_report():
    users = User.query.order_by(User.role, User.name).all()
    return render_template('admin/print_users.html', users=users)

@admin_bp.route('/reports/financials/print')
@role_required(['admin'])
def print_financials_report():
    payments = FeePayment.query.join(StudentProfile).join(User).all()
    return render_template('admin/print_financials.html', payments=payments)

@admin_bp.route('/users/upload/students', methods=['POST'])
@role_required(['admin'])
def upload_students_csv():
    if 'file' not in request.files:
        flash('No file uploaded.', 'danger')
        return redirect(url_for('admin.users'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected.', 'danger')
        return redirect(url_for('admin.users'))
    
    if not file.filename.endswith('.csv'):
        flash('Invalid file. Only CSV uploads are supported.', 'danger')
        return redirect(url_for('admin.users'))
        
    try:
        csv_file = TextIOWrapper(file.stream, encoding='utf-8')
        reader = csv.DictReader(csv_file)
        
        success_count = 0
        skipped_count = 0
        
        for row in reader:
            name = row.get('name', '').strip()
            email = row.get('email', '').strip()
            roll_no = row.get('roll_no', '').strip()
            phone = row.get('phone', '').strip()
            course_code = row.get('course_code', '').strip().upper()
            batch_name = row.get('batch_name', '').strip()
            
            if not name or not email or not roll_no or not course_code or not batch_name:
                skipped_count += 1
                continue
                
            username = roll_no.lower()
            
            # Check duplicates
            if User.query.filter((User.username == username) | (User.email == email)).first():
                skipped_count += 1
                continue
            if StudentProfile.query.filter_by(roll_no=roll_no).first():
                skipped_count += 1
                continue
                
            # Resolve Course & Batch
            course = Course.query.filter_by(code=course_code).first()
            if not course:
                skipped_count += 1
                continue
            batch = Batch.query.filter_by(name=batch_name, course_id=course.id).first()
            if not batch:
                skipped_count += 1
                continue
                
            # Generate default password and create account
            temp_pass = "SCAS-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
            new_user = User(username=username, email=email, role='student', name=name)
            new_user.set_password(temp_pass)
            db.session.add(new_user)
            db.session.flush()
            
            # Create StudentProfile
            profile = StudentProfile(
                user_id=new_user.id, roll_no=roll_no, 
                batch_id=batch.id, course_id=course.id, phone=phone
            )
            db.session.add(profile)
            db.session.flush()
            
            # Add default billing
            payment = FeePayment(
                student_id=profile.id, amount=65000.0, 
                status='Pending', receipt_no=f"REC-{roll_no}-CSV"
            )
            db.session.add(payment)
            
            # Trigger email
            from email_utils import send_credentials_email
            send_credentials_email(email, name, 'student', username, temp_pass)
            success_count += 1
            
        db.session.commit()
        flash(f'CSV Upload complete! Imported: {success_count}, Skipped: {skipped_count}. Check sent_emails.log.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Failed to parse CSV file: {str(e)}', 'danger')
        
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/upload/faculty', methods=['POST'])
@role_required(['admin'])
def upload_faculty_csv():
    if 'file' not in request.files:
        flash('No file uploaded.', 'danger')
        return redirect(url_for('admin.users'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected.', 'danger')
        return redirect(url_for('admin.users'))
    
    if not file.filename.endswith('.csv'):
        flash('Invalid file. Only CSV uploads are supported.', 'danger')
        return redirect(url_for('admin.users'))
        
    try:
        csv_file = TextIOWrapper(file.stream, encoding='utf-8')
        reader = csv.DictReader(csv_file)
        
        success_count = 0
        skipped_count = 0
        
        for row in reader:
            name = row.get('name', '').strip()
            email = row.get('email', '').strip()
            dept = row.get('department', '').strip()
            desig = row.get('designation', '').strip()
            sub_code = row.get('subject_code', '').strip().upper()
            sub_name = row.get('subject_name', '').strip()
            course_code = row.get('course_code', '').strip().upper()
            
            if not name or not email or not dept or not desig or not sub_code or not sub_name or not course_code:
                skipped_count += 1
                continue
                
            username = email.split('@')[0].lower()
            
            # Check duplicates
            if User.query.filter((User.username == username) | (User.email == email)).first():
                skipped_count += 1
                continue
                
            # Resolve Course
            course = Course.query.filter_by(code=course_code).first()
            if not course:
                skipped_count += 1
                continue
                
            # Generate default password and create account
            temp_pass = "SCAS-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
            new_user = User(username=username, email=email, role='faculty', name=name)
            new_user.set_password(temp_pass)
            db.session.add(new_user)
            db.session.flush()
            
            # Create FacultyProfile
            profile = FacultyProfile(user_id=new_user.id, department=dept, designation=desig)
            db.session.add(profile)
            
            # Check if Subject exists, update instructor; else create
            subject = Subject.query.filter_by(code=sub_code).first()
            if subject:
                subject.faculty_id = new_user.id
            else:
                subject = Subject(
                    name=sub_name, code=sub_code, 
                    course_id=course.id, faculty_id=new_user.id
                )
                db.session.add(subject)
                
            # Trigger email
            from email_utils import send_credentials_email
            send_credentials_email(email, name, 'faculty', username, temp_pass)
            success_count += 1
            
        db.session.commit()
        flash(f'CSV Upload complete! Imported: {success_count}, Skipped: {skipped_count}. Check sent_emails.log.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Failed to parse CSV file: {str(e)}', 'danger')
        
    return redirect(url_for('admin.users'))

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
import csv
from io import StringIO, TextIOWrapper
import random
import string
from datetime import datetime, date
from models.models import db, User, Course, Batch, Subject, StudentProfile, FacultyProfile, FeePayment, Result, Attendance, LeaveApplication
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
            import re
            email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(email_pattern, email):
                flash('Invalid email address format. Please enter a valid email.', 'danger')
                return redirect(url_for('admin.users'))
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
                db.session.flush() # Populate ID for SQLite
                
                # Setup a default fee payment record for analytics testing
                fee_payment = FeePayment(
                    student_id=stud_profile.id, amount=45000.0, 
                    status='Pending', receipt_no=f"REC-{roll_no}-DEF"
                )
                db.session.add(fee_payment)
                
            db.session.commit()
            
            # Trigger credentials email for manually created user
            from email_utils import send_credentials_email
            send_credentials_email(email, name, role, username, password)
            
            flash(f'Successfully created {role} user: {name}', 'success')
            
        elif action == 'edit':
            user_id = request.form.get('user_id')
            user = User.query.get(user_id)
            if user:
                user.name = request.form.get('name').strip()
                email = request.form.get('email').strip()
                import re
                email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if not re.match(email_pattern, email):
                    flash('Invalid email address format. Please enter a valid email.', 'danger')
                    return redirect(url_for('admin.users'))
                user.email = email
                
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
                
            import re
            email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(email_pattern, email):
                skipped_count += 1
                continue
                
            username = email.lower()
            
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
            temp_pass = row.get('password', '').strip()
            if not temp_pass:
                temp_pass = "SCASStudent123"
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
                
            import re
            email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(email_pattern, email):
                skipped_count += 1
                continue
                
            username = email.lower()
            
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
            temp_pass = row.get('password', '').strip()
            if not temp_pass:
                temp_pass = "SCASFaculty123"
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

@admin_bp.route('/courses/upload/subjects', methods=['POST'])
@role_required(['admin'])
def upload_subjects_csv():
    if 'file' not in request.files:
        flash('No file uploaded.', 'danger')
        return redirect(url_for('admin.courses'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected.', 'danger')
        return redirect(url_for('admin.courses'))
    
    if not file.filename.endswith('.csv'):
        flash('Invalid file. Only CSV uploads are supported.', 'danger')
        return redirect(url_for('admin.courses'))
        
    try:
        csv_file = TextIOWrapper(file.stream, encoding='utf-8')
        reader = csv.DictReader(csv_file)
        
        success_count = 0
        skipped_count = 0
        missing_faculties = []
        
        for row in reader:
            sub_code = row.get('subject_code', '').strip().upper()
            sub_name = row.get('subject_name', '').strip()
            course_code = row.get('course_code', '').strip().upper()
            fac_email = row.get('faculty_email', '').strip().lower()
            
            if not sub_code or not sub_name or not course_code or not fac_email:
                skipped_count += 1
                continue
                
            import re
            email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(email_pattern, fac_email):
                missing_faculties.append(fac_email)
                skipped_count += 1
                continue
                
            # Resolve Course
            course = Course.query.filter_by(code=course_code).first()
            if not course:
                skipped_count += 1
                continue
                
            # Resolve Faculty user
            faculty = User.query.filter_by(email=fac_email, role='faculty').first()
            if not faculty:
                missing_faculties.append(fac_email)
                skipped_count += 1
                continue
                
            # Check if Subject exists, update name, course, and faculty; else create
            subject = Subject.query.filter_by(code=sub_code).first()
            if subject:
                subject.name = sub_name
                subject.course_id = course.id
                subject.faculty_id = faculty.id
            else:
                subject = Subject(
                    name=sub_name, code=sub_code, 
                    course_id=course.id, faculty_id=faculty.id
                )
                db.session.add(subject)
                
            success_count += 1
            
        db.session.commit()
        if missing_faculties:
            unique_missing = list(set(missing_faculties))
            flash(f"Warning: The following faculty emails do not exist: {', '.join(unique_missing)}. Those subjects were not imported.", 'warning')
        flash(f'Subjects CSV Upload complete! Imported/Updated: {success_count}, Skipped: {skipped_count}.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Failed to parse CSV file: {str(e)}', 'danger')
        
    return redirect(url_for('admin.courses'))

@admin_bp.route('/users/send_credentials/<int:user_id>', methods=['POST'])
@role_required(['admin'])
def send_credentials(user_id):
    user = User.query.get_or_404(user_id)
    # Generate temporary password
    temp_pass = "SCAS-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
    user.set_password(temp_pass)
    db.session.commit()
    
    # Trigger email
    from email_utils import send_credentials_email
    send_credentials_email(user.email, user.name, user.role, user.username, temp_pass, is_reset=True)
    
    flash(f'Credentials email sent to {user.name} ({user.email}). Check sent_emails.log.', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/send_all_students_credentials', methods=['POST'])
@role_required(['admin'])
def send_all_students_credentials():
    students = User.query.filter_by(role='student').all()
    if not students:
        flash('No students found in the database.', 'warning')
        return redirect(url_for('admin.users'))
        
    sent_count = 0
    from email_utils import send_credentials_email
    for student in students:
        temp_pass = "SCAS-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        student.set_password(temp_pass)
        send_credentials_email(student.email, student.name, student.role, student.username, temp_pass, is_reset=True)
        sent_count += 1
        
    db.session.commit()
    flash(f'Credentials successfully reset and emailed to all {sent_count} students. Check sent_emails.log.', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/send_all_faculty_credentials', methods=['POST'])
@role_required(['admin'])
def send_all_faculty_credentials():
    faculty_list = User.query.filter_by(role='faculty').all()
    if not faculty_list:
        flash('No faculty members found in the database.', 'warning')
        return redirect(url_for('admin.users'))
        
    sent_count = 0
    from email_utils import send_credentials_email
    for faculty in faculty_list:
        temp_pass = "SCAS-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        faculty.set_password(temp_pass)
        send_credentials_email(faculty.email, faculty.name, faculty.role, faculty.username, temp_pass, is_reset=True)
        sent_count += 1
        
    db.session.commit()
    flash(f'Credentials successfully reset and emailed to all {sent_count} faculty members. Check sent_emails.log.', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/results', methods=['GET'])
@role_required(['admin'])
def results():
    all_results = Result.query.join(StudentProfile).order_by(StudentProfile.roll_no, Result.semester).all()
    grouped = {}
    for r in all_results:
        key = (r.student_id, r.semester)
        if key not in grouped:
            grouped[key] = {
                'student': r.student,
                'semester': r.semester,
                'subjects': [],
                'total_credits': 0,
                'weighted_points': 0
            }
            
        percentage = (r.marks_obtained / r.max_marks * 100) if r.max_marks > 0 else 0
        if percentage >= 90:
            gp = 10
            grade = 'O'
        elif percentage >= 80:
            gp = 9
            grade = 'A+'
        elif percentage >= 70:
            gp = 8
            grade = 'A'
        elif percentage >= 60:
            gp = 7
            grade = 'B+'
        elif percentage >= 50:
            gp = 6
            grade = 'B'
        elif percentage >= 40:
            gp = 5
            grade = 'C'
        else:
            gp = 0
            grade = 'F'
            
        grouped[key]['subjects'].append({
            'code': r.subject.code,
            'name': r.subject.name,
            'marks_obtained': r.marks_obtained,
            'max_marks': r.max_marks,
            'grade': grade,
            'credits': r.credits
        })
        grouped[key]['total_credits'] += r.credits
        grouped[key]['weighted_points'] += gp * r.credits
        
    display_groups = []
    for key, data in grouped.items():
        sgpa = (data['weighted_points'] / data['total_credits']) if data['total_credits'] > 0 else 0.0
        data['sgpa'] = round(sgpa, 2)
        display_groups.append(data)
        
    return render_template('admin/results.html', results=display_groups)

@admin_bp.route('/results/upload', methods=['POST'])
@role_required(['admin'])
def upload_results_csv():
    if 'file' not in request.files:
        flash('No file uploaded.', 'danger')
        return redirect(url_for('admin.results'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected.', 'danger')
        return redirect(url_for('admin.results'))
    
    if not file.filename.endswith('.csv'):
        flash('Invalid file. Only CSV uploads are supported.', 'danger')
        return redirect(url_for('admin.results'))
        
    try:
        csv_file = TextIOWrapper(file.stream, encoding='utf-8')
        reader = csv.DictReader(csv_file)
        
        success_count = 0
        skipped_count = 0
        missing_students = []
        missing_subjects = []
        
        for row in reader:
            roll_no = row.get('roll_no', '').strip()
            sem_str = row.get('semester', '').strip()
            
            if not roll_no or not sem_str:
                skipped_count += 1
                continue
                
            try:
                semester = int(sem_str)
            except ValueError:
                skipped_count += 1
                continue
                
            # Resolve student
            student = StudentProfile.query.filter_by(roll_no=roll_no).first()
            if not student:
                missing_students.append(roll_no)
                skipped_count += 1
                continue
                
            subject_imported_for_row = False
            for i in range(1, 21):
                sub_code = row.get(f'sub{i}_code', '').strip().upper()
                marks_obtained_str = row.get(f'sub{i}_marks', '').strip()
                max_marks_str = row.get(f'sub{i}_max', '').strip()
                credits_str = row.get(f'sub{i}_credits', '').strip()
                
                if not sub_code:
                    continue
                    
                if not marks_obtained_str or not max_marks_str:
                    skipped_count += 1
                    continue
                    
                try:
                    marks_obtained = float(marks_obtained_str)
                    max_marks = float(max_marks_str)
                    credits = int(credits_str) if credits_str else 4
                except ValueError:
                    skipped_count += 1
                    continue
                    
                # Resolve subject
                subject = Subject.query.filter_by(code=sub_code).first()
                if not subject:
                    missing_subjects.append(sub_code)
                    skipped_count += 1
                    continue
                    
                # Check if Result exists, update it; else create
                res = Result.query.filter_by(student_id=student.id, subject_id=subject.id, semester=semester).first()
                if res:
                    res.marks_obtained = marks_obtained
                    res.max_marks = max_marks
                    res.credits = credits
                else:
                    res = Result(
                        student_id=student.id,
                        subject_id=subject.id,
                        semester=semester,
                        marks_obtained=marks_obtained,
                        max_marks=max_marks,
                        credits=credits
                    )
                    db.session.add(res)
                    
                success_count += 1
                subject_imported_for_row = True
                
            if not subject_imported_for_row:
                skipped_count += 1
            
        db.session.commit()
        if missing_students:
            unique_students = list(set(missing_students))
            flash(f"Warning: The following student roll numbers do not exist: {', '.join(unique_students)}", 'warning')
        if missing_subjects:
            unique_subjects = list(set(missing_subjects))
            flash(f"Warning: The following subject codes do not exist: {', '.join(unique_subjects)}", 'warning')
            
        flash(f'Results CSV Upload complete! Imported/Updated: {success_count} subject grades, Skipped/Invalid entries: {skipped_count}.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Failed to parse CSV file: {str(e)}', 'danger')
        
    return redirect(url_for('admin.results'))

@admin_bp.route('/results/delete/<int:student_id>/<int:semester>', methods=['POST'])
@role_required(['admin'])
def delete_result(student_id, semester):
    Result.query.filter_by(student_id=student_id, semester=semester).delete()
    db.session.commit()
    flash('Student semester result records deleted successfully.', 'success')
    return redirect(url_for('admin.results'))

@admin_bp.route('/attendance', methods=['GET', 'POST'])
@role_required(['admin'])
def attendance():
    subjects = Subject.query.all()
    
    selected_subject_id = request.args.get('subject_id', type=int)
    selected_batch_id = request.args.get('batch_id', type=int)
    selected_date_str = request.args.get('date', default=date.today().isoformat())
    selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    
    batches = []
    students = []
    attendance_records = {}
    
    if selected_subject_id:
        sub = Subject.query.get(selected_subject_id)
        if sub:
            batches = Batch.query.filter_by(course_id=sub.course_id).all()
            
    if selected_subject_id and selected_batch_id:
        students = StudentProfile.query.filter_by(batch_id=selected_batch_id).all()
        logs = Attendance.query.filter_by(
            subject_id=selected_subject_id, 
            date=selected_date
        ).all()
        attendance_records = {log.student_id: log.status for log in logs}
        
    if request.method == 'POST':
        sub_id = request.form.get('subject_id', type=int)
        bat_id = request.form.get('batch_id', type=int)
        att_date_str = request.form.get('date')
        att_date = datetime.strptime(att_date_str, '%Y-%m-%d').date()
        
        students_to_mark = StudentProfile.query.filter_by(batch_id=bat_id).all()
        
        for s in students_to_mark:
            status = 'Present' if request.form.get(f'status_{s.id}') == 'on' else 'Absent'
            
            log = Attendance.query.filter_by(
                student_id=s.id, 
                subject_id=sub_id, 
                date=att_date
            ).first()
            
            if log:
                log.status = status
            else:
                new_log = Attendance(
                    student_id=s.id, 
                    subject_id=sub_id, 
                    date=att_date, 
                    status=status
                )
                db.session.add(new_log)
                
        db.session.commit()
        flash(f'Attendance recorded for date: {att_date_str}', 'success')
        return redirect(url_for('admin.attendance', subject_id=sub_id, batch_id=bat_id, date=att_date_str))
        
    return render_template(
        'admin/attendance.html',
        subjects=subjects,
        batches=batches,
        students=students,
        attendance_records=attendance_records,
        selected_subject_id=selected_subject_id,
        selected_batch_id=selected_batch_id,
        selected_date=selected_date_str
    )

@admin_bp.route('/attendance/download/<int:subject_id>/<int:batch_id>')
@role_required(['admin'])
def download_attendance_report(subject_id, batch_id):
    sub = Subject.query.get_or_404(subject_id)
    bat = Batch.query.get_or_404(batch_id)
    students = StudentProfile.query.filter_by(batch_id=batch_id).all()
    
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Roll Number', 'Student Name', 'Present Classes', 'Total Classes', 'Attendance Rate %'])
    
    for s in students:
        pres = Attendance.query.filter_by(student_id=s.id, subject_id=subject_id, status='Present').count()
        tot = Attendance.query.filter_by(student_id=s.id, subject_id=subject_id).count()
        rate = (pres / tot * 100) if tot > 0 else 100.0
        cw.writerow([s.roll_no, s.user.name, pres, tot, round(rate, 1)])
        
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=attendance_{sub.code}_{bat.name.replace(' ', '_')}.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@admin_bp.route('/attendance/print/<int:subject_id>/<int:batch_id>')
@role_required(['admin'])
def print_attendance_report(subject_id, batch_id):
    sub = Subject.query.get_or_404(subject_id)
    bat = Batch.query.get_or_404(batch_id)
    students = StudentProfile.query.filter_by(batch_id=batch_id).all()
    
    report_data = []
    for s in students:
        pres = Attendance.query.filter_by(student_id=s.id, subject_id=subject_id, status='Present').count()
        tot = Attendance.query.filter_by(student_id=s.id, subject_id=subject_id).count()
        rate = (pres / tot * 100) if tot > 0 else 100.0
        report_data.append({
            'student': s,
            'present': pres,
            'total': tot,
            'rate': round(rate, 1)
        })
        
    return render_template(
        'faculty/print_attendance.html',
        subject=sub,
        batch=bat,
        report_data=report_data
    )

@admin_bp.route('/leaves', methods=['GET'])
@role_required(['admin'])
def leaves():
    status_filter = request.args.get('status', 'Pending')
    
    if status_filter == 'All':
        applications = LeaveApplication.query.order_by(LeaveApplication.applied_at.desc()).all()
    else:
        applications = LeaveApplication.query.filter_by(status=status_filter).order_by(LeaveApplication.applied_at.desc()).all()
        
    return render_template(
        'admin/leaves.html',
        applications=applications,
        selected_status=status_filter
    )

@admin_bp.route('/leaves/action/<int:leave_id>/<string:action>', methods=['POST'])
@role_required(['admin'])
def leave_action(leave_id, action):
    app_record = LeaveApplication.query.get_or_404(leave_id)
    
    if action == 'approve':
        app_record.status = 'Approved'
        flash(f"Leave application for {app_record.user.name} approved.", 'success')
    elif action == 'reject':
        app_record.status = 'Rejected'
        flash(f"Leave application for {app_record.user.name} rejected.", 'warning')
        
    db.session.commit()
    return redirect(url_for('admin.leaves'))


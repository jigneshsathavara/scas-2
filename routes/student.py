from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
import csv
import random
import string
from datetime import datetime
from io import StringIO
from models.models import db, User, Course, Batch, Subject, StudentProfile, Schedule, Attendance, Mark, FeePayment
from routes.auth import role_required

student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard')
@role_required(['student'])
def dashboard():
    user_id = session.get('user_id')
    student = StudentProfile.query.filter_by(user_id=user_id).first()
    
    if not student:
        flash('Student profile not found.', 'danger')
        return redirect(url_for('auth.login'))
        
    # Get subjects in student's course
    subjects = Subject.query.filter_by(course_id=student.course_id).all()
    
    # Calculate attendance metrics
    subject_attendance = []
    total_present = 0
    total_sessions = 0
    
    for sub in subjects:
        pres = Attendance.query.filter_by(student_id=student.id, subject_id=sub.id, status='Present').count()
        tot = Attendance.query.filter_by(student_id=student.id, subject_id=sub.id).count()
        rate = (pres / tot * 100) if tot > 0 else 100.0
        
        subject_attendance.append({
            'subject_name': sub.name,
            'subject_code': sub.code,
            'present': pres,
            'total': tot,
            'rate': round(rate, 1)
        })
        total_present += pres
        total_sessions += tot
        
    overall_attendance = (total_present / total_sessions * 100) if total_sessions > 0 else 100.0
    
    # Calculate academic grades average
    marks = Mark.query.filter_by(student_id=student.id).all()
    gpa_base = 0.0
    if marks:
        percentage_avg = sum((m.marks_obtained / m.max_marks * 100) for m in marks) / len(marks)
        # Convert to 10-point GPA scale
        gpa_base = (percentage_avg / 10.0)
    else:
        gpa_base = 0.0
        
    # Find next lecture today
    today_name = datetime.now().strftime('%A')
    schedules = Schedule.query.filter_by(batch_id=student.batch_id, day_of_week=today_name).all()
    
    # Fetch billing info
    pending_bill = FeePayment.query.filter_by(student_id=student.id, status='Pending').first()
    
    return render_template(
        'student/dashboard.html',
        student=student,
        subject_attendance=subject_attendance,
        overall_attendance=round(overall_attendance, 1),
        gpa=round(gpa_base, 2),
        today_schedules=schedules,
        pending_bill=pending_bill
    )

@student_bp.route('/academic')
@role_required(['student'])
def academic():
    user_id = session.get('user_id')
    student = StudentProfile.query.filter_by(user_id=user_id).first()
    
    subjects = Subject.query.filter_by(course_id=student.course_id).all()
    
    academic_summary = []
    for sub in subjects:
        # Attendance rates
        pres = Attendance.query.filter_by(student_id=student.id, subject_id=sub.id, status='Present').count()
        tot = Attendance.query.filter_by(student_id=student.id, subject_id=sub.id).count()
        att_rate = (pres / tot * 100) if tot > 0 else 100.0
        
        # Test grades
        marks_list = Mark.query.filter_by(student_id=student.id, subject_id=sub.id).all()
        
        academic_summary.append({
            'subject': sub,
            'present': pres,
            'total': tot,
            'attendance_rate': round(att_rate, 1),
            'marks': marks_list
        })
        
    return render_template(
        'student/academic.html',
        student=student,
        academic_summary=academic_summary
    )

@student_bp.route('/payment', methods=['GET', 'POST'])
@role_required(['student'])
def payment():
    user_id = session.get('user_id')
    student = StudentProfile.query.filter_by(user_id=user_id).first()
    
    if request.method == 'POST':
        payment_id = request.form.get('payment_id', type=int)
        card_no = request.form.get('card_number')
        
        bill = FeePayment.query.filter_by(id=payment_id, student_id=student.id).first()
        if bill and bill.status == 'Pending':
            # Complete mock payment processing
            bill.status = 'Paid'
            bill.payment_date = datetime.now()
            
            # Generate random receipt number and transaction code
            txn_hash = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            bill.transaction_id = f"TXN-{txn_hash}"
            bill.receipt_no = f"REC-{student.roll_no}-{random.randint(1000, 9999)}"
            
            db.session.commit()
            flash('Mock Tuition Fee paid successfully! Receipt generated.', 'success')
            return redirect(url_for('student.receipt', payment_id=bill.id))
            
    # Load bills list
    bills = FeePayment.query.filter_by(student_id=student.id).order_by(FeePayment.status.desc(), FeePayment.payment_date.desc()).all()
    return render_template('student/payment.html', student=student, bills=bills)

@student_bp.route('/receipt/<int:payment_id>')
@role_required(['student'])
def receipt(payment_id):
    user_id = session.get('user_id')
    student = StudentProfile.query.filter_by(user_id=user_id).first()
    
    payment = FeePayment.query.filter_by(id=payment_id, student_id=student.id, status='Paid').first()
    if not payment:
        flash('Receipt not found or payment is incomplete.', 'danger')
        return redirect(url_for('student.payment'))
        
    return render_template('student/receipt.html', student=student, payment=payment)

# ================= CSV REPORTS DOWNLOAD =================

@student_bp.route('/reports/academic')
@role_required(['student'])
def download_student_report():
    user_id = session.get('user_id')
    student = StudentProfile.query.filter_by(user_id=user_id).first()
    
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Subject Code', 'Subject Name', 'Exam Type', 'Marks Obtained', 'Max Marks', 'Percentage %'])
    
    marks = Mark.query.filter_by(student_id=student.id).join(Subject).all()
    for m in marks:
        perc = (m.marks_obtained / m.max_marks * 100)
        cw.writerow([m.subject.code, m.subject.name, m.exam_type, m.marks_obtained, m.max_marks, round(perc, 2)])
        
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=academic_report_{student.roll_no}.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@student_bp.route('/reports/academic/print')
@role_required(['student'])
def print_student_report():
    user_id = session.get('user_id')
    student = StudentProfile.query.filter_by(user_id=user_id).first()
    
    subjects = Subject.query.filter_by(course_id=student.course_id).all()
    
    academic_summary = []
    for sub in subjects:
        pres = Attendance.query.filter_by(student_id=student.id, subject_id=sub.id, status='Present').count()
        tot = Attendance.query.filter_by(student_id=student.id, subject_id=sub.id).count()
        att_rate = (pres / tot * 100) if tot > 0 else 100.0
        
        marks_list = Mark.query.filter_by(student_id=student.id, subject_id=sub.id).all()
        
        academic_summary.append({
            'subject': sub,
            'present': pres,
            'total': tot,
            'attendance_rate': round(att_rate, 1),
            'marks': marks_list
        })
        
    return render_template(
        'student/print_academic.html',
        student=student,
        academic_summary=academic_summary
    )

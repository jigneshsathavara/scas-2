from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, make_response
from datetime import datetime, date
import csv
from io import StringIO
from models.models import db, User, Course, Batch, Subject, StudentProfile, Schedule, Attendance, Mark
from routes.auth import role_required

faculty_bp = Blueprint('faculty', __name__)

# Helper function to get AI risk calculations for a student list
def run_ai_prediction_for_students(students, subject_id):
    # Features for the AI: Attendance rate, Midterm avg, assignment avg
    predictions = []
    
    for s in students:
        # 1. Attendance Rate
        total_att = Attendance.query.filter_by(student_id=s.id, subject_id=subject_id).count()
        present_att = Attendance.query.filter_by(student_id=s.id, subject_id=subject_id, status='Present').count()
        att_rate = (present_att / total_att * 100) if total_att > 0 else 100.0
        
        # 2. Academic Midterms
        marks = Mark.query.filter_by(student_id=s.id, subject_id=subject_id).all()
        midterm_marks = [m.marks_obtained / m.max_marks for m in marks if 'Midterm' in m.exam_type]
        midterm_avg = sum(midterm_marks) / len(midterm_marks) if len(midterm_marks) > 0 else 1.0 # default to pass if no exams yet
        
        # 3. Decision Heuristics / Mock ML Model
        # In a real project, this simulates a classifier model trained on past grades.
        # High Risk: low attendance AND low midterms, or critical levels of either
        # Medium Risk: average attendance (~70-80%) or average midterms (~40-60%)
        # Low Risk: good attendance and good grades
        
        risk_score = 0.0
        # Weights: 45% attendance, 55% marks
        risk_score += (1.0 - (att_rate / 100.0)) * 4.5
        risk_score += (1.0 - midterm_avg) * 5.5
        
        if risk_score >= 4.0 or att_rate < 70.0 or midterm_avg < 0.45:
            risk_level = "High Risk"
            risk_color = "danger"
            reason = "Poor midterm score or critically low attendance."
        elif risk_score >= 2.0 or att_rate < 80.0 or midterm_avg < 0.65:
            risk_level = "Medium Risk"
            risk_color = "warning"
            reason = "Borderline attendance/performance metrics."
        else:
            risk_level = "Low Risk"
            risk_color = "success"
            reason = "Satisfactory progress in tests & attendance."
            
        predictions.append({
            'student_id': s.id,
            'name': s.user.name,
            'roll_no': s.roll_no,
            'attendance_rate': round(att_rate, 1),
            'midterm_avg': round(midterm_avg * 100, 1),
            'risk_level': risk_level,
            'risk_color': risk_color,
            'reason': reason
        })
    return predictions

@faculty_bp.route('/dashboard')
@role_required(['faculty'])
def dashboard():
    faculty_id = session.get('user_id')
    # Get subjects assigned to this faculty
    subjects = Subject.query.filter_by(faculty_id=faculty_id).all()
    
    # Get total teaching schedules
    schedules = Schedule.query.filter(Schedule.subject_id.in_([s.id for s in subjects])).all() if subjects else []
    
    # Run AI analysis for students across all classes taught
    at_risk_students = []
    for sub in subjects:
        # Students in the batches that take this subject
        batches = Batch.query.filter_by(course_id=sub.course_id).all()
        for b in batches:
            students = StudentProfile.query.filter_by(batch_id=b.id).all()
            preds = run_ai_prediction_for_students(students, sub.id)
            for p in preds:
                if p['risk_level'] != 'Low Risk':
                    p['subject'] = sub.name
                    p['batch'] = b.name
                    at_risk_students.append(p)
                    
    return render_template(
        'faculty/dashboard.html',
        subjects=subjects,
        schedules=schedules,
        at_risk_students=at_risk_students[:10]  # Show top 10 alert profiles
    )

# ================= ATTENDANCE MANAGEMENT =================

@faculty_bp.route('/attendance', methods=['GET', 'POST'])
@role_required(['faculty'])
def attendance():
    faculty_id = session.get('user_id')
    subjects = Subject.query.filter_by(faculty_id=faculty_id).all()
    
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
            # Batches are linked via course
            batches = Batch.query.filter_by(course_id=sub.course_id).all()
            
    if selected_subject_id and selected_batch_id:
        students = StudentProfile.query.filter_by(batch_id=selected_batch_id).all()
        # Find existing attendance logs for this day
        logs = Attendance.query.filter_by(
            subject_id=selected_subject_id, 
            date=selected_date
        ).all()
        attendance_records = {log.student_id: log.status for log in logs}
        
    if request.method == 'POST':
        # Handle marking attendance
        sub_id = request.form.get('subject_id', type=int)
        bat_id = request.form.get('batch_id', type=int)
        att_date_str = request.form.get('date')
        att_date = datetime.strptime(att_date_str, '%Y-%m-%d').date()
        
        students_to_mark = StudentProfile.query.filter_by(batch_id=bat_id).all()
        
        for s in students_to_mark:
            # Check status
            status = 'Present' if request.form.get(f'status_{s.id}') == 'on' else 'Absent'
            
            # Update or create
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
        return redirect(url_for('faculty.attendance', subject_id=sub_id, batch_id=bat_id, date=att_date_str))
        
    return render_template(
        'faculty/attendance.html',
        subjects=subjects,
        batches=batches,
        students=students,
        attendance_records=attendance_records,
        selected_subject_id=selected_subject_id,
        selected_batch_id=selected_batch_id,
        selected_date=selected_date_str
    )

# ================= MARKS UPLOADER =================

@faculty_bp.route('/marks', methods=['GET', 'POST'])
@role_required(['faculty'])
def marks():
    faculty_id = session.get('user_id')
    subjects = Subject.query.filter_by(faculty_id=faculty_id).all()
    
    selected_subject_id = request.args.get('subject_id', type=int)
    selected_batch_id = request.args.get('batch_id', type=int)
    selected_exam = request.args.get('exam_type', default='Midterm 1')
    
    batches = []
    students = []
    marks_records = {}
    
    if selected_subject_id:
        sub = Subject.query.get(selected_subject_id)
        if sub:
            batches = Batch.query.filter_by(course_id=sub.course_id).all()
            
    if selected_subject_id and selected_batch_id:
        students = StudentProfile.query.filter_by(batch_id=selected_batch_id).all()
        # Find existing marks
        logs = Mark.query.filter_by(
            subject_id=selected_subject_id,
            exam_type=selected_exam
        ).all()
        marks_records = {log.student_id: log.marks_obtained for log in logs}
        
    if request.method == 'POST':
        sub_id = request.form.get('subject_id', type=int)
        bat_id = request.form.get('batch_id', type=int)
        exam_type = request.form.get('exam_type')
        max_marks = float(request.form.get('max_marks', 100))
        
        students_to_mark = StudentProfile.query.filter_by(batch_id=bat_id).all()
        
        for s in students_to_mark:
            val = request.form.get(f'marks_{s.id}')
            if val is not None and val.strip() != '':
                obtained = float(val)
                
                # Update or create
                record = Mark.query.filter_by(
                    student_id=s.id,
                    subject_id=sub_id,
                    exam_type=exam_type
                ).first()
                
                if record:
                    record.marks_obtained = obtained
                    record.max_marks = max_marks
                else:
                    new_record = Mark(
                        student_id=s.id,
                        subject_id=sub_id,
                        exam_type=exam_type,
                        marks_obtained=obtained,
                        max_marks=max_marks
                    )
                    db.session.add(new_record)
                    
        db.session.commit()
        flash(f'Exam results updated for {exam_type}', 'success')
        return redirect(url_for('faculty.marks', subject_id=sub_id, batch_id=bat_id, exam_type=exam_type))
        
    return render_template(
        'faculty/marks.html',
        subjects=subjects,
        batches=batches,
        students=students,
        marks_records=marks_records,
        selected_subject_id=selected_subject_id,
        selected_batch_id=selected_batch_id,
        selected_exam=selected_exam
    )

# ================= SCHEDULE MANAGEMENT =================

@faculty_bp.route('/schedule', methods=['GET', 'POST'])
@role_required(['faculty'])
def schedule():
    faculty_id = session.get('user_id')
    subjects = Subject.query.filter_by(faculty_id=faculty_id).all()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            subject_id = request.form.get('subject_id')
            batch_id = request.form.get('batch_id')
            day_of_week = request.form.get('day_of_week')
            start_time = request.form.get('start_time')
            end_time = request.form.get('end_time')
            room = request.form.get('room').strip()
            
            new_schedule = Schedule(
                subject_id=subject_id, batch_id=batch_id, 
                day_of_week=day_of_week, start_time=start_time, 
                end_time=end_time, room=room
            )
            db.session.add(new_schedule)
            db.session.commit()
            flash('Lecture scheduled successfully.', 'success')
            
        elif action == 'delete':
            schedule_id = request.form.get('schedule_id')
            sched = Schedule.query.get(schedule_id)
            if sched:
                db.session.delete(sched)
                db.session.commit()
                flash('Lecture removed from schedule.', 'success')
                
        return redirect(url_for('faculty.schedule'))
        
    # Get all faculty schedules
    schedules = Schedule.query.filter(Schedule.subject_id.in_([s.id for s in subjects])).all() if subjects else []
    # Collect batches available for scheduling (from all subjects courses)
    course_ids = list(set([s.course_id for s in subjects]))
    batches = Batch.query.filter(Batch.course_id.in_(course_ids)).all() if course_ids else []
    
    return render_template(
        'faculty/schedule.html',
        subjects=subjects,
        batches=batches,
        schedules=schedules
    )

# ================= CSV REPORTS DOWNLOAD =================

@faculty_bp.route('/reports/attendance/<int:subject_id>/<int:batch_id>')
@role_required(['faculty'])
def download_attendance_report(subject_id, batch_id):
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Roll No', 'Student Name', 'Present Classes', 'Total Classes', 'Attendance %'])
    
    students = StudentProfile.query.filter_by(batch_id=batch_id).all()
    for s in students:
        total_att = Attendance.query.filter_by(student_id=s.id, subject_id=subject_id).count()
        present_att = Attendance.query.filter_by(student_id=s.id, subject_id=subject_id, status='Present').count()
        rate = (present_att / total_att * 100) if total_att > 0 else 100.0
        cw.writerow([s.roll_no, s.user.name, present_att, total_att, round(rate, 2)])
        
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=attendance_report_subject_{subject_id}.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@faculty_bp.route('/reports/marks/<int:subject_id>/<int:batch_id>/<exam_type>')
@role_required(['faculty'])
def download_marks_report(subject_id, batch_id, exam_type):
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Roll No', 'Student Name', 'Exam Type', 'Marks Obtained', 'Max Marks', 'Percentage %'])
    
    students = StudentProfile.query.filter_by(batch_id=batch_id).all()
    for s in students:
        record = Mark.query.filter_by(student_id=s.id, subject_id=subject_id, exam_type=exam_type).first()
        if record:
            perc = (record.marks_obtained / record.max_marks * 100)
            cw.writerow([s.roll_no, s.user.name, exam_type, record.marks_obtained, record.max_marks, round(perc, 2)])
        else:
            cw.writerow([s.roll_no, s.user.name, exam_type, 'N/A', 'N/A', 'N/A'])
            
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=marks_report_{exam_type.replace(' ', '_')}.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@faculty_bp.route('/reports/attendance/<int:subject_id>/<int:batch_id>/print')
@role_required(['faculty'])
def print_attendance_report(subject_id, batch_id):
    subject = Subject.query.get_or_404(subject_id)
    batch = Batch.query.get_or_404(batch_id)
    students = StudentProfile.query.filter_by(batch_id=batch_id).all()
    
    attendance_summary = []
    for s in students:
        total_att = Attendance.query.filter_by(student_id=s.id, subject_id=subject_id).count()
        present_att = Attendance.query.filter_by(student_id=s.id, subject_id=subject_id, status='Present').count()
        rate = (present_att / total_att * 100) if total_att > 0 else 100.0
        attendance_summary.append({
            'student': s,
            'present': present_att,
            'total': total_att,
            'rate': round(rate, 1)
        })
        
    return render_template(
        'faculty/print_attendance.html',
        subject=subject,
        batch=batch,
        attendance_summary=attendance_summary
    )

@faculty_bp.route('/reports/marks/<int:subject_id>/<int:batch_id>/<exam_type>/print')
@role_required(['faculty'])
def print_marks_report(subject_id, batch_id, exam_type):
    subject = Subject.query.get_or_404(subject_id)
    batch = Batch.query.get_or_404(batch_id)
    students = StudentProfile.query.filter_by(batch_id=batch_id).all()
    
    marks_summary = []
    for s in students:
        record = Mark.query.filter_by(student_id=s.id, subject_id=subject_id, exam_type=exam_type).first()
        marks_summary.append({
            'student': s,
            'record': record
        })
        
    return render_template(
        'faculty/print_marks.html',
        subject=subject,
        batch=batch,
        exam_type=exam_type,
        marks_summary=marks_summary
    )

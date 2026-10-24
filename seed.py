from models.models import db, User, Course, Batch, FacultyProfile, StudentProfile, Subject, FeePayment, Schedule, Attendance, Mark, Result, LeaveApplication
from datetime import datetime, date, timedelta

def seed_database(drop_first=True):
    print("Starting database seeding...")
    
    # Drop all and recreate database tables only when requested
    if drop_first:
        db.drop_all()
    db.create_all()
    
    # 1. Create Users
    # Admin
    admin_user = User(username='admin', email='admin@college.edu', role='admin', name='Dean System Administrator')
    admin_user.set_password('admin123')
    db.session.add(admin_user)
    db.session.flush()
    
    # 2. Create Courses & Batches
    c1 = Course(name='Master of Computer Applications', code='MCA', description='Post-graduate program in Computer Applications and Software Engineering.')
    db.session.add(c1)
    db.session.flush()
    
    b1 = Batch(name='MCA 2024-2026', course_id=c1.id, year=2026)
    db.session.add(b1)
    db.session.flush()

    # 3. Create Faculty
    f1 = User(username='cdpatel@college.edu', email='cdpatel@college.edu', role='faculty', name='Dr. CD Patel')
    f1.set_password('SCASFaculty123')
    db.session.add(f1)
    db.session.flush()
    fp1 = FacultyProfile(user_id=f1.id, department='Computer Applications', designation='Professor')
    db.session.add(fp1)

    f2 = User(username='sanjaybhai@college.edu', email='sanjaybhai@college.edu', role='faculty', name='Prof. sanjaybhai patel')
    f2.set_password('SCASFaculty123')
    db.session.add(f2)
    db.session.flush()
    fp2 = FacultyProfile(user_id=f2.id, department='Computer Applications', designation='Associate Professor')
    db.session.add(fp2)
    db.session.flush()

    # 4. Create Subjects
    sub1 = Subject(name='Theory of Computation', code='MCA-104', course_id=c1.id, faculty_id=f1.id)
    sub2 = Subject(name='Compiler Design', code='MCA-105', course_id=c1.id, faculty_id=f2.id)
    db.session.add_all([sub1, sub2])
    db.session.flush()

    # 5. Create Students
    s1 = User(username='goswami@college.edu', email='goswami@college.edu', role='student', name='himanshu goswami')
    s1.set_password('SCASStudent123')
    db.session.add(s1)
    db.session.flush()
    sp1 = StudentProfile(user_id=s1.id, roll_no='MCA24004', course_id=c1.id, batch_id=b1.id, phone='7016429311')
    db.session.add(sp1)

    s2 = User(username='sathavara@college.edu', email='sathavara@college.edu', role='student', name='jignesh sathavara')
    s2.set_password('SCASStudent123')
    db.session.add(s2)
    db.session.flush()
    sp2 = StudentProfile(user_id=s2.id, roll_no='MCA24005', course_id=c1.id, batch_id=b1.id, phone='9898510712')
    db.session.add(sp2)
    db.session.flush()

    # 6. Create Fee Payments
    p1 = FeePayment(student_id=sp1.id, amount=65000.0, status='Pending', receipt_no='REC-MCA24004-CSV')
    p2 = FeePayment(student_id=sp2.id, amount=65000.0, status='Paid', receipt_no='REC-MCA24005-CSV', transaction_id='TXN-984712-SUCCESS', payment_date=datetime.utcnow())
    db.session.add_all([p1, p2])
    db.session.flush()

    # 7. Create Lecture Schedules
    sched1 = Schedule(subject_id=sub1.id, batch_id=b1.id, day_of_week='Monday', start_time='09:00 AM', end_time='10:30 AM', room='Lab 3')
    sched2 = Schedule(subject_id=sub2.id, batch_id=b1.id, day_of_week='Monday', start_time='11:00 AM', end_time='12:30 PM', room='Room 204')
    sched3 = Schedule(subject_id=sub1.id, batch_id=b1.id, day_of_week='Wednesday', start_time='10:00 AM', end_time='11:30 AM', room='Lab 3')
    sched4 = Schedule(subject_id=sub2.id, batch_id=b1.id, day_of_week='Friday', start_time='02:00 PM', end_time='03:30 PM', room='Room 204')
    db.session.add_all([sched1, sched2, sched3, sched4])
    db.session.flush()

    # 8. Create Attendance Records
    base_date = date.today()
    for days_back in range(1, 15):
        past_date = base_date - timedelta(days=days_back)
        if past_date.weekday() < 5:  # Monday to Friday
            # Subject 1 attendance
            db.session.add(Attendance(student_id=sp1.id, subject_id=sub1.id, date=past_date, status='Present'))
            db.session.add(Attendance(student_id=sp2.id, subject_id=sub1.id, date=past_date, status='Present' if days_back % 3 != 0 else 'Absent'))
            
            # Subject 2 attendance
            db.session.add(Attendance(student_id=sp1.id, subject_id=sub2.id, date=past_date, status='Present' if days_back % 4 != 0 else 'Absent'))
            db.session.add(Attendance(student_id=sp2.id, subject_id=sub2.id, date=past_date, status='Present'))

    # 9. Create Exam Marks
    marks_data = [
        # Student 1 (Himanshu)
        Mark(student_id=sp1.id, subject_id=sub1.id, exam_type='Midterm 1', marks_obtained=26.0, max_marks=30.0),
        Mark(student_id=sp1.id, subject_id=sub1.id, exam_type='Midterm 2', marks_obtained=27.5, max_marks=30.0),
        Mark(student_id=sp1.id, subject_id=sub1.id, exam_type='Final Exam', marks_obtained=62.0, max_marks=70.0),
        Mark(student_id=sp1.id, subject_id=sub1.id, exam_type='Assignment', marks_obtained=19.0, max_marks=20.0),
        Mark(student_id=sp1.id, subject_id=sub2.id, exam_type='Midterm 1', marks_obtained=24.0, max_marks=30.0),
        Mark(student_id=sp1.id, subject_id=sub2.id, exam_type='Midterm 2', marks_obtained=25.0, max_marks=30.0),
        Mark(student_id=sp1.id, subject_id=sub2.id, exam_type='Final Exam', marks_obtained=58.0, max_marks=70.0),
        Mark(student_id=sp1.id, subject_id=sub2.id, exam_type='Assignment', marks_obtained=18.0, max_marks=20.0),

        # Student 2 (Jignesh)
        Mark(student_id=sp2.id, subject_id=sub1.id, exam_type='Midterm 1', marks_obtained=28.0, max_marks=30.0),
        Mark(student_id=sp2.id, subject_id=sub1.id, exam_type='Midterm 2', marks_obtained=29.0, max_marks=30.0),
        Mark(student_id=sp2.id, subject_id=sub1.id, exam_type='Final Exam', marks_obtained=65.0, max_marks=70.0),
        Mark(student_id=sp2.id, subject_id=sub1.id, exam_type='Assignment', marks_obtained=20.0, max_marks=20.0),
        Mark(student_id=sp2.id, subject_id=sub2.id, exam_type='Midterm 1', marks_obtained=22.0, max_marks=30.0),
        Mark(student_id=sp2.id, subject_id=sub2.id, exam_type='Midterm 2', marks_obtained=23.5, max_marks=30.0),
        Mark(student_id=sp2.id, subject_id=sub2.id, exam_type='Final Exam', marks_obtained=54.0, max_marks=70.0),
        Mark(student_id=sp2.id, subject_id=sub2.id, exam_type='Assignment', marks_obtained=17.0, max_marks=20.0),
    ]
    db.session.add_all(marks_data)

    # 10. Create Semester Results
    res1 = Result(student_id=sp1.id, subject_id=sub1.id, semester=1, marks_obtained=88.0, max_marks=100.0, credits=4)
    res2 = Result(student_id=sp1.id, subject_id=sub2.id, semester=1, marks_obtained=82.0, max_marks=100.0, credits=4)
    res3 = Result(student_id=sp2.id, subject_id=sub1.id, semester=1, marks_obtained=92.0, max_marks=100.0, credits=4)
    res4 = Result(student_id=sp2.id, subject_id=sub2.id, semester=1, marks_obtained=76.0, max_marks=100.0, credits=4)
    db.session.add_all([res1, res2, res3, res4])

    # 11. Create Sample Leave Application
    leave1 = LeaveApplication(
        user_id=s1.id,
        leave_type='Sick Leave',
        start_date=date.today() + timedelta(days=2),
        end_date=date.today() + timedelta(days=3),
        reason='Medical appointment and dental procedure.',
        status='Pending'
    )
    db.session.add(leave1)

    db.session.commit()
    print("Database seeding completed successfully (faculty, students, schedules, attendance, marks, results, and leaves populated)!")

if __name__ == '__main__':
    from app import app
    with app.app_context():
        seed_database(drop_first=True)

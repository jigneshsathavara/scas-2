from app import create_app
from models.models import db, User, Course, Batch, StudentProfile, FacultyProfile, Subject, Schedule, Attendance, Mark, FeePayment
from datetime import datetime, date, timedelta

app = create_app()

def seed_database():
    print("Starting database seeding...")
    
    # Drop all and recreate database tables
    db.drop_all()
    db.create_all()
    
    # 1. Create Users
    # Admin
    admin_user = User(username='admin', email='admin@college.edu', role='admin', name='Dean System Administrator')
    admin_user.set_password('admin123')
    db.session.add(admin_user)
    
    # Faculty
    f1 = User(username='dr_sharma', email='r.sharma@college.edu', role='faculty', name='Dr. Rajesh Sharma')
    f1.set_password('faculty123')
    f2 = User(username='prof_verma', email='a.verma@college.edu', role='faculty', name='Prof. Amit Verma')
    f2.set_password('faculty123')
    db.session.add_all([f1, f2])
    db.session.flush() # get IDs
    
    # Faculty Profiles
    fp1 = FacultyProfile(user_id=f1.id, department='Computer Applications', designation='Professor & HOD')
    fp2 = FacultyProfile(user_id=f2.id, department='Computer Applications', designation='Assistant Professor')
    db.session.add_all([fp1, fp2])
    
    # Students
    s1 = User(username='alice', email='alice.c@student.edu', role='student', name='Alice Cooper')
    s1.set_password('student123')
    s2 = User(username='bob', email='bob.m@student.edu', role='student', name='Bob Marley')
    s2.set_password('student123')
    s3 = User(username='charlie', email='charlie.p@student.edu', role='student', name='Charlie Puth')
    s3.set_password('student123')
    db.session.add_all([s1, s2, s3])
    db.session.flush()
    
    # 2. Create Courses & Batches
    c1 = Course(name='Master of Computer Applications', code='MCA', description='Post-graduate program in Computer Applications and Software Engineering.')
    c2 = Course(name='Bachelor of Technology', code='BTECH', description='Undergraduate engineering studies program.')
    db.session.add_all([c1, c2])
    db.session.flush()
    
    b1 = Batch(name='MCA 2024-2026', course_id=c1.id, year=2026)
    b2 = Batch(name='BTech 2023-2027', course_id=c2.id, year=2027)
    db.session.add_all([b1, b2])
    db.session.flush()
    
    # Student Profiles
    sp1 = StudentProfile(user_id=s1.id, roll_no='MCA24001', batch_id=b1.id, course_id=c1.id, phone='9876543210')
    sp2 = StudentProfile(user_id=s2.id, roll_no='MCA24002', batch_id=b1.id, course_id=c1.id, phone='8765432109')
    sp3 = StudentProfile(user_id=s3.id, roll_no='MCA24003', batch_id=b1.id, course_id=c1.id, phone='7654321098')
    db.session.add_all([sp1, sp2, sp3])
    db.session.flush()
    
    # 3. Create Subjects
    sub1 = Subject(name='Python Web Development', code='MCA-101', course_id=c1.id, faculty_id=f1.id)
    sub2 = Subject(name='Machine Learning & Analytics', code='MCA-102', course_id=c1.id, faculty_id=f1.id)
    sub3 = Subject(name='Advanced Database Systems', code='MCA-103', course_id=c1.id, faculty_id=f2.id)
    db.session.add_all([sub1, sub2, sub3])
    db.session.flush()
    
    # 4. Create Schedules
    scheds = [
        Schedule(subject_id=sub1.id, batch_id=b1.id, day_of_week='Monday', start_time='10:00 AM', end_time='12:00 PM', room='Lab 3'),
        Schedule(subject_id=sub2.id, batch_id=b1.id, day_of_week='Tuesday', start_time='09:00 AM', end_time='11:00 AM', room='L-201'),
        Schedule(subject_id=sub3.id, batch_id=b1.id, day_of_week='Wednesday', start_time='10:00 AM', end_time='12:00 PM', room='L-102'),
        Schedule(subject_id=sub1.id, batch_id=b1.id, day_of_week='Thursday', start_time='02:00 PM', end_time='04:00 PM', room='Lab 3'),
        Schedule(subject_id=sub2.id, batch_id=b1.id, day_of_week='Thursday', start_time='11:00 AM', end_time='01:00 PM', room='L-201'),
        Schedule(subject_id=sub3.id, batch_id=b1.id, day_of_week='Friday', start_time='09:00 AM', end_time='11:00 AM', room='L-102')
    ]
    db.session.add_all(scheds)
    
    # 5. Seed Attendance Logs (last 10 days of classes)
    # Alice: 90% attendance, Bob: 80%, Charlie: 50% (below 75% indicator)
    base_date = date.today()
    for offset in range(10):
        class_date = base_date - timedelta(days=offset)
        # Skip Sundays
        if class_date.weekday() == 6:
            continue
            
        for sub in [sub1, sub2, sub3]:
            # Alice: attends 90% (absent on offset=5)
            s1_status = 'Absent' if offset == 5 else 'Present'
            db.session.add(Attendance(student_id=sp1.id, subject_id=sub.id, date=class_date, status=s1_status))
            
            # Bob: attends 80% (absent on offset=3, 7)
            s2_status = 'Absent' if offset in [3, 7] else 'Present'
            db.session.add(Attendance(student_id=sp2.id, subject_id=sub.id, date=class_date, status=s2_status))
            
            # Charlie: attends 50% (absent on odd offsets)
            s3_status = 'Absent' if offset % 2 != 0 else 'Present'
            db.session.add(Attendance(student_id=sp3.id, subject_id=sub.id, date=class_date, status=s3_status))
            
    # 6. Seed Exam Marks
    # Alice (A+ student), Bob (B average), Charlie (Risk of fail)
    for sub in [sub1, sub2, sub3]:
        # Midterm 1
        db.session.add(Mark(student_id=sp1.id, subject_id=sub.id, exam_type='Midterm 1', marks_obtained=27, max_marks=30))
        db.session.add(Mark(student_id=sp2.id, subject_id=sub.id, exam_type='Midterm 1', marks_obtained=20, max_marks=30))
        db.session.add(Mark(student_id=sp3.id, subject_id=sub.id, exam_type='Midterm 1', marks_obtained=11, max_marks=30))
        
        # Midterm 2
        db.session.add(Mark(student_id=sp1.id, subject_id=sub.id, exam_type='Midterm 2', marks_obtained=28, max_marks=30))
        db.session.add(Mark(student_id=sp2.id, subject_id=sub.id, exam_type='Midterm 2', marks_obtained=18, max_marks=30))
        db.session.add(Mark(student_id=sp3.id, subject_id=sub.id, exam_type='Midterm 2', marks_obtained=12, max_marks=30))
        
        # Final Exams
        db.session.add(Mark(student_id=sp1.id, subject_id=sub.id, exam_type='Final Exam', marks_obtained=94, max_marks=100))
        db.session.add(Mark(student_id=sp2.id, subject_id=sub.id, exam_type='Final Exam', marks_obtained=73, max_marks=100))
        db.session.add(Mark(student_id=sp3.id, subject_id=sub.id, exam_type='Final Exam', marks_obtained=42, max_marks=100))
        
    # 7. Seed Tuition Fee Payments
    # Alice paid
    db.session.add(FeePayment(
        student_id=sp1.id, amount=65000.0, 
        payment_date=datetime.now() - timedelta(days=20),
        status='Paid', receipt_no='REC-MCA24001-9034', transaction_id='TXN-ALICECOOPER7842'
    ))
    # Bob paid
    db.session.add(FeePayment(
        student_id=sp2.id, amount=65000.0,
        payment_date=datetime.now() - timedelta(days=18),
        status='Paid', receipt_no='REC-MCA24002-4211', transaction_id='TXN-BOBMARLEY1094'
    ))
    # Charlie pending
    db.session.add(FeePayment(
        student_id=sp3.id, amount=65000.0,
        status='Pending', receipt_no='REC-MCA24003-DEF'
    ))
    
    db.session.commit()
    print("Database seeding completed successfully!")

if __name__ == '__main__':
    with app.app_context():
        seed_database()

from app import create_app
from models.models import db, User, Course, Batch, FacultyProfile, StudentProfile, Subject, FeePayment
from datetime import datetime

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
    p2 = FeePayment(student_id=sp2.id, amount=65000.0, status='Pending', receipt_no='REC-MCA24005-CSV')
    db.session.add_all([p1, p2])
    
    db.session.commit()
    print("Database seeding completed successfully (faculty and student demo accounts populated)!")

if __name__ == '__main__':
    with app.app_context():
        seed_database()

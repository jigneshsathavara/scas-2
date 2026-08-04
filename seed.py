from app import create_app
from models.models import db, User, Course, Batch, FacultyProfile, Subject, Schedule
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
    
    # 2. Create Courses & Batches
    c1 = Course(name='Master of Computer Applications', code='MCA', description='Post-graduate program in Computer Applications and Software Engineering.')
    c2 = Course(name='Bachelor of Technology', code='BTECH', description='Undergraduate engineering studies program.')
    db.session.add_all([c1, c2])
    db.session.flush()
    
    b1 = Batch(name='MCA 2024-2026', course_id=c1.id, year=2026)
    b2 = Batch(name='BTech 2023-2027', course_id=c2.id, year=2027)
    db.session.add_all([b1, b2])
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
    
    db.session.commit()
    print("Database seeding completed successfully (demo students removed)!")

if __name__ == '__main__':
    with app.app_context():
        seed_database()

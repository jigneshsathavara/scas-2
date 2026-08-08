from app import create_app
from models.models import db, User, Course, Batch
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
    c2 = Course(name='Bachelor of Technology', code='BTECH', description='Undergraduate engineering studies program.')
    db.session.add_all([c1, c2])
    db.session.flush()
    
    b1 = Batch(name='MCA 2024-2026', course_id=c1.id, year=2026)
    b2 = Batch(name='BTech 2023-2027', course_id=c2.id, year=2027)
    db.session.add_all([b1, b2])
    
    db.session.commit()
    print("Database seeding completed successfully (faculty and student data removed)!")

if __name__ == '__main__':
    with app.app_context():
        seed_database()

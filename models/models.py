from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'scas_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'faculty', 'student'
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    student_profile = db.relationship('StudentProfile', backref='user', uselist=False, cascade="all, delete-orphan")
    faculty_profile = db.relationship('FacultyProfile', backref='user', uselist=False, cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Course(db.Model):
    __tablename__ = 'scas_courses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    # Relationships
    batches = db.relationship('Batch', backref='course', cascade="all, delete-orphan")
    subjects = db.relationship('Subject', backref='course', cascade="all, delete-orphan")
    students = db.relationship('StudentProfile', backref='course', cascade="all, delete-orphan")

class Batch(db.Model):
    __tablename__ = 'scas_batches'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # e.g., 'MCA 2024-2026'
    course_id = db.Column(db.Integer, db.ForeignKey('scas_courses.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)     # e.g., 2026
    
    # Relationships
    students = db.relationship('StudentProfile', backref='batch', cascade="all, delete-orphan")
    schedules = db.relationship('Schedule', backref='batch', cascade="all, delete-orphan")

class FacultyProfile(db.Model):
    __tablename__ = 'scas_faculty_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('scas_users.id'), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)

class StudentProfile(db.Model):
    __tablename__ = 'scas_student_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('scas_users.id'), nullable=False)
    roll_no = db.Column(db.String(30), unique=True, nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('scas_batches.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('scas_courses.id'), nullable=False)
    phone = db.Column(db.String(20))
    
    # Relationships
    attendance_records = db.relationship('Attendance', backref='student', cascade="all, delete-orphan")
    marks = db.relationship('Mark', backref='student', cascade="all, delete-orphan")
    payments = db.relationship('FeePayment', backref='student', cascade="all, delete-orphan")

class Subject(db.Model):
    __tablename__ = 'scas_subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('scas_courses.id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('scas_users.id'), nullable=False)  # Link to faculty User
    
    # Relationships
    attendance_records = db.relationship('Attendance', backref='subject', cascade="all, delete-orphan")
    marks = db.relationship('Mark', backref='subject', cascade="all, delete-orphan")
    schedules = db.relationship('Schedule', backref='subject', cascade="all, delete-orphan")

class Schedule(db.Model):
    __tablename__ = 'scas_schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('scas_subjects.id'), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('scas_batches.id'), nullable=False)
    day_of_week = db.Column(db.String(20), nullable=False)  # 'Monday', 'Tuesday', etc.
    start_time = db.Column(db.String(10), nullable=False)   # '09:00 AM'
    end_time = db.Column(db.String(10), nullable=False)     # '10:00 AM'
    room = db.Column(db.String(20), nullable=False)

class Attendance(db.Model):
    __tablename__ = 'scas_attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('scas_student_profiles.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('scas_subjects.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)  # 'Present', 'Absent'

class Mark(db.Model):
    __tablename__ = 'scas_marks'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('scas_student_profiles.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('scas_subjects.id'), nullable=False)
    exam_type = db.Column(db.String(30), nullable=False)  # 'Midterm 1', 'Midterm 2', 'Final Exam', 'Assignment'
    marks_obtained = db.Column(db.Float, nullable=False)
    max_marks = db.Column(db.Float, nullable=False)

class FeePayment(db.Model):
    __tablename__ = 'scas_fee_payments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('scas_student_profiles.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False)  # 'Paid', 'Pending'
    receipt_no = db.Column(db.String(50), unique=True)
    transaction_id = db.Column(db.String(50), unique=True)

import unittest
from app import create_app
from models.models import db, User, StudentProfile, FacultyProfile
from datetime import date

class TestCollegeAnalyticsSystem(unittest.TestCase):
    
    def setUp(self):
        # Configure app to use testing flags and SQLite in-memory database
        self.app = create_app({
            'TESTING': True,
            'WTF_CSRF_ENABLED': False,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
        })
        self.client = self.app.test_client()
        
        # Open clean application context
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Seed the in-memory database for testing
        from seed import seed_database
        seed_database()
        
    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_unauthenticated_redirection(self):
        """Test that unauthenticated users are redirected to login."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/auth/login', response.headers['Location'])
        
        # Test direct page access gets blocked
        response_admin = self.client.get('/admin/dashboard')
        self.assertEqual(response_admin.status_code, 302)
        
        response_fac = self.client.get('/faculty/dashboard')
        self.assertEqual(response_fac.status_code, 302)
        
        response_stud = self.client.get('/student/dashboard')
        self.assertEqual(response_stud.status_code, 302)

    def test_database_records_seeded(self):
        """Test database connection and check seeded records exist."""
        # Ensure our seeds exist in DB
        admin_user = User.query.filter_by(username='admin').first()
        self.assertIsNotNone(admin_user)
        self.assertEqual(admin_user.role, 'admin')
        
        # Verify that demo students and faculty are empty
        faculty_count = User.query.filter_by(role='faculty').count()
        self.assertEqual(faculty_count, 0)
        
        student_count = User.query.filter_by(role='student').count()
        self.assertEqual(student_count, 0)

    def test_login_by_email_and_username(self):
        """Test logging in via email or username."""
        # Create a test user
        user = User(username='teststudent', email='teststudent@college.edu', role='student', name='Test Student')
        user.set_password('student123')
        db.session.add(user)
        db.session.commit()
        
        try:
            # Test login via username
            response_user = self.client.post('/auth/login', data={
                'username': 'teststudent',
                'password': 'student123'
            })
            self.assertEqual(response_user.status_code, 302)
            self.assertIn('/student/dashboard', response_user.headers['Location'])
            
            # Logout
            self.client.get('/auth/logout')
            
            # Test login via email
            response_email = self.client.post('/auth/login', data={
                'username': 'teststudent@college.edu',
                'password': 'student123'
            })
            self.assertEqual(response_email.status_code, 302)
            self.assertIn('/student/dashboard', response_email.headers['Location'])
        finally:
            # Clean up
            db.session.delete(user)
            db.session.commit()

    def test_admin_manual_user_creation_sends_email(self):
        """Test that manual student creation by admin triggers credentials email and formats it correctly."""
        # 1. Log in as admin
        self.client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        # 2. Remember the initial length of sent_emails.log
        import os
        from email_utils import LOG_FILE
        initial_log_content = ""
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                initial_log_content = f.read()
                
        # 3. Create a student manually
        response = self.client.post('/admin/users', data={
            'action': 'create',
            'username': 'testmanstudent',
            'name': 'Test Manual Student',
            'email': 'testmanstudent@college.edu',
            'password': 'tempPass123',
            'role': 'student',
            'roll_no': 'ROLL-TEST-MAN',
            'batch_id': 1,
            'course_id': 1,
            'phone': '9999999999'
        }, follow_redirects=True)
        
        # 4. Assert response was successful
        self.assertIn(b'Successfully created student user: Test Manual Student', response.data)
        
        # 5. Read LOG_FILE and find the newly appended email
        self.assertTrue(os.path.exists(LOG_FILE))
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            new_log_content = f.read()
            
        added_content = new_log_content[len(initial_log_content):]
        
        # Verify email contents
        self.assertIn('To: testmanstudent@college.edu (Test Manual Student)', added_content)
        self.assertIn('👉 Login ID (Email): testmanstudent@college.edu', added_content)
        self.assertIn('👉 Password: tempPass123', added_content)
        self.assertIn('⚠️ IMPORTANT NOTICE: This is a default/temporary password.', added_content)
        self.assertIn('For security reasons, you are kindly requested to log in and change your password immediately.', added_content)
        
        # Clean up database
        user = User.query.filter_by(username='testmanstudent').first()
        if user:
            db.session.delete(user)
            db.session.commit()

    def test_change_password(self):
        """Test changing a user's password via the /auth/change-password route."""
        # Create a test student and profile
        user = User(username='pwstudent', email='pwstudent@college.edu', role='student', name='PW Test Student')
        user.set_password('oldpass123')
        db.session.add(user)
        db.session.flush()
        
        profile = StudentProfile(user_id=user.id, roll_no='ROLL-PW-TEST', batch_id=1, course_id=1)
        db.session.add(profile)
        db.session.commit()
        
        try:
            # 1. Log in
            self.client.post('/auth/login', data={
                'username': 'pwstudent',
                'password': 'oldpass123'
            })
            
            # 2. Change password
            response = self.client.post('/auth/change-password', data={
                'current_password': 'oldpass123',
                'new_password': 'newpass123',
                'confirm_password': 'newpass123'
            }, follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Your password has been changed successfully.', response.data)
            
            # 3. Reload user from DB and check passwords
            db.session.expire(user)
            db.session.refresh(user)
            self.assertTrue(user.check_password('newpass123'))
            self.assertFalse(user.check_password('oldpass123'))
        finally:
            # Clean up
            db.session.delete(user)
            db.session.commit()

if __name__ == '__main__':
    print("Executing system verification tests...")
    unittest.main()

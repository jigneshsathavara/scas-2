import unittest
from app import create_app
from models.models import db, User, StudentProfile, FacultyProfile
from datetime import date

class TestCollegeAnalyticsSystem(unittest.TestCase):
    
    def setUp(self):
        # Configure app to use testing flags
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        
        # Open clean application context
        self.app_context = self.app.app_context()
        self.app_context.push()
        
    def tearDown(self):
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
        
        faculty = User.query.filter_by(username='dr_sharma').first()
        self.assertIsNotNone(faculty)
        self.assertEqual(faculty.role, 'faculty')
        self.assertIsNotNone(faculty.faculty_profile)
        
        student = User.query.filter_by(username='alice').first()
        self.assertIsNotNone(student)
        self.assertEqual(student.role, 'student')
        self.assertIsNotNone(student.student_profile)

if __name__ == '__main__':
    print("Executing system verification tests...")
    unittest.main()

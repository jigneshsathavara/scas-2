import unittest
from app import create_app
from models.models import db, User, StudentProfile, FacultyProfile, Subject, Result, Attendance
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
        
        # Verify that demo students and faculty counts match seeded state
        faculty_count = User.query.filter_by(role='faculty').count()
        self.assertEqual(faculty_count, 2)
        
        student_count = User.query.filter_by(role='student').count()
        self.assertEqual(student_count, 2)

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

    def test_forgot_password_flow(self):
        """Test requesting a password reset link and resetting the password."""
        # Create a test student
        user = User(username='resetstudent', email='resetstudent@college.edu', role='student', name='Reset Test Student')
        user.set_password('oldpass123')
        db.session.add(user)
        db.session.commit()
        
        try:
            # 1. Remember log size
            import os
            from email_utils import LOG_FILE
            initial_log_content = ""
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, 'r', encoding='utf-8') as f:
                    initial_log_content = f.read()
            
            # 2. Request forgot password
            response = self.client.post('/auth/forgot-password', data={
                'email': 'resetstudent@college.edu'
            }, follow_redirects=True)
            self.assertIn(b'A password reset link has been sent to your email. Check sent_emails.log!', response.data)
            
            # 3. Read sent_emails.log to extract the reset link
            self.assertTrue(os.path.exists(LOG_FILE))
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                new_log_content = f.read()
                
            added_content = new_log_content[len(initial_log_content):]
            self.assertIn('To: resetstudent@college.edu (Reset Test Student)', added_content)
            self.assertIn('👉 Reset Password Link:', added_content)
            
            # Extract token or link. Example link: http://localhost:5000/auth/reset-password/<token>
            import re
            link_match = re.search(r'👉 Reset Password Link:\s*(https?://[^\s\n]+)', added_content)
            self.assertIsNotNone(link_match, "Reset password link not found in email log")
            reset_link = link_match.group(1)
            
            # Extract the path from reset link (e.g. /auth/reset-password/<token>)
            parsed_path = '/' + reset_link.split('/', 3)[3]
            
            # 4. Get the reset page
            get_response = self.client.get(parsed_path)
            self.assertEqual(get_response.status_code, 200)
            self.assertIn(b'Reset Password', get_response.data)
            self.assertIn(b'New Password', get_response.data)
            
            # 5. Post the new password
            post_response = self.client.post(parsed_path, data={
                'new_password': 'newpassword123',
                'confirm_password': 'newpassword123'
            }, follow_redirects=True)
            self.assertIn(b'Your password has been reset successfully. Please log in.', post_response.data)
            
            # 6. Verify password updated in database
            db.session.expire(user)
            db.session.refresh(user)
            self.assertTrue(user.check_password('newpassword123'))
            self.assertFalse(user.check_password('oldpass123'))
            
            # 7. Verify we can log in with new password
            login_response = self.client.post('/auth/login', data={
                'username': 'resetstudent',
                'password': 'newpassword123'
            })
            self.assertEqual(login_response.status_code, 302)
            self.assertIn('/student/dashboard', login_response.headers['Location'])
            
        finally:
            # Clean up
            db.session.delete(user)
            db.session.commit()

    def test_upload_subjects_csv(self):
        """Test importing subjects and assigning faculty via CSV upload."""
        # 1. Log in as admin
        self.client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        # 2. Create a test faculty user
        faculty_user = User(username='testfac', email='testfac@college.edu', role='faculty', name='Test Faculty')
        faculty_user.set_password('fac123')
        db.session.add(faculty_user)
        db.session.flush()
        
        profile = FacultyProfile(user_id=faculty_user.id, department='Computer Applications', designation='Professor')
        db.session.add(profile)
        db.session.commit()
        
        try:
            # 3. Simulate uploading a CSV file
            import io
            csv_data = (
                "subject_code,subject_name,course_code,faculty_email\n"
                "MCA-801,Advanced AI and Agents,MCA,testfac@college.edu\n"
            )
            
            response = self.client.post('/admin/courses/upload/subjects', data={
                'file': (io.BytesIO(csv_data.encode('utf-8')), 'subjects.csv')
            }, content_type='multipart/form-data', follow_redirects=True)
            
            # Assert successful flash message
            self.assertIn(b'Subjects CSV Upload complete! Imported/Updated: 1, Skipped: 0.', response.data)
            
            # 4. Query DB to verify Subject creation and assignment
            subject = Subject.query.filter_by(code='MCA-801').first()
            self.assertIsNotNone(subject)
            self.assertEqual(subject.name, 'Advanced AI and Agents')
            self.assertEqual(subject.faculty_id, faculty_user.id)
            
        finally:
            # Clean up
            subject = Subject.query.filter_by(code='MCA-801').first()
            if subject:
                db.session.delete(subject)
            db.session.delete(faculty_user)
            db.session.commit()

    def test_upload_subjects_csv_missing_faculty(self):
        """Test that uploading a subject with a non-existent faculty triggers a warning notification."""
        # 1. Log in as admin
        self.client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        # 2. Simulate uploading a CSV file with a non-existent faculty email
        import io
        csv_data = (
            "subject_code,subject_name,course_code,faculty_email\n"
            "MCA-999,Quantum Computing,MCA,nonexistent_fac@college.edu\n"
        )
        
        response = self.client.post('/admin/courses/upload/subjects', data={
            'file': (io.BytesIO(csv_data.encode('utf-8')), 'subjects.csv')
        }, content_type='multipart/form-data', follow_redirects=True)
        
        # Assert flash message contains warning about missing faculty
        self.assertIn(b'Warning: The following faculty emails do not exist: nonexistent_fac@college.edu.', response.data)
        
        # Assert subject was not imported
        subject = Subject.query.filter_by(code='MCA-999').first()
        self.assertIsNone(subject)

    def test_results_system_flow(self):
        """Test uploading student results via CSV as admin and viewing/calculating SGPA and CGPA as student."""
        # 1. Log in as admin
        self.client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        # 2. Create test student, course, batch, subject
        student_user = User(username='testgpa', email='testgpa@college.edu', role='student', name='GPA Test Student')
        student_user.set_password('student123')
        db.session.add(student_user)
        db.session.flush()
        
        student_profile = StudentProfile(user_id=student_user.id, roll_no='MCA-TEST-GPA', course_id=1, batch_id=1)
        db.session.add(student_profile)
        
        faculty_user = User(username='testfac2', email='testfac2@college.edu', role='faculty', name='Test Faculty Two')
        faculty_user.set_password('fac123')
        db.session.add(faculty_user)
        db.session.flush()
        
        profile = FacultyProfile(user_id=faculty_user.id, department='Computer Applications', designation='Professor')
        db.session.add(profile)
        db.session.flush()
        
        sub1 = Subject(name='Subject 1', code='MCA-901', course_id=1, faculty_id=faculty_user.id)
        sub2 = Subject(name='Subject 2', code='MCA-902', course_id=1, faculty_id=faculty_user.id)
        db.session.add_all([sub1, sub2])
        db.session.commit()
        
        try:
            # 3. Simulate uploading results CSV
            import io
            csv_data = (
                "roll_no,student_name,semester,sub1_code,sub1_marks,sub1_max,sub1_credits,sub2_code,sub2_marks,sub2_max,sub2_credits\n"
                "MCA-TEST-GPA,GPA Test Student,1,MCA-901,85,100,4,MCA-902,72,100,4\n"
            )
            
            upload_response = self.client.post('/admin/results/upload', data={
                'file': (io.BytesIO(csv_data.encode('utf-8')), 'results.csv')
            }, content_type='multipart/form-data', follow_redirects=True)
            
            # Assert successful flash message
            self.assertIn(b'Results CSV Upload complete! Imported/Updated: 2 subject grades, Skipped/Invalid entries: 0.', upload_response.data)
            
            # 4. Query DB to verify Results creation
            res1 = Result.query.filter_by(student_id=student_profile.id, subject_id=sub1.id).first()
            self.assertIsNotNone(res1)
            self.assertEqual(res1.marks_obtained, 85.0)
            self.assertEqual(res1.semester, 1)
            
            # 5. Log in as student to check calculations
            self.client.get('/auth/logout')
            self.client.post('/auth/login', data={
                'username': 'testgpa',
                'password': 'student123'
            })
            
            # Get Results page
            results_response = self.client.get('/student/results')
            self.assertEqual(results_response.status_code, 200)
            self.assertIn(b'SGPA: 8.5', results_response.data)
            self.assertIn(b'8.5 / 10.00', results_response.data)
            
            # Verify CSV download route works
            download_response = self.client.get('/student/results/download')
            self.assertEqual(download_response.status_code, 200)
            self.assertEqual(download_response.headers['Content-Type'], 'text/csv')
            self.assertIn(b'MCA-901', download_response.data)
            self.assertIn(b'MCA-902', download_response.data)
            
        finally:
            # Clean up
            Result.query.filter_by(student_id=student_profile.id).delete()
            db.session.delete(sub1)
            db.session.delete(sub2)
            db.session.delete(student_user)
            db.session.delete(faculty_user)
            db.session.commit()

    def test_attendance_management_flow(self):
        """Test Admin managing attendance and student viewing and downloading attendance records."""
        # 1. Log in as admin
        self.client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        # 2. Get admin attendance panel
        response = self.client.get('/admin/attendance?subject_id=1&batch_id=1&date=2026-08-08')
        self.assertEqual(response.status_code, 200)
        
        # 3. Post attendance log as Admin (student profile 1 has ID 1)
        response_post = self.client.post('/admin/attendance', data={
            'subject_id': 1,
            'batch_id': 1,
            'date': '2026-08-08',
            'status_1': 'on'  # present
        }, follow_redirects=True)
        self.assertIn(b'Attendance recorded for date: 2026-08-08', response_post.data)
        
        # Verify db log
        att = Attendance.query.filter_by(student_id=1, subject_id=1, date=date(2026, 8, 8)).first()
        self.assertIsNotNone(att)
        self.assertEqual(att.status, 'Present')
        
        # 4. Log in as student to check view & download
        self.client.get('/auth/logout')
        self.client.post('/auth/login', data={
            'username': 'goswami@college.edu',
            'password': 'SCASStudent123'
        })
        
        # View attendance
        student_response = self.client.get('/student/attendance')
        self.assertEqual(student_response.status_code, 200)
        self.assertIn(b'My Attendance Registry', student_response.data)
        self.assertIn(b'Overall Attendance Rate', student_response.data)
        
        # Download report
        download_response = self.client.get('/student/attendance/download')
        self.assertEqual(download_response.status_code, 200)
        self.assertEqual(download_response.headers['Content-Type'], 'text/csv')
        self.assertIn(b'Date,Subject Code,Subject Name,Status', download_response.data)
        self.assertIn(b'2026-08-08', download_response.data)
        
        # Clean up
        Attendance.query.filter_by(student_id=1, subject_id=1, date=date(2026, 8, 8)).delete()
        db.session.commit()

if __name__ == '__main__':
    print("Executing system verification tests...")
    unittest.main()

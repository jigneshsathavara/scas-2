# Smart College Analytics System (SCAS)

An enterprise-grade, role-based academic management and student performance analytics portal built with **Flask**, **SQLAlchemy**, and **MySQL / MariaDB**, featuring machine learning risk prediction models and automated email communications.

---

## 📌 Project Architecture & Highlights

- **Backend Framework**: Python 3.12+ / Flask 3.0.3 with Modular Blueprints
- **Database Engine**: **MySQL / MariaDB** (Default: `localhost:3306/scas_db`) via `PyMySQL` and `Flask-SQLAlchemy`
- **Analytics & AI Engine**: `scikit-learn`, `pandas`, `numpy` for predictive dropout & academic risk evaluation
- **Security & Auth**: Role-Based Access Control (RBAC), password hashing via `werkzeug.security`, timed token password resets via `itsdangerous`
- **Communication Engine**: SMTP Email delivery with fallback to transactional mock logging (`sent_emails.log`)
- **Frontend**: Full-Stack Jinja2 Templates styled with responsive CSS and Lucide icons; optional standalone React 19 + TypeScript SPA in `src/`

---

## 🏛️ Comprehensive Module Breakdown

### 1. Authentication & Security Module (`routes/auth.py`)
- **Role-Based Access Control**: Strict route protection via `@login_required` and `@role_required(['admin', 'faculty', 'student'])`.
- **Flexible Login**: Supports authentication via either username or institutional email.
- **Secure Password Resets**: Cryptographically signed URL tokens with 1-hour expiration; password reset notifications sent via email.
- **Password Management**: In-app self-service password update for all authenticated users.

### 2. Administrator Management Module (`routes/admin.py`)
- **Executive Analytics Dashboard**: Real-time KPI counters (total students, faculty, active courses, fee revenue, and pending dues), dynamic enrolment distribution charts, and recent activity feeds.
- **User Account Management**: Create, edit, and delete accounts for students and faculty.
- **Automated Credential Dispatch**: Single-click actions to generate temporary passwords and email credentials to individual or all users simultaneously.
- **Academic Setup**: Complete lifecycle management of Degree Programs (`scas_courses`), Batches (`scas_batches`), and Subjects (`scas_subjects`).
- **Bulk CSV Import Engine**: Batch upload faculties, students, subjects, and examination marks via CSV with automated validation and error logging.
- **Examination & Results Controller**: Calculates SGPA/CGPA, letter grades (`O`, `A+`, `A`, `B+`, `B`, `C`, `F`), credits, and generates transcripts.
- **Financial & Fee Management**: Audit fee statuses, view transaction IDs, generate fee receipts, and export reports in CSV and print formats.
- **Leave Applications Management**: Centralized approval/rejection workflow for student and faculty leave requests.

### 3. Faculty Portal Module (`routes/faculty.py`)
- **Faculty Dashboard**: Overview of assigned subjects, timetable schedule, and **AI Student Risk Alerts**.
- **Predictive AI Risk Modeling**: Analyzes individual student attendance rates and midterm scores using weighted decision heuristics (45% attendance, 55% academic scores) to classify students into `High Risk`, `Medium Risk`, or `Low Risk` categories.
- **Daily Attendance Register**: Mark class attendance per subject and batch with present/absent statuses.
- **Marks & Evaluation Entry**: Record continuous assessments across `Midterm 1`, `Midterm 2`, `Final Exam`, and `Assignment`.
- **Lecture Scheduling**: Configure class timetables with day of week, time slots, and lecture room assignments.
- **Reporting & Exports**: Export attendance sheets and marks registers to CSV or print-ready layouts.

### 4. Student Portal Module (`routes/student.py`)
- **Student Dashboard**: Live overview of overall attendance percentage, cumulative GPA, today's schedule, and fee alerts.
- **My Academics**: Detailed breakdown of subject-wise attendance logs and exam scores.
- **Fee Payment Gateway**: Interactive simulated payment gateway with receipt number and transaction ID generation.
- **Official Semester Results**: View semester scorecards with subject grades, grade points, and semester SGPA.
- **Attendance Record Viewer**: Complete historical attendance log with status indicators and CSV export.
- **Leave Application Center**: Submit leave requests with reason and date range; track approval status in real time.

---

## 🗄️ Database Architecture (MySQL)

The application utilizes **MySQL / MariaDB** database `scas_db` with relational constraints, foreign keys, and cascading deletes.

### Table Schema Summary:
1. `scas_users`: System user credentials, email, role, and names.
2. `scas_courses`: Degree programs (e.g. Master of Computer Applications).
3. `scas_batches`: Academic cohorts (e.g. MCA 2024-2026).
4. `scas_faculty_profiles`: Department and designation metadata.
5. `scas_student_profiles`: Roll numbers, batch mappings, and contact numbers.
6. `scas_subjects`: Subject names, codes, course mappings, and assigned faculty.
7. `scas_schedules`: Timetable scheduling with days, times, and room numbers.
8. `scas_attendance`: Date-stamped attendance logs (`Present` / `Absent`).
9. `scas_marks`: Internal assessments, midterms, and finals marks.
10. `scas_fee_payments`: Fee billing records, receipts, and payment transactions.
11. `scas_results`: Final semester grade records with credit weightings.
12. `scas_leave_applications`: Leave requests, date ranges, reasons, and approval statuses.
13. `scas_test_assessments`: Unit-wise mastery assessment scores and evaluations.

---

## 🚀 Setup & Execution Guide

### Prerequisites
- Python 3.10+ (Python 3.12 recommended)
- MySQL / MariaDB (e.g., via **XAMPP**, WampServer, or standalone MySQL service)

### 1. Configure Database Connection
Ensure MySQL is running on `localhost:3306`. Connection credentials are configured in `.env`:
```ini
DATABASE_URL=mysql+pymysql://root:@localhost:3306/scas_db
SECRET_KEY=smart_college_secret_key_129847
```
*(The system automatically detects MySQL, creates `scas_db` if not present, and connects seamlessly).*

### 2. Install Dependencies
```bash
pip install -r requirements.txt
pip install python-dotenv
```

### 3. Seed MySQL Database with Demo Data
Run the database seeder to create all tables and populate realistic demonstration records:
```bash
python seed.py
```
*(Or double-click `setup_mysql.bat` on Windows)*

### 4. Start the Application Server
```bash
python app.py
```
*(Or double-click `run_server.bat` on Windows)*

The application will be live at:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🔑 Pre-Configured Demo Accounts

| Role | Username / Email | Password | Dashboard Features |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` *(or `admin@college.edu`)* | `admin123` | Full ERP Control, Users, Courses, Results, Attendance, Leaves |
| **Faculty** | `cdpatel@college.edu` | `SCASFaculty123` | Class Attendance, Marks Entry, Lecture Schedule, AI Risk Alerts |
| **Faculty** | `sanjaybhai@college.edu` | `SCASFaculty123` | Compiler Design evaluation, schedules, and class attendance |
| **Student** | `goswami@college.edu` | `SCASStudent123` | Roll No: `MCA24004`, Academics, Fee Payment, Results, Attendance, Leaves |
| **Student** | `sathavara@college.edu` | `SCASStudent123` | Roll No: `MCA24005`, Academics, Paid Fee Receipt, Results, Attendance |

---

## 🧪 Automated Test Suite Verification

Run the comprehensive unit test suite to verify all core workflows:
```bash
python -m unittest verify_system.py
```
**Results**: 100% tests pass (Authentication, RBAC access control, DB seeding, student creation, email dispatch, and grade calculations).

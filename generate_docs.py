import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_document():
    doc = docx.Document()

    # Define color palette
    PRIMARY_COLOR = RGBColor(26, 54, 93)     # Deep Navy (#1A365D)
    SECONDARY_COLOR = RGBColor(49, 130, 206) # Blue Accent (#3182CE)
    DARK_TEXT = RGBColor(45, 55, 72)         # Slate Gray (#2D3748)
    MUTED_TEXT = RGBColor(113, 128, 150)     # Muted Gray (#718096)

    # Set Margins
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Base Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Segoe UI'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = DARK_TEXT

    # Helper Functions
    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.name = 'Segoe UI'
        run.font.size = Pt(26)
        run.font.bold = True
        run.font.color.rgb = PRIMARY_COLOR

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(24)
        run = p.add_run(text)
        run.font.name = 'Segoe UI'
        run.font.size = Pt(14)
        run.font.italic = True
        run.font.color.rgb = SECONDARY_COLOR

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Segoe UI'
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = PRIMARY_COLOR

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Segoe UI'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = SECONDARY_COLOR

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Segoe UI'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = PRIMARY_COLOR

    def add_p(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = 'Segoe UI'
        run.font.size = Pt(11)
        run.font.color.rgb = DARK_TEXT
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            run_b = p.add_run(bold_prefix)
            run_b.font.name = 'Segoe UI'
            run_b.font.bold = True
            run_b.font.color.rgb = PRIMARY_COLOR
        run = p.add_run(text)
        run.font.name = 'Segoe UI'
        run.font.color.rgb = DARK_TEXT

    def add_callout(text, title="NOTE"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        
        # Set shading background
        shading = parse_xml(r'<w:shd {} w:fill="EBF8FF"/>'.format(nsdecls('w')))
        cell._tc.get_or_add_tcPr().append(shading)
        
        # Set left border thick blue, others none
        borders = parse_xml(r'''
            <w:tcBorders {} >
                <w:top w:val="none"/>
                <w:left w:val="single" w:sz="36" w:space="0" w:color="3182CE"/>
                <w:bottom w:val="none"/>
                <w:right w:val="none"/>
            </w:tcBorders>
        '''.format(nsdecls('w')))
        cell._tc.get_or_add_tcPr().append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.left_indent = Inches(0.1)
        
        r_t = p.add_run(f"📌 {title}: ")
        r_t.bold = True
        r_t.font.color.rgb = SECONDARY_COLOR
        
        r_b = p.add_run(text)
        r_b.font.color.rgb = DARK_TEXT
        
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    def style_table(table, col_widths, headers, data):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        hdr_cells = table.rows[0].cells
        for i, header in enumerate(headers):
            hdr_cells[i].text = header
            hdr_cells[i].width = Inches(col_widths[i])
            # Shading header
            shd = parse_xml(r'<w:shd {} w:fill="1A365D"/>'.format(nsdecls('w')))
            hdr_cells[i]._tc.get_or_add_tcPr().append(shd)
            p = hdr_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = 'Segoe UI'
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
                run.font.size = Pt(10)

        for row_idx, row_data in enumerate(data):
            row_cells = table.add_row().cells
            bg_color = "F7FAFC" if row_idx % 2 == 1 else "FFFFFF"
            for col_idx, cell_value in enumerate(row_data):
                row_cells[col_idx].text = str(cell_value)
                row_cells[col_idx].width = Inches(col_widths[col_idx])
                shd = parse_xml(r'<w:shd {} w:fill="{}"/>'.format(nsdecls('w'), bg_color))
                row_cells[col_idx]._tc.get_or_add_tcPr().append(shd)
                p = row_cells[col_idx].paragraphs[0]
                for run in p.runs:
                    run.font.name = 'Segoe UI'
                    run.font.size = Pt(9.5)
                    run.font.color.rgb = DARK_TEXT

    # -------------------------------------------------------------
    # DOCUMENT CONTENT GENERATION
    # -------------------------------------------------------------

    # Title & Metadata
    add_title("Smart College Analytics System (SCAS)")
    add_subtitle("Comprehensive System Specification, Database Schema & Architecture Guide")

    add_callout(
        "This document contains the complete structural, technical, and operational documentation for the Smart College Analytics System (SCAS / MCA-PS3).",
        "DOCUMENT METADATA"
    )

    # 1. Executive Overview
    add_h1("1. Executive Summary & System Overview")
    add_p("The Smart College Analytics System (SCAS) is an enterprise-grade higher education ERP (Enterprise Resource Planning) and academic performance portal designed for modern academic institutions. It provides a multi-tenant, role-based ecosystem for Managing Administrators, Academic Faculty, and Enrolled Students.")
    add_p("SCAS bridges administrative management, academic monitoring, real-time attendance tracking, continuous internal assessments, fee processing, and placement readiness into a unified digital platform.")

    add_h2("Key Goals of the Platform")
    add_bullet(" Automation of manual attendance entry, internal mark calculations, and fee receipt generation.", "1. Operational Efficiency:")
    add_bullet(" Interactive charts and performance dashboards providing instant insights into student GPAs and subject-level trends.", "2. Academic Performance Analytics:")
    add_bullet(" Dedicated modules for placement training, mock aptitude exams, and performance tracking.", "3. Career Readiness:")
    add_bullet(" Digital submission and multi-tier approval workflows for student leave and duty applications.", "4. Transparent Workflows:")

    # 2. System Architecture
    add_h1("2. System Architecture & Tech Stack")
    add_p("SCAS is engineered with a hybrid dual-architecture pattern combining a robust Python/Flask backend API with a modern React + TypeScript single-page application (SPA) frontend.")

    headers_tech = ["Layer", "Technologies", "Description / Responsibilities"]
    tech_data = [
        ["Frontend UI", "React 19, TypeScript, Vite, Tailwind CSS", "Responsive SPA with interactive dashboards, dark theme glassmorphic UI, Lucide icons, and Canvas Confetti."],
        ["Data Visualization", "Chart.js, react-chartjs-2", "Renders dynamic GPA progression graphs, attendance distribution charts, and mark breakdown radar visualizers."],
        ["Backend API", "Python 3.x, Flask, Flask-SQLAlchemy", "RESTful API services, session-based role authentication, template filters, and business logic controllers."],
        ["Database Layer", "MySQL / SQLite, SQLAlchemy ORM", "Relational database schema storing users, profiles, courses, batches, subjects, marks, attendance, and fee transactions."],
        ["Email & Notifications", "Python smtplib, MIME, Sent Email Logger", "Transports welcome credentials, password resets, and alert notifications with real SMTP and local fallback options."]
    ]
    t_tech = doc.add_table(rows=1, cols=3)
    style_table(t_tech, [1.5, 2.2, 2.8], headers_tech, tech_data)

    # 3. Directory Structure
    add_h1("3. Project Directory & File Index")
    add_p("The project structure separates frontend assets, backend blueprints, database models, utilities, and configuration files clearly:")

    headers_files = ["Directory / File", "Type", "Purpose & Description"]
    files_data = [
        ["app.py", "Python File", "Application entry point. Initializes Flask app, registers blueprints, configures database connection, and custom template filters."],
        ["config.py", "Python File", "Configuration class loading environment variables (.env) for database connection strings and SMTP mail server settings."],
        ["models/models.py", "ORM Models", "SQLAlchemy relational schema defining 12 database entities including User, StudentProfile, FacultyProfile, Attendance, and FeePayment."],
        ["routes/auth.py", "Flask Blueprint", "Authentication endpoints for user login, logout, and session role handling."],
        ["routes/admin.py", "Flask Blueprint", "Administrative endpoints for student/faculty registration, fee tracking, and notice board management."],
        ["routes/faculty.py", "Flask Blueprint", "Faculty management endpoints for taking attendance, uploading exam marks, and managing aptitude tests."],
        ["routes/student.py", "Flask Blueprint", "Student portal endpoints for viewing marks, checking attendance, applying for leave, and taking tests."],
        ["email_utils.py", "Python Utility", "Mail delivery engine capable of dispatching HTML/Plain emails via SMTP and logging deliveries to sent_emails.log."],
        ["seed.py", "Python Script", "Database seeder creating demo accounts, sample courses (MCA), batches, subjects, and initial test data."],
        ["verify_system.py", "Python Diagnostic", "Comprehensive system diagnostic script checking DB connection, table integrity, sample data, and email transport."],
        ["src/App.tsx", "React Component", "Main React application container managing global ERP state, local storage persistence, role toggles, and view routing."],
        ["src/pages/*", "React Pages", "Role-segmented page components (AdminDashboard, FacultyTakeAttendance, StudentAnalytics, etc.)."],
        ["database.sql", "SQL File", "Native MySQL schema DDL script containing table creations, constraints, foreign keys, and indexes."]
    ]
    t_files = doc.add_table(rows=1, cols=3)
    style_table(t_files, [1.8, 1.4, 3.3], headers_files, files_data)

    # 4. Database Schema
    add_h1("4. Relational Database Schema & Entities")
    add_p("The SCAS database (`scas_db`) uses a fully normalized relational schema consisting of 12 interconnected tables:")

    headers_db = ["Table Name", "Primary Key", "Foreign Keys", "Description"]
    db_data = [
        ["scas_users", "id", "None", "Stores authentication credentials (username, password_hash, email) and system role ('admin', 'faculty', 'student')."],
        ["scas_courses", "id", "None", "Defines academic degree programs (e.g. Master of Computer Applications - MCA)."],
        ["scas_batches", "id", "course_id", "Groups students into academic years (e.g., MCA 2024-2026)."],
        ["scas_faculty_profiles", "id", "user_id", "Faculty member metadata including department and academic designation."],
        ["scas_student_profiles", "id", "user_id, batch_id, course_id", "Student demographic profile, roll number, phone number, and academic links."],
        ["scas_subjects", "id", "course_id, faculty_id", "Curriculum subjects assigned to specific faculty members."],
        ["scas_schedules", "id", "subject_id, batch_id", "Timetable entries specifying days, rooms, and start/end time slots."],
        ["scas_attendance", "id", "student_id, subject_id", "Daily student attendance records marked as 'Present' or 'Absent' with timestamps."],
        ["scas_marks", "id", "student_id, subject_id", "Internal evaluation scores across Midterm 1, Midterm 2, Assignments, and Final Exams."],
        ["scas_fee_payments", "id", "student_id", "Fee transaction logs including transaction ID, receipt number, amount, and status ('Paid'/'Pending')."],
        ["scas_results", "id", "student_id, subject_id", "Semester grade sheets tracking obtained marks, max marks, and earned course credits."],
        ["scas_leave_applications", "id", "user_id", "Student and faculty leave requests storing date ranges, reason, and approval status."]
    ]
    t_db = doc.add_table(rows=1, cols=4)
    style_table(t_db, [1.6, 0.9, 1.8, 2.2], headers_db, db_data)

    # 5. User Roles & Detailed Features
    add_h1("5. Detailed Feature Breakdown by Role")

    add_h2("5.1 Student Portal")
    add_bullet(" Displays current GPA, overall attendance percentage, fee status, and recent institutional notices.", "Dashboard Summary: ")
    add_bullet(" Breakdown of marks by subject, midterm performance, assignment scores, and final exam grades.", "Marks & Grade Sheets: ")
    add_bullet(" Subject-wise attendance breakdown with visual indicators for attendance risks (<75%).", "Attendance Tracker: ")
    add_bullet(" Interactive graphs powered by Chart.js displaying semester GPA progression and subject comparison.", "Academic Analytics: ")
    add_bullet(" Take mock placement aptitude tests, view test results, and track competitive leaderboards.", "Placement & Aptitude: ")
    add_bullet(" Submit leave and duty applications with reasons, start/end dates, and monitor approval status.", "Leave Applications: ")

    add_h2("5.2 Faculty Portal")
    add_bullet(" Overview of assigned courses, student counts, and quick action shortcuts.", "Faculty Dashboard: ")
    add_bullet(" View directory of enrolled students with contact numbers and performance records.", "Student Directory: ")
    add_bullet(" Mark daily student attendance per subject and batch with instant database synchronization.", "Attendance Entry: ")
    add_bullet(" Upload and edit internal marks, midterm scores, and final assessment grades.", "Marks Upload: ")
    add_bullet(" Create custom multiple-choice aptitude exams for placement preparation.", "Aptitude Exam Builder: ")
    add_bullet(" Review, approve, or reject pending student leave requests.", "Application Review: ")

    add_h2("5.3 Administrator Portal")
    add_bullet(" High-level institutional metrics including total enrolled students, faculty strength, overall attendance %, and fee collections.", "Admin Dashboard: ")
    add_bullet(" Register new student and faculty accounts, trigger automated welcome email credentials, and edit profiles.", "User Management: ")
    add_bullet(" Broadcast official college announcements, pin urgent notices, and delete expired notices.", "Notice Board: ")
    add_bullet(" Track tuition fee payments, verify transaction IDs, generate official receipt numbers, and update payment statuses.", "Fee Management: ")
    add_bullet(" Run system-wide data integrity checks (`verify_system.py`) and trigger database seeders.", "System Operations: ")

    # 6. Setup & Verification
    add_h1("6. Installation, Configuration & Verification Guide")

    add_h2("Step 1: Environment Setup")
    add_p("Clone the repository, create a virtual environment, and install required Python and Node.js packages:")
    add_bullet("python -m venv .venv && .\\.venv\\Scripts\\activate", "Python Virtualenv: ")
    add_bullet("pip install -r requirements.txt", "Backend Dependencies: ")
    add_bullet("npm install", "Frontend Dependencies: ")

    add_h2("Step 2: Database Initialization & Seeding")
    add_p("Execute the database seeder to create sample admin, faculty, and student accounts with realistic course data:")
    add_bullet("python seed.py", "Run Database Seeder: ")

    add_h2("Step 3: System Diagnostic Verification")
    add_p("SCAS includes a self-testing suite (`verify_system.py`) that executes 10 comprehensive verification steps:")
    add_bullet("Verifies Database Connection & SQLAlchemy ORM.", "1. DB Connection Test: ")
    add_bullet("Validates presence of all 12 required tables.", "2. Table Integrity Check: ")
    add_bullet("Confirms existence of default Admin ('admin'), Faculty ('prof_sharma'), and Student ('mca_rahul') accounts.", "3. Sample User Check: ")
    add_bullet("Tests mock email dispatch and sent_emails.log file writing.", "4. Email Transport Test: ")

    add_h2("Step 4: Launching Servers")
    add_bullet("python app.py  (Runs on http://127.0.0.1:5000)", "Start Flask Backend: ")
    add_bullet("npm run dev  (Runs on http://localhost:5173)", "Start Vite Frontend: ")

    # Save Document
    doc_path = os.path.join(os.getcwd(), "SCAS_Project_Documentation.docx")
    doc.save(doc_path)
    print(f"Document successfully created at: {doc_path}")

if __name__ == "__main__":
    create_document()

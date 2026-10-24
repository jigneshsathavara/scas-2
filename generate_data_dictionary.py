"""
Generate SCAS Data Dictionary PDF matching the exact 'Data Dict Demo' format
from media_1791016747998.png.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# --- Canvas for Running Headers and Footers ---
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        # Top Header (Only on content pages, after cover if needed)
        self.setFont('Helvetica-Bold', 9)
        self.setFillColor(colors.HexColor('#1E293B'))
        self.drawString(36, 812, "Student Central Administrative System (SCAS)")
        self.setFont('Helvetica', 9)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawRightString(559, 812, "Section 4.2 Data Dictionary")
        
        # Header dividing rule
        self.setStrokeColor(colors.HexColor('#CBD5E1'))
        self.setLineWidth(0.75)
        self.line(36, 804, 559, 804)

        # Bottom Footer
        self.setFont('Helvetica-Bold', 8.5)
        self.setFillColor(colors.HexColor('#B91C1C')) # Ganpat University primary maroon
        self.drawString(36, 28, "Ganpat University | AMPICS")
        self.setFont('Helvetica', 8)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawString(180, 28, "•   BCA / MCA Project Technical Documentation")
        self.drawRightString(559, 28, f"Page {self._pageNumber} of {page_count}")
        
        # Footer dividing rule
        self.setStrokeColor(colors.HexColor('#CBD5E1'))
        self.setLineWidth(0.75)
        self.line(36, 38, 559, 38)
        self.restoreState()


# --- Full Table Data Specifications ---
DATA_DICTIONARY_TABLES = [
    {
        "table_no": "4.2.1",
        "table_name": "scas_users",
        "description": "Stores system authentication credentials, user identity profiles, role-based access control (RBAC), and account creation timestamps for administrative, faculty, and student users.",
        "constraints": "id (PK), username (UNIQUE, NOT NULL), password_hash (NOT NULL), email (UNIQUE, NOT NULL), role (NOT NULL), name (NOT NULL), created_at (NOT NULL, DEFAULT CURRENT_TIMESTAMP)",
        "fields": [
            ("1", "id", "INT", "11", "PK, AUTO_INCREMENT, NOT NULL", "Unique internal synthetic user identifier; primary key."),
            ("2", "username", "VARCHAR", "80", "UNIQUE, NOT NULL", "System login identifier; globally unique across all system roles."),
            ("3", "password_hash", "VARCHAR", "255", "NOT NULL", "Cryptographic password hash generated via Scrypt (Werkzeug security)."),
            ("4", "email", "VARCHAR", "120", "UNIQUE, NOT NULL", "Primary contact email address; globally unique; used for notices & resets."),
            ("5", "role", "VARCHAR", "20", "NOT NULL", "Role-Based Access Control enum: 'admin', 'faculty', or 'student'."),
            ("6", "name", "VARCHAR", "100", "NOT NULL", "Full legal name of the user for institutional records & certificates."),
            ("7", "created_at", "DATETIME", "-", "NOT NULL, DEFAULT CURRENT_TIMESTAMP", "UTC timestamp recording account creation time.")
        ]
    },
    {
        "table_no": "4.2.2",
        "table_name": "scas_courses",
        "description": "Stores academic degree programs, program identification codes, and comprehensive curriculum syllabus guidelines.",
        "constraints": "id (PK), code (UNIQUE, NOT NULL), name (NOT NULL), description (NULL)",
        "fields": [
            ("1", "id", "INT", "11", "PK, AUTO_INCREMENT, NOT NULL", "Unique identifier for the degree program / course."),
            ("2", "name", "VARCHAR", "100", "NOT NULL", "Full academic degree name (e.g., 'Master of Computer Applications')."),
            ("3", "code", "VARCHAR", "20", "UNIQUE, NOT NULL", "Short unique institutional course code (e.g., 'MCA', 'BCA', 'B.Tech')."),
            ("4", "description", "TEXT", "-", "NULL", "Detailed curriculum overview, program syllabus objectives, and guidelines.")
        ]
    },
    {
        "table_no": "4.2.3",
        "table_name": "scas_batches",
        "description": "Stores academic cohort batches, section designations, graduation/completion calendar years, and degree program associations.",
        "constraints": "id (PK), course_id (FK, NOT NULL), name (NOT NULL), year (NOT NULL)",
        "fields": [
            ("1", "id", "INT", "11", "PK, AUTO_INCREMENT, NOT NULL", "Unique identifier for academic cohort batch."),
            ("2", "name", "VARCHAR", "50", "NOT NULL", "Cohort identifier name (e.g., 'MCA 2024-2026', 'MCA Section A')."),
            ("3", "course_id", "INT", "11", "FK, NOT NULL", "Foreign key referencing scas_courses(id) ON DELETE CASCADE."),
            ("4", "year", "INT", "11", "NOT NULL", "Graduation or passing calendar year (e.g., 2026).")
        ]
    },
    {
        "table_no": "4.2.4",
        "table_name": "scas_faculty_profiles",
        "description": "Stores faculty academic metadata, teaching departments, and institutional designations as a 1:1 extension of the user account.",
        "constraints": "id (PK), user_id (FK, UNIQUE, NOT NULL), department (NOT NULL), designation (NOT NULL)",
        "fields": [
            ("1", "id", "INT", "11", "PK, AUTO_INCREMENT, NOT NULL", "Unique faculty profile record identifier."),
            ("2", "user_id", "INT", "11", "FK, UNIQUE, NOT NULL", "Foreign key referencing scas_users(id) ON DELETE CASCADE (1:1 extension)."),
            ("3", "department", "VARCHAR", "100", "NOT NULL", "Academic teaching department (e.g., 'Department of Computer Science & Applications')."),
            ("4", "designation", "VARCHAR", "100", "NOT NULL", "Academic rank/title (e.g., 'Associate Professor', 'Assistant Professor', 'HOD').")
        ]
    },
    {
        "table_no": "4.2.5",
        "table_name": "scas_student_profiles",
        "description": "Stores student enrollment profiles, university hall ticket/matriculation numbers, cohort batch links, course allocations, and contact details.",
        "constraints": "id (PK), user_id (FK, UNIQUE, NOT NULL), roll_no (UNIQUE, NOT NULL), batch_id (FK, NOT NULL), course_id (FK, NOT NULL), phone (NULL)",
        "fields": [
            ("1", "id", "INT", "11", "PK, AUTO_INCREMENT, NOT NULL", "Unique student profile record identifier."),
            ("2", "user_id", "INT", "11", "FK, UNIQUE, NOT NULL", "Foreign key referencing scas_users(id) ON DELETE CASCADE (1:1 extension)."),
            ("3", "roll_no", "VARCHAR", "30", "UNIQUE, NOT NULL", "University matriculation / hall ticket roll number (e.g., 'MCA2401', '24MCA042')."),
            ("4", "batch_id", "INT", "11", "FK, NOT NULL", "Foreign key referencing scas_batches(id) ON DELETE CASCADE."),
            ("5", "course_id", "INT", "11", "FK, NOT NULL", "Foreign key referencing scas_courses(id) ON DELETE CASCADE."),
            ("6", "phone", "VARCHAR", "20", "NULL", "Student / emergency guardian contact phone number for SMS and notifications.")
        ]
    },
    {
        "table_no": "4.2.6",
        "table_name": "scas_subjects",
        "description": "Stores academic curriculum subjects, subject course codes, degree course associations, and assigned faculty educator references.",
        "constraints": "id (PK), code (UNIQUE, NOT NULL), name (NOT NULL), course_id (FK, NOT NULL), faculty_id (FK, NOT NULL)",
        "fields": [
            ("1", "id", "INT", "11", "PK, AUTO_INCREMENT, NOT NULL", "Unique curriculum course subject identifier."),
            ("2", "name", "VARCHAR", "100", "NOT NULL", "Full academic subject title (e.g., 'Advanced Database Systems', 'Cloud Computing')."),
            ("3", "code", "VARCHAR", "20", "UNIQUE, NOT NULL", "Official academic subject course code (e.g., 'MCA201', 'CS304')."),
            ("4", "course_id", "INT", "11", "FK, NOT NULL", "Foreign key referencing scas_courses(id) ON DELETE CASCADE."),
            ("5", "faculty_id", "INT", "11", "FK, NOT NULL", "Foreign key referencing scas_users(id) ON DELETE CASCADE (Assigned teacher).")
        ]
    },
    {
        "table_no": "4.2.7",
        "table_name": "scas_schedules",
        "description": "Stores weekly timetable lecture schedules, room allocations, days of the week, and commencement/termination time slots.",
        "constraints": "id (PK), subject_id (FK, NOT NULL), batch_id (FK, NOT NULL), day_of_week (NOT NULL), start_time (NOT NULL), end_time (NOT NULL), room (NOT NULL)",
        "fields": [
            ("1", "id", "INT", "11", "PK, AUTO_INCREMENT, NOT NULL", "Unique timetable slot identifier."),
            ("2", "subject_id", "INT", "11", "FK, NOT NULL", "Foreign key referencing scas_subjects(id) ON DELETE CASCADE."),
            ("3", "batch_id", "INT", "11", "FK, NOT NULL", "Foreign key referencing scas_batches(id) ON DELETE CASCADE."),
            ("4", "day_of_week", "VARCHAR", "20", "NOT NULL", "Scheduled lecture day: 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'."),
            ("5", "start_time", "VARCHAR", "10", "NOT NULL", "Lecture commencement time string (e.g., '09:00 AM', '11:30 AM')."),
            ("6", "end_time", "VARCHAR", "10", "NOT NULL", "Lecture termination time string (e.g., '10:00 AM', '12:30 PM')."),
            ("7", "room", "VARCHAR", "20", "NOT NULL", "Allocated classroom / computer laboratory identifier (e.g., 'Lab 3', 'Hall 201').")
        ]
    },
    {
        "table_no": "4.2.8",
        "table_name": "scas_attendance",
        "description": "Stores daily attendance event logs recording student presence or absence status per scheduled subject lecture.",
        "constraints": "id (PK), student_id (FK, NOT NULL), subject_id (FK, NOT NULL), date (NOT NULL), status (NOT NULL)",
        "fields": [
            ("1", "id", "INT", "11", "PK, AUTO_INCREMENT, NOT NULL", "Unique attendance log transaction identifier."),
            ("2", "student_id", "INT", "11", "FK, NOT NULL", "Foreign key referencing scas_student_profiles(id) ON DELETE CASCADE."),
            ("3", "subject_id", "INT", "11", "FK, NOT NULL", "Foreign key referencing scas_subjects(id) ON DELETE CASCADE."),
            ("4", "date", "DATE", "-", "NOT NULL", "Calendar date on which attendance was recorded (YYYY-MM-DD)."),
            ("5", "status", "VARCHAR", "10", "NOT NULL", "Daily attendance status value: 'Present' or 'Absent'.")
        ]
    },
    {
        "table_no": "4.2.9",
        "table_name": "scas_marks",
        "description": "Stores continuous internal evaluations (CIE), examination classifications, scores achieved, and maximum benchmark marks.",
        "constraints": "id (PK), student_id (FK, NOT NULL), subject_id (FK, NOT NULL), exam_type (NOT NULL), marks_obtained (NOT NULL), max_marks (NOT NULL)",
        "fields": [
            ("1", "id", "INT", "11", "PK, AUTO_INCREMENT, NOT NULL", "Unique internal evaluation score entry identifier."),
            ("2", "student_id", "INT", "11", "FK, NOT NULL", "Foreign key referencing scas_student_profiles(id) ON DELETE CASCADE."),
            ("3", "subject_id", "INT", "11", "FK, NOT NULL", "Foreign key referencing scas_subjects(id) ON DELETE CASCADE."),
            ("4", "exam_type", "VARCHAR", "30", "NOT NULL", "Examination classification: 'Midterm 1', 'Midterm 2', 'Assignment', 'Final Exam'."),
            ("5", "marks_obtained", "FLOAT", "-", "NOT NULL", "Numeric score achieved by student in the assessment (e.g., 42.5)."),
            ("6", "max_marks", "FLOAT", "-", "NOT NULL", "Maximum total marks possible for this examination type (e.g., 50.0 or 100.0).")
        ]
    },
    {
        "table_no": "4.2.10",
        "table_name": "scas_results",
        "description": "Stores semester grade sheets, final aggregated scores, benchmark marks, and academic credits earned by students.",
        "constraints": "id (PK), student_id (FK, NOT NULL), subject_id (FK, NOT NULL), semester (NOT NULL), marks_obtained (NOT NULL), max_marks (NOT NULL), credits (NOT NULL, DEFAULT 4)",
        "fields": [
            ("1", "id", "INT", "11", "PK, AUTO_INCREMENT, NOT NULL", "Unique semester result sheet entry identifier."),
            ("2", "student_id", "INT", "11", "FK, NOT NULL", "Foreign key referencing scas_student_profiles(id) ON DELETE CASCADE."),
            ("3", "subject_id", "INT", "11", "FK, NOT NULL", "Foreign key referencing scas_subjects(id) ON DELETE CASCADE."),
            ("4", "semester", "INT", "11", "NOT NULL", "Academic semester index (e.g., 1, 2, 3, 4 for MCA program)."),
            ("5", "marks_obtained", "FLOAT", "-", "NOT NULL", "Final aggregate score obtained out of 100 in the semester."),
            ("6", "max_marks", "FLOAT", "-", "NOT NULL", "Benchmark maximum aggregate marks (standard 100.0)."),
            ("7", "credits", "INT", "11", "NOT NULL, DEFAULT 4", "Academic credits assigned to this course subject (default = 4 credits).")
        ]
    },
    {
        "table_no": "4.2.11",
        "table_name": "scas_test_assessments",
        "description": "Stores continuous unit diagnostic evaluations, pre/post MCQ test transactions, raw scores, percentage metrics, and mastery taxonomy.",
        "constraints": "id (PK), student_id (FK, NOT NULL), subject_id (FK, NOT NULL), unit_number (NOT NULL), unit_title (NOT NULL), test_type (NOT NULL), score (NOT NULL), percentage (NOT NULL), total_questions (DEFAULT 25), mastery_level (DEFAULT 'Intermediate'), submitted_at (DEFAULT CURRENT_TIMESTAMP)",
        "fields": [
            ("1", "id", "INT", "11", "PK, AUTO_INCREMENT, NOT NULL", "Unique test assessment attempt transaction identifier."),
            ("2", "student_id", "INT", "11", "FK, NOT NULL", "Foreign key referencing scas_student_profiles(id) ON DELETE CASCADE."),
            ("3", "subject_id", "INT", "11", "FK, NOT NULL", "Foreign key referencing scas_subjects(id) ON DELETE CASCADE."),
            ("4", "unit_number", "INT", "11", "NOT NULL", "Curriculum unit sequence number (e.g., Unit 1 through Unit 5)."),
            ("5", "unit_title", "VARCHAR", "200", "NOT NULL", "Descriptive topic / chapter heading covered by this assessment."),
            ("6", "test_type", "VARCHAR", "20", "NOT NULL", "Diagnostic evaluation classification: 'pre-test' or 'post-test'."),
            ("7", "score", "FLOAT", "-", "NOT NULL", "Raw marks achieved in test (typically out of 25.0 points)."),
            ("8", "total_questions", "INT", "11", "NOT NULL, DEFAULT 25", "Total questions presented in the multiple-choice assessment."),
            ("9", "percentage", "FLOAT", "-", "NOT NULL", "Calculated performance percentage: (score / total_questions) * 100."),
            ("10", "mastery_level", "VARCHAR", "50", "DEFAULT 'Intermediate'", "Categorical taxonomy: 'Beginner', 'Intermediate', or 'Mastered'."),
            ("11", "submitted_at", "DATETIME", "-", "NOT NULL, DEFAULT CURRENT_TIMESTAMP", "Submission timestamp for speed, telemetry & placement leaderboard.")
        ]
    },
    {
        "table_no": "4.2.12",
        "table_name": "scas_fee_payments",
        "description": "Stores student financial fee ledgers, transaction records, clearance status, institutional receipts, and payment gateway references.",
        "constraints": "id (PK), student_id (FK, NOT NULL), amount (NOT NULL), status (NOT NULL), payment_date (NOT NULL, DEFAULT CURRENT_TIMESTAMP), receipt_no (UNIQUE, NULL), transaction_id (UNIQUE, NULL)",
        "fields": [
            ("1", "id", "INT", "11", "PK, AUTO_INCREMENT, NOT NULL", "Unique fee transaction ledger identifier."),
            ("2", "student_id", "INT", "11", "FK, NOT NULL", "Foreign key referencing scas_student_profiles(id) ON DELETE CASCADE."),
            ("3", "amount", "FLOAT", "-", "NOT NULL", "Transaction amount in institutional currency (e.g., 45000.00)."),
            ("4", "payment_date", "DATETIME", "-", "NOT NULL, DEFAULT CURRENT_TIMESTAMP", "Timestamp when payment was confirmed or recorded in ledger."),
            ("5", "status", "VARCHAR", "20", "NOT NULL", "Fee clearance state: 'Paid', 'Pending', or 'Overdue'."),
            ("6", "receipt_no", "VARCHAR", "50", "UNIQUE, NULL", "Unique institutional receipt sequence number (e.g., 'REC-2026-0814')."),
            ("7", "transaction_id", "VARCHAR", "50", "UNIQUE, NULL", "External banking / UPI reference transaction code (e.g., 'TXN938201948').")
        ]
    },
    {
        "table_no": "4.2.13",
        "table_name": "scas_leave_applications",
        "description": "Stores institutional leave applications, leave categories, absence date spans, applicant justifications, and administrative approval workflow states.",
        "constraints": "id (PK), user_id (FK, NOT NULL), leave_type (NOT NULL), start_date (NOT NULL), end_date (NOT NULL), reason (NOT NULL), status (NOT NULL, DEFAULT 'Pending'), applied_at (NOT NULL, DEFAULT CURRENT_TIMESTAMP)",
        "fields": [
            ("1", "id", "INT", "11", "PK, AUTO_INCREMENT, NOT NULL", "Unique leave application identifier."),
            ("2", "user_id", "INT", "11", "FK, NOT NULL", "Foreign key referencing scas_users(id) ON DELETE CASCADE (Applicant)."),
            ("3", "leave_type", "VARCHAR", "50", "NOT NULL", "Leave classification: 'Sick Leave', 'Casual Leave', 'Duty Leave', 'Maternity'."),
            ("4", "start_date", "DATE", "-", "NOT NULL", "Inclusive start date of proposed absence (YYYY-MM-DD)."),
            ("5", "end_date", "DATE", "-", "NOT NULL", "Inclusive completion date of proposed absence (YYYY-MM-DD)."),
            ("6", "reason", "TEXT", "-", "NOT NULL", "Applicant's textual justification, medical note details, or on-duty event brief."),
            ("7", "status", "VARCHAR", "20", "NOT NULL, DEFAULT 'Pending'", "Workflow lifecycle approval status: 'Pending', 'Approved', 'Rejected'."),
            ("8", "applied_at", "DATETIME", "-", "NOT NULL, DEFAULT CURRENT_TIMESTAMP", "Submission timestamp for review SLA tracking.")
        ]
    }
]

# Demo table from user's screenshot
DEMO_TABLE = {
    "table_no": "DEMO SPECIFICATION",
    "table_name": "companies",
    "description": "Stores company information such as company identity, login details, contact information, website, location, and company logo for managing placement-related organizations.",
    "constraints": "company_id (PK), email (UNIQUE), company_name (NOT NULL), email (NOT NULL), password (NOT NULL), created_at (NOT NULL, DEFAULT CURRENT_TIMESTAMP)",
    "fields": [
        ("1", "company_id", "INT", "11", "PK, AUTO_INCREMENT, NOT NULL", "Unique identifier for each company"),
        ("2", "company_name", "VARCHAR", "150", "NOT NULL", "Name of the company"),
        ("3", "email", "VARCHAR", "100", "UNIQUE, NOT NULL", "Unique email address used for company login/contact"),
        ("4", "password", "VARCHAR", "255", "NOT NULL", "Encrypted/hashed password for company account")
    ]
}


def build_data_dict_table(t_info, styles):
    """
    Constructs a ReportLab table matching the exact visual design of the demo image:
    Top Box: Table Name, Description, Constraints in a rectangular bordered container.
    Directly connected underneath: Grid table with Field No., Field Name, Type, Size, Constraints, Description.
    """
    meta_p_style = ParagraphStyle(
        'MetaPara',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.black
    )
    
    th_style = ParagraphStyle(
        'THCenter',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        alignment=1, # Center
        textColor=colors.black
    )
    th_left = ParagraphStyle(
        'THLeft',
        parent=th_style,
        alignment=0 # Left
    )
    
    td_style = ParagraphStyle(
        'TDLeft',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.black
    )
    td_center = ParagraphStyle(
        'TDCenter',
        parent=td_style,
        alignment=1 # Center
    )
    
    # Meta box text: 3 lines formatted like the demo image
    meta_html = (
        f"<b>Table Name:</b> {t_info['table_name']}<br/>"
        f"<b>Description:</b> {t_info['description']}<br/>"
        f"<b>Constraints:</b> {t_info['constraints']}"
    )
    
    # Construct rows:
    # Row 0: Meta box (spans all 6 columns)
    # Row 1: Table headers
    # Row 2+: Data rows
    table_rows = [
        [Paragraph(meta_html, meta_p_style), '', '', '', '', ''],
        [
            Paragraph('<b>Field No.</b>', th_center := th_style),
            Paragraph('<b>Field Name</b>', th_left),
            Paragraph('<b>Type</b>', th_center),
            Paragraph('<b>Size</b>', th_center),
            Paragraph('<b>Constraints</b>', th_left),
            Paragraph('<b>Description</b>', th_left)
        ]
    ]
    
    for f in t_info['fields']:
        f_no, f_name, f_type, f_size, f_const, f_desc = f
        table_rows.append([
            Paragraph(f_no, td_center),
            Paragraph(f"<b>{f_name}</b>" if 'id' in f_name and 'PK' in f_const else f_name, td_style),
            Paragraph(f_type, td_center),
            Paragraph(f_size, td_center),
            Paragraph(f_const, td_style),
            Paragraph(f_desc, td_style)
        ])
    
    # Styling to match the demo image perfectly
    # Total width = 525 pt (A4 width 595.27 - 70 margin = 525.27 pt)
    col_widths = [45, 105, 52, 38, 125, 160]
    
    style_commands = [
        # Span row 0 across all 6 columns
        ('SPAN', (0, 0), (5, 0)),
        
        # Border around the top meta box
        ('BOX', (0, 0), (5, 0), 1.0, colors.black),
        
        # Padding for meta box
        ('TOPPADDING', (0, 0), (5, 0), 6),
        ('BOTTOMPADDING', (0, 0), (5, 0), 6),
        ('LEFTPADDING', (0, 0), (5, 0), 8),
        ('RIGHTPADDING', (0, 0), (5, 0), 8),
        
        # Grid table borders: row 1 to bottom
        ('BOX', (0, 1), (5, -1), 1.0, colors.black),
        ('INNERGRID', (0, 1), (5, -1), 1.0, colors.black),
        
        # Vertical alignment
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        
        # Padding for grid cells
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
        ('LEFTPADDING', (0, 1), (-1, -1), 5),
        ('RIGHTPADDING', (0, 1), (-1, -1), 5),
        
        # Crisp white background (as in the demo image)
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
    ]
    
    return Table(table_rows, colWidths=col_widths, style=TableStyle(style_commands))


def generate_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=35,
        rightMargin=35,
        topMargin=46,
        bottomMargin=46
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=26,
        alignment=1,
        textColor=colors.HexColor('#0F172A')
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        alignment=1,
        textColor=colors.HexColor('#475569')
    )
    
    badge_style = ParagraphStyle(
        'BadgeStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=colors.HexColor('#B91C1C')
    )
    
    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=8
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#334155')
    )
    
    section_tag_style = ParagraphStyle(
        'SectionTag',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=6
    )

    story = []
    
    # ----------------------------------------------------
    # COVER / OVERVIEW PAGE
    # ----------------------------------------------------
    story.append(Spacer(1, 10))
    story.append(Paragraph("GANPAT UNIVERSITY", badge_style))
    story.append(Paragraph("ACHARYA MOTIBHAI PATEL INSTITUTE OF COMPUTER STUDIES (AMPICS)", ParagraphStyle('AMPICS', parent=badge_style, fontSize=9, textColor=colors.HexColor('#64748B'))))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Student Central Administrative System (SCAS)", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("System Database Architecture & Relational Schema Specification", subtitle_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Document Section: 4.2 Data Dictionary</b>", ParagraphStyle('SecH', parent=subtitle_style, fontName='Helvetica-Bold', textColor=colors.HexColor('#0F172A'))))
    story.append(Spacer(1, 15))
    
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E2E8F0'), spaceAfter=14))
    
    story.append(Paragraph("<b>1. Specification Overview & Standard Design</b>", h2_style))
    story.append(Paragraph(
        "This document details the comprehensive Data Dictionary for the <b>Student Central Administrative System (SCAS)</b>, "
        "designed in accordance with standard relational database documentation specifications. Every entity represents an active table "
        "in the MySQL database schema powering authentication, curriculum management, automated timetabling, CIE evaluations, "
        "diagnostic unit testing, and fee transaction accounting.",
        body_style
    ))
    story.append(Spacer(1, 10))
    
    # Demo reference table preview
    story.append(Paragraph("<b>Reference Design Standard (Demo Specification):</b>", ParagraphStyle('RefH', parent=body_style, fontName='Helvetica-Bold', textColor=colors.HexColor('#047857'))))
    story.append(Spacer(1, 6))
    demo_table_flowable = build_data_dict_table(DEMO_TABLE, styles)
    story.append(demo_table_flowable)
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "<i>Note: All 13 relational database tables below strictly adopt this validated structural schema format.</i>",
        ParagraphStyle('NoteSub', parent=body_style, fontName='Helvetica-Oblique', fontSize=8.5, textColor=colors.HexColor('#64748B'))
    ))
    
    # Clean page break before Master Index
    story.append(PageBreak())
    
    # Summary of 13 SCAS Tables
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>2. Master Index of SCAS System Tables (13 Entities)</b>", h2_style))
    story.append(Paragraph(
        "The following master index provides a consolidated register of all 13 core relational entities "
        "implemented within the SCAS database engine, indexed by section number, table identifier, primary key, and functional purpose:",
        body_style
    ))
    story.append(Spacer(1, 10))
    
    index_header = [
        Paragraph("<b>Table #</b>", ParagraphStyle('IdxH', parent=body_style, fontName='Helvetica-Bold', alignment=1)),
        Paragraph("<b>Physical Table Name</b>", ParagraphStyle('IdxH2', parent=body_style, fontName='Helvetica-Bold')),
        Paragraph("<b>Primary Key</b>", ParagraphStyle('IdxH3', parent=body_style, fontName='Helvetica-Bold')),
        Paragraph("<b>Functional Subsystem Role</b>", ParagraphStyle('IdxH4', parent=body_style, fontName='Helvetica-Bold'))
    ]
    index_data = [index_header]
    
    subsystems = [
        ("4.2.1", "scas_users", "id", "Security, RBAC & Synthetic User Credentials"),
        ("4.2.2", "scas_courses", "id", "Curricular Degrees (MCA, BCA, B.Tech)"),
        ("4.2.3", "scas_batches", "id", "Academic Cohorts & Graduation Batches"),
        ("4.2.4", "scas_faculty_profiles", "id", "Faculty Metadata & Department Assignments"),
        ("4.2.5", "scas_student_profiles", "id", "Student Roll Numbers & Demographics"),
        ("4.2.6", "scas_subjects", "id", "Academic Curriculum Subjects & Faculty Links"),
        ("4.2.7", "scas_schedules", "id", "Weekly Lecture Timetable & Room Allocations"),
        ("4.2.8", "scas_attendance", "id", "Daily Lecture Attendance Logs"),
        ("4.2.9", "scas_marks", "id", "Continuous Internal Evaluation (CIE) Marks"),
        ("4.2.10", "scas_results", "id", "Semester Official Grade Sheets & Credits"),
        ("4.2.11", "scas_test_assessments", "id", "Diagnostic MCQ Engine & Mastery Taxonomy"),
        ("4.2.12", "scas_fee_payments", "id", "Student Tuition Ledger & Transaction Receipts"),
        ("4.2.13", "scas_leave_applications", "id", "Digital Leave Workflow & Approval Auditing")
    ]
    
    for row in subsystems:
        index_data.append([
            Paragraph(row[0], ParagraphStyle('IdxCell', parent=body_style, alignment=1)),
            Paragraph(f"<code>{row[1]}</code>", body_style),
            Paragraph(f"<code>{row[2]}</code>", body_style),
            Paragraph(row[3], body_style)
        ])
    
    idx_table = Table(
        index_data,
        colWidths=[55, 135, 75, 260],
        style=TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#94A3B8')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F1F5F9')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ])
    )
    story.append(idx_table)
    
    # ----------------------------------------------------
    # DEDICATED PAGES FOR EACH OF THE 13 SCAS TABLES
    # ----------------------------------------------------
    for table_info in DATA_DICTIONARY_TABLES:
        story.append(PageBreak())
        
        # Header banner for each table
        story.append(Spacer(1, 5))
        story.append(Paragraph(f"<b>Table {table_info['table_no']}: {table_info['table_name']}</b>", section_tag_style))
        story.append(Spacer(1, 4))
        
        # Build Table element
        table_flowable = build_data_dict_table(table_info, styles)
        story.append(table_flowable)
        
        # Relational Context Card underneath the table
        story.append(Spacer(1, 14))
        rel_box = [
            [Paragraph(
                f"<b>Relational Integrity & Schema Notes for <code>{table_info['table_name']}</code>:</b><br/>"
                f"• <b>Primary Key:</b> <code>id</code> (Auto-incrementing integer identifier guaranteeing unique row resolution).<br/>"
                f"• <b>Referential Action:</b> Foreign key relationships utilize <code>ON DELETE CASCADE</code> to preserve referential consistency across parent entities.<br/>"
                f"• <b>Storage Engine:</b> InnoDB | <b>Character Set:</b> utf8mb4 | <b>Collation:</b> utf8mb4_unicode_ci.",
                ParagraphStyle('RelNote', parent=body_style, fontSize=8, leading=11.5, textColor=colors.HexColor('#475569'))
            )]
        ]
        rel_table = Table(rel_box, colWidths=[525], style=TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(rel_table)

    # Build PDF with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Data Dictionary PDF successfully generated at: {output_path}")

if __name__ == '__main__':
    target_path = os.path.join(r"d:\SCAS-HG-OR\scas-final", "SCAS_Data_Dictionary.pdf")
    generate_pdf(target_path)
    
    # Also copy to root workspace directory
    import shutil
    root_target = os.path.join(r"d:\SCAS-HG-OR", "SCAS_Data_Dictionary.pdf")
    shutil.copyfile(target_path, root_target)
    print(f"Copied to root directory: {root_target}")

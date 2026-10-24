import os
import sys
from PIL import Image, ImageDraw, ImageFont

def get_font(name="segoeui.ttf", size=20, bold=False):
    if bold:
        bold_paths = ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"]
        for bp in bold_paths:
            if os.path.exists(bp):
                try:
                    return ImageFont.truetype(bp, size)
                except:
                    pass
    font_path = f"C:/Windows/Fonts/{name}"
    if os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size)
        except:
            pass
    return ImageFont.load_default()

def draw_header(draw, W, title, category="SMART COLLEGE ANALYTICS SYSTEM (SCAS) - SYSTEM DESIGN & UML"):
    draw.rectangle([(0, 0), (W, 110)], fill=(26, 54, 93)) # Navy Primary
    draw.text((50, 15), category.upper(), font=get_font("segoeuib.ttf", 15, bold=True), fill=(56, 189, 248))
    draw.text((50, 42), title, font=get_font("segoeuib.ttf", 30, bold=True), fill=(255, 255, 255))
    draw.line([(0, 110), (W, 110)], fill=(56, 189, 248), width=3)

def draw_footer(draw, W, H, subtitle="MCA PS3 Project | Department of Computer Science & Applications"):
    draw.text((50, H - 35), subtitle, font=get_font("segoeui.ttf", 12), fill=(100, 116, 139))
    draw.text((W - 380, H - 35), "SCAS System Architecture & Design Model", font=get_font("segoeui.ttf", 12), fill=(100, 116, 139))

# =========================================================================
# 1. TIMELINE / GANTT CHART (4.1 Time Line Chart)
# =========================================================================
def generate_timeline_chart():
    W, H = 1920, 1080
    img = Image.new("RGB", (W, H), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)
    draw_header(draw, W, "4.1 PROJECT DEVELOPMENT TIMELINE (GANTT CHART)", "4. SYSTEM DESIGN AND DEVELOPMENT")

    # Legend / Info Card
    draw.rounded_rectangle([(50, 130), (W - 50, 200)], radius=10, fill=(30, 41, 59), outline=(56, 189, 248), width=1)
    draw.text((70, 142), "Project Duration: 18 Weeks (MCA Academic Semester)", font=get_font("segoeuib.ttf", 15, bold=True), fill=(255, 255, 255))
    draw.text((70, 168), "Methodology: Iterative Agile Development Model with Milestone Verifications", font=get_font("segoeui.ttf", 13), fill=(148, 163, 184))
    
    # Legend Pills
    draw.rounded_rectangle([(W - 480, 145), (W - 320, 185)], radius=6, fill=(34, 197, 94))
    draw.text((W - 460, 153), "100% Completed", font=get_font("segoeuib.ttf", 13, bold=True), fill=(15, 23, 42))
    draw.rounded_rectangle([(W - 300, 145), (W - 70, 185)], radius=6, fill=(56, 189, 248))
    draw.text((W - 280, 153), "Milestone Verified", font=get_font("segoeuib.ttf", 13, bold=True), fill=(15, 23, 42))

    grid_left = 520
    grid_right = W - 70
    grid_width = grid_right - grid_left
    total_weeks = 18
    week_w = grid_width / total_weeks
    grid_top = 220
    grid_bottom = 980

    # Draw Week Headers
    draw.rectangle([(50, grid_top), (grid_right, grid_top + 45)], fill=(26, 54, 93))
    draw.text((70, grid_top + 12), "Development Phases & Key Milestones", font=get_font("segoeuib.ttf", 15, bold=True), fill=(255, 255, 255))

    for w in range(1, total_weeks + 1):
        wx = grid_left + (w - 1) * week_w
        draw.line([(wx, grid_top), (wx, grid_bottom)], fill=(51, 65, 85), width=1)
        draw.text((wx + week_w/2 - 12, grid_top + 12), f"W{w}", font=get_font("segoeuib.ttf", 13, bold=True), fill=(56, 189, 248))

    tasks = [
        {"name": "1. Requirement Analysis & Feasibility Study", "start": 1, "end": 3, "color": (59, 130, 246), "deliverable": "SRS & System Scope Document"},
        {"name": "2. System Design, E-R & UML Modeling", "start": 3, "end": 5, "color": (16, 185, 129), "deliverable": "Use Case, Sequence & Class Models"},
        {"name": "3. Database Schema & Normalized Tables (MySQL)", "start": 5, "end": 7, "color": (245, 158, 11), "deliverable": "12 SQL Tables, Foreign Keys & Seed Data"},
        {"name": "4. Flask REST API & Backend Logic Development", "start": 6, "end": 10, "color": (139, 92, 246), "deliverable": "Auth, Attendance, Marks & Leave APIs"},
        {"name": "5. React 19 Single Page App & Tailwind UI", "start": 9, "end": 13, "color": (236, 72, 153), "deliverable": "Student, Faculty & Admin Portals"},
        {"name": "6. Academic Analytics Engine (Chart.js) & Aptitude", "start": 12, "end": 15, "color": (14, 165, 233), "deliverable": "SGPA/CGPA Graphs & Mock Test Module"},
        {"name": "7. Email Transport (SMTP) & System Verification", "start": 14, "end": 16, "color": (34, 197, 94), "deliverable": "verify_system.py automated diagnostics"},
        {"name": "8. Final Testing, Bug Fixes & Project Documentation", "start": 16, "end": 18, "color": (249, 115, 22), "deliverable": "Project Report & Final PPT Deck"}
    ]

    row_h = 85
    for idx, t in enumerate(tasks):
        ry = grid_top + 50 + idx * row_h
        if idx % 2 == 0:
            draw.rectangle([(50, ry), (grid_right, ry + row_h)], fill=(24, 34, 53))
        else:
            draw.rectangle([(50, ry), (grid_right, ry + row_h)], fill=(18, 26, 43))

        draw.text((70, ry + 18), t["name"], font=get_font("segoeuib.ttf", 14, bold=True), fill=(248, 250, 252))
        draw.text((70, ry + 46), f"Deliverable: {t['deliverable']}", font=get_font("segoeui.ttf", 12), fill=(148, 163, 184))

        bx1 = grid_left + (t["start"] - 1) * week_w + 6
        bx2 = grid_left + t["end"] * week_w - 6
        draw.rounded_rectangle([(bx1, ry + 20), (bx2, ry + 64)], radius=8, fill=t["color"])
        
        dur = t["end"] - t["start"] + 1
        draw.text((bx1 + 14, ry + 28), f"{dur} Weeks | 100% Done", font=get_font("segoeuib.ttf", 12, bold=True), fill=(15, 23, 42))

    draw_footer(draw, W, H)
    out_path = os.path.join(os.getcwd(), "scas_timeline_chart.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# =========================================================================
# 2. ENTITY-RELATIONSHIP (E-R) DIAGRAM (4.3 E-R Diagram)
# =========================================================================
def generate_er_diagram():
    W, H = 1920, 1080
    img = Image.new("RGB", (W, H), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)
    draw_header(draw, W, "4.3 ENTITY-RELATIONSHIP (E-R) DIAGRAM - SCAS DATABASE SCHEMA", "4. SYSTEM DESIGN AND DEVELOPMENT")

    # Grid 3 Rows x 4 Columns
    col_w = 320
    row_h = 240
    gap_x = 45
    gap_y = 35
    start_x = 60
    start_y = 140

    entities_grid = [
        # Row 1
        {"name": "SCAS_USERS", "r": 0, "c": 0, "pk": "id (PK)", "fields": ["username (UQ)", "password_hash", "email (UQ)", "role [Admin/Fac/Stud]", "name"], "color": (59, 130, 246)},
        {"name": "SCAS_FACULTY_PROFILES", "r": 0, "c": 1, "pk": "id (PK)", "fields": ["user_id (FK -> users.id)", "department", "designation"], "color": (139, 92, 246)},
        {"name": "SCAS_COURSES", "r": 0, "c": 2, "pk": "id (PK)", "fields": ["name", "code (UQ)", "description"], "color": (16, 185, 129)},
        {"name": "SCAS_BATCHES", "r": 0, "c": 3, "pk": "id (PK)", "fields": ["name", "course_id (FK -> courses.id)", "year"], "color": (245, 158, 11)},

        # Row 2
        {"name": "SCAS_STUDENT_PROFILES", "r": 1, "c": 0, "pk": "id (PK)", "fields": ["user_id (FK -> users.id)", "roll_no (UQ)", "batch_id (FK)", "course_id (FK)", "phone"], "color": (236, 72, 153)},
        {"name": "SCAS_SUBJECTS", "r": 1, "c": 1, "pk": "id (PK)", "fields": ["name", "code (UQ)", "course_id (FK)", "faculty_id (FK)"], "color": (14, 165, 233)},
        {"name": "SCAS_ATTENDANCE", "r": 1, "c": 2, "pk": "id (PK)", "fields": ["student_id (FK)", "subject_id (FK)", "date", "status [Present/Absent]"], "color": (34, 197, 94)},
        {"name": "SCAS_SCHEDULES", "r": 1, "c": 3, "pk": "id (PK)", "fields": ["subject_id (FK)", "batch_id (FK)", "day_of_week", "start_time, end_time, room"], "color": (20, 184, 166)},

        # Row 3
        {"name": "SCAS_MARKS", "r": 2, "c": 0, "pk": "id (PK)", "fields": ["student_id (FK)", "subject_id (FK)", "exam_type", "marks_obtained, max_marks"], "color": (249, 115, 22)},
        {"name": "SCAS_RESULTS", "r": 2, "c": 1, "pk": "id (PK)", "fields": ["student_id (FK)", "subject_id (FK)", "semester", "marks_obtained, credits"], "color": (168, 85, 247)},
        {"name": "SCAS_FEE_PAYMENTS", "r": 2, "c": 2, "pk": "id (PK)", "fields": ["student_id (FK)", "amount", "payment_date", "status [Paid/Pending]", "receipt_no (UQ)"], "color": (225, 29, 72)},
        {"name": "SCAS_LEAVE_APPLICATIONS", "r": 2, "c": 3, "pk": "id (PK)", "fields": ["user_id (FK)", "leave_type", "start_date, end_date", "status [Pending/Approved]"], "color": (99, 102, 241)}
    ]

    for e in entities_grid:
        x = start_x + e["c"] * (col_w + gap_x)
        y = start_y + e["r"] * (row_h + gap_y)

        # Entity Card
        draw.rounded_rectangle([(x, y), (x + col_w, y + row_h)], radius=10, fill=(30, 41, 59), outline=e["color"], width=2)
        # Header
        draw.rounded_rectangle([(x, y), (x + col_w, y + 36)], radius=10, fill=e["color"])
        draw.rectangle([(x, y + 18), (x + col_w, y + 36)], fill=e["color"])
        draw.text((x + 12, y + 8), e["name"], font=get_font("segoeuib.ttf", 13, bold=True), fill=(15, 23, 42))

        # Primary Key
        draw.text((x + 12, y + 44), f"[PK] {e['pk']}", font=get_font("segoeuib.ttf", 11.5, bold=True), fill=(251, 191, 36))

        # Field list
        fy = y + 70
        for fld in e["fields"]:
            draw.text((x + 12, fy), f"• {fld}", font=get_font("segoeui.ttf", 11), fill=(226, 232, 240))
            fy += 24

    # Bottom Legend Card
    draw.rounded_rectangle([(50, 970), (W - 50, 1030)], radius=8, fill=(24, 34, 53), outline=(56, 189, 248), width=1)
    draw.text((70, 985), "CARDINALITY & CONSTRAINTS:  Users (1:1) Profiles  |  Courses (1:N) Batches  |  Students (1:N) Attendance / Marks / Fees  |  Cascade Deletes Active", font=get_font("segoeuib.ttf", 12.5, bold=True), fill=(56, 189, 248))

    draw_footer(draw, W, H)
    out_path = os.path.join(os.getcwd(), "scas_er_diagram.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# =========================================================================
# 3. USE CASE DIAGRAM (4.4.1 Use Case Diagram)
# =========================================================================
def generate_usecase_diagram():
    W, H = 1920, 1080
    img = Image.new("RGB", (W, H), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)
    draw_header(draw, W, "4.4.1 UML USE CASE DIAGRAM - ROLE-BASED ACCESS MODEL", "4.4 USER MODELING LANGUAGE (UML) DIAGRAMS")

    # System Boundary Box
    draw.rounded_rectangle([(380, 140), (1540, 980)], radius=16, fill=(24, 34, 53), outline=(56, 189, 248), width=2)
    draw.text((410, 160), "SYSTEM BOUNDARY: SMART COLLEGE ANALYTICS SYSTEM (SCAS)", font=get_font("segoeuib.ttf", 15, bold=True), fill=(56, 189, 248))

    def draw_actor(x, y, name, color=(56, 189, 248)):
        draw.ellipse([(x - 20, y - 20), (x + 20, y + 20)], fill=(30, 41, 59), outline=color, width=3)
        draw.line([(x, y + 20), (x, y + 70)], fill=color, width=3)
        draw.line([(x - 30, y + 40), (x + 30, y + 40)], fill=color, width=3)
        draw.line([(x, y + 70), (x - 25, y + 115)], fill=color, width=3)
        draw.line([(x, y + 70), (x + 25, y + 115)], fill=color, width=3)
        draw.rounded_rectangle([(x - 75, y + 125), (x + 75, y + 155)], radius=6, fill=color)
        draw.text((x - 65, y + 132), name, font=get_font("segoeuib.ttf", 13, bold=True), fill=(15, 23, 42))

    draw_actor(180, 260, "ADMINISTRATOR", color=(239, 68, 68))
    draw_actor(180, 680, "FACULTY MEMBER", color=(59, 130, 246))
    draw_actor(1740, 460, "STUDENT", color=(34, 197, 94))

    # Ovals Grid inside Boundary (2 columns)
    left_cases = [
        {"text": "1. User Login & Password Hash Auth", "color": (59, 130, 246)},
        {"text": "2. Manage Student & Faculty Records", "color": (239, 68, 68)},
        {"text": "3. Fee Payment Status & Receipts", "color": (239, 68, 68)},
        {"text": "4. Publish Digital Notices & Alerts", "color": (239, 68, 68)},
        {"text": "5. Daily Attendance Marking (1-Click)", "color": (59, 130, 246)},
        {"text": "6. Upload Marks & Generate Result CSV", "color": (59, 130, 246)},
        {"text": "7. Approve / Reject Leave Slips", "color": (59, 130, 246)}
    ]

    right_cases = [
        {"text": "8. View Live Attendance % & Alerts", "color": (34, 197, 94)},
        {"text": "9. View SGPA/CGPA Analytics Charts", "color": (34, 197, 94)},
        {"text": "10. Submit Online Leave Application", "color": (34, 197, 94)},
        {"text": "11. Attempt Mock Placement Test", "color": (34, 197, 94)},
        {"text": "12. View Fee Dues & Download Receipt", "color": (34, 197, 94)},
        {"text": "<<extend>> Low Attendance Alert (<75%)", "color": (245, 158, 11)}
    ]

    # Draw left use cases
    uc_w = 420
    uc_h = 55
    y_start = 220
    y_gap = 100

    drawn_left = []
    for idx, uc in enumerate(left_cases):
        uy = y_start + idx * y_gap
        draw.ellipse([(430, uy), (430 + uc_w, uy + uc_h)], fill=(30, 41, 59), outline=uc["color"], width=2)
        draw.text((455, uy + 18), uc["text"], font=get_font("segoeuib.ttf", 12, bold=True), fill=(248, 250, 252))
        drawn_left.append((430, uy + uc_h//2, 430 + uc_w, uy + uc_h//2))

    drawn_right = []
    for idx, uc in enumerate(right_cases):
        uy = y_start + idx * y_gap + 40
        draw.ellipse([(1030, uy), (1030 + uc_w, uy + uc_h)], fill=(30, 41, 59), outline=uc["color"], width=2)
        draw.text((1055, uy + 18), uc["text"], font=get_font("segoeuib.ttf", 12, bold=True), fill=(248, 250, 252))
        drawn_right.append((1030, uy + uc_h//2, 1030 + uc_w, uy + uc_h//2))

    # Connect Admin (Actor 1 -> Cases 0,1,2,3)
    for i in [0, 1, 2, 3]:
        draw.line([(260, 310), (drawn_left[i][0], drawn_left[i][1])], fill=(239, 68, 68), width=2)

    # Connect Faculty (Actor 2 -> Cases 0,4,5,6)
    for i in [0, 4, 5, 6]:
        draw.line([(260, 720), (drawn_left[i][0], drawn_left[i][1])], fill=(59, 130, 246), width=2)

    # Connect Student (Actor 3 -> Left case 0 & Right cases 0,1,2,3,4)
    draw.line([(1660, 500), (drawn_left[0][2], drawn_left[0][3])], fill=(34, 197, 94), width=2)
    for i in range(5):
        draw.line([(1660, 500), (drawn_right[i][2], drawn_right[i][3])], fill=(34, 197, 94), width=2)

    # <<extend>> line from Attendance (Left 4) to Low Attendance Alert (Right 5)
    draw.line([(drawn_left[4][2], drawn_left[4][3]), (drawn_right[5][0], drawn_right[5][1])], fill=(245, 158, 11), width=2)

    draw_footer(draw, W, H)
    out_path = os.path.join(os.getcwd(), "scas_usecase_diagram.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# =========================================================================
# 4. ACTIVITY DIAGRAM (4.4.2 Activity Diagram)
# =========================================================================
def generate_activity_diagram():
    W, H = 1920, 1080
    img = Image.new("RGB", (W, H), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)
    draw_header(draw, W, "4.4.2 UML ACTIVITY DIAGRAM - CORE ACADEMIC PROCESS WORKFLOWS", "4.4 USER MODELING LANGUAGE (UML) DIAGRAMS")

    lane_w = (W - 100) // 3
    lanes = [
        {"title": "SWIMLANE 1: ADMINISTRATOR WORKFLOW", "x": 50, "color": (239, 68, 68)},
        {"title": "SWIMLANE 2: FACULTY WORKFLOW (ATTENDANCE & MARKS)", "x": 50 + lane_w, "color": (59, 130, 246)},
        {"title": "SWIMLANE 3: STUDENT WORKFLOW (ANALYTICS & LEAVE)", "x": 50 + 2 * lane_w, "color": (34, 197, 94)}
    ]

    for lane in lanes:
        lx = lane["x"]
        draw.rectangle([(lx, 140), (lx + lane_w, 980)], fill=(24, 34, 53), outline=(51, 65, 85), width=2)
        draw.rectangle([(lx, 140), (lx + lane_w, 185)], fill=lane["color"])
        draw.text((lx + 20, 152), lane["title"], font=get_font("segoeuib.ttf", 13, bold=True), fill=(15, 23, 42))

    def draw_activity(x, y, w, h, text, color=(56, 189, 248)):
        draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=10, fill=(30, 41, 59), outline=color, width=2)
        draw.text((x + 15, y + (h//2) - 8), text, font=get_font("segoeuib.ttf", 11.5, bold=True), fill=(248, 250, 252))

    def draw_decision(x, y, size, text):
        draw.polygon([(x, y - size), (x + size*1.5, y), (x, y + size), (x - size*1.5, y)], fill=(45, 55, 72), outline=(245, 158, 11), width=2)
        draw.text((x - 45, y - 8), text, font=get_font("segoeuib.ttf", 10.5, bold=True), fill=(251, 191, 36))

    # 1. Admin Lane Activities
    draw.ellipse([(200, 210), (230, 240)], fill=(34, 197, 94))
    draw_activity(100, 270, 400, 45, "1. Admin Logs into Portal", (239, 68, 68))
    draw_activity(100, 360, 400, 45, "2. Add/Import Student & Faculty CSV", (239, 68, 68))
    draw_activity(100, 450, 400, 45, "3. Auto-Dispatch Credentials via SMTP", (239, 68, 68))
    draw_activity(100, 540, 400, 45, "4. Update Student Fee Status (Paid/Pending)", (239, 68, 68))
    draw_activity(100, 630, 400, 45, "5. Auto-Generate Unique Receipt Number", (239, 68, 68))
    draw_activity(100, 720, 400, 45, "6. Post Urgent Notice to Notice Board", (239, 68, 68))

    draw.line([(215, 240), (215, 270)], fill=(239, 68, 68), width=2)
    draw.line([(215, 315), (215, 360)], fill=(239, 68, 68), width=2)
    draw.line([(215, 405), (215, 450)], fill=(239, 68, 68), width=2)
    draw.line([(215, 495), (215, 540)], fill=(239, 68, 68), width=2)
    draw.line([(215, 585), (215, 630)], fill=(239, 68, 68), width=2)
    draw.line([(215, 675), (215, 720)], fill=(239, 68, 68), width=2)

    # 2. Faculty Lane Activities
    fx = 50 + lane_w + 50
    draw.ellipse([(fx + 180, 210), (fx + 210, 240)], fill=(34, 197, 94))
    draw_activity(fx, 270, 400, 45, "1. Faculty Selects Subject & Date", (59, 130, 246))
    draw_activity(fx, 360, 400, 45, "2. 1-Click Roll Call Marking (Present/Absent)", (59, 130, 246))
    draw_activity(fx, 450, 400, 45, "3. Submit & Commit to MySQL Database", (59, 130, 246))
    draw_decision(fx + 200, 540, 25, "Attendance < 75% ?")
    draw_activity(fx, 620, 400, 45, "4. Trigger Real-Time Low Attendance Alert", (245, 158, 11))
    draw_activity(fx, 710, 400, 45, "5. Upload Internal Marks CSV & Compute GPA", (59, 130, 246))
    draw_activity(fx, 800, 400, 45, "6. Review Student Leave Applications (Approve)", (59, 130, 246))

    draw.line([(fx + 195, 240), (fx + 195, 270)], fill=(59, 130, 246), width=2)
    draw.line([(fx + 195, 315), (fx + 195, 360)], fill=(59, 130, 246), width=2)
    draw.line([(fx + 195, 405), (fx + 195, 450)], fill=(59, 130, 246), width=2)
    draw.line([(fx + 195, 495), (fx + 195, 515)], fill=(59, 130, 246), width=2)
    draw.line([(fx + 195, 565), (fx + 195, 620)], fill=(245, 158, 11), width=2)
    draw.text((fx + 205, 580), "[YES]", font=get_font("segoeuib.ttf", 10, bold=True), fill=(245, 158, 11))
    draw.line([(fx + 195, 665), (fx + 195, 710)], fill=(59, 130, 246), width=2)
    draw.line([(fx + 195, 755), (fx + 195, 800)], fill=(59, 130, 246), width=2)

    # 3. Student Lane Activities
    sx = 50 + 2 * lane_w + 50
    draw.ellipse([(sx + 180, 210), (sx + 210, 240)], fill=(34, 197, 94))
    draw_activity(sx, 270, 400, 45, "1. Student Opens Real-Time Dashboard", (34, 197, 94))
    draw_activity(sx, 360, 400, 45, "2. View Subject Attendance % & Warning Badge", (34, 197, 94))
    draw_activity(sx, 450, 400, 45, "3. Analyze Interactive SGPA/CGPA Progression", (34, 197, 94))
    draw_activity(sx, 540, 400, 45, "4. Apply for Leave / Duty Slip Online", (34, 197, 94))
    draw_activity(sx, 630, 400, 45, "5. Attempt Mock Placement Aptitude Test", (34, 197, 94))
    draw_activity(sx, 720, 400, 45, "6. View Instant Scorecard & Mastery Level", (34, 197, 94))

    draw.ellipse([(sx + 185, 810), (sx + 215, 840)], fill=(30, 41, 59), outline=(34, 197, 94), width=3)
    draw.ellipse([(sx + 190, 815), (sx + 210, 835)], fill=(34, 197, 94))

    draw.line([(sx + 195, 240), (sx + 195, 270)], fill=(34, 197, 94), width=2)
    draw.line([(sx + 195, 315), (sx + 195, 360)], fill=(34, 197, 94), width=2)
    draw.line([(sx + 195, 405), (sx + 195, 450)], fill=(34, 197, 94), width=2)
    draw.line([(sx + 195, 495), (sx + 195, 540)], fill=(34, 197, 94), width=2)
    draw.line([(sx + 195, 585), (sx + 195, 630)], fill=(34, 197, 94), width=2)
    draw.line([(sx + 195, 675), (sx + 195, 720)], fill=(34, 197, 94), width=2)
    draw.line([(sx + 195, 765), (sx + 195, 810)], fill=(34, 197, 94), width=2)

    draw_footer(draw, W, H)
    out_path = os.path.join(os.getcwd(), "scas_activity_diagram.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# =========================================================================
# 5. SEQUENCE DIAGRAM (4.4.3 Sequence Diagram)
# =========================================================================
def generate_sequence_diagram():
    W, H = 1920, 1080
    img = Image.new("RGB", (W, H), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)
    draw_header(draw, W, "4.4.3 UML SEQUENCE DIAGRAM - ATTENDANCE MARKING & REAL-TIME ANALYTICS", "4.4 USER MODELING LANGUAGE (UML) DIAGRAMS")

    lifelines = [
        {"name": "Faculty / User\n(Actor)", "x": 180, "color": (56, 189, 248)},
        {"name": ":React19 UI\n(Client View)", "x": 460, "color": (59, 130, 246)},
        {"name": ":AuthGuard\n(Session Handler)", "x": 750, "color": (168, 85, 247)},
        {"name": ":FlaskAPI Controller\n(REST WSGI Server)", "x": 1050, "color": (245, 158, 11)},
        {"name": ":SQLAlchemy ORM\n(Database Engine)", "x": 1350, "color": (34, 197, 94)},
        {"name": ":SMTP Mailer\n(Notification Service)", "x": 1650, "color": (239, 68, 68)}
    ]

    top_y = 150
    bottom_y = 960

    for ll in lifelines:
        x = ll["x"]
        draw.rounded_rectangle([(x - 90, top_y), (x + 90, top_y + 55)], radius=8, fill=(30, 41, 59), outline=ll["color"], width=2)
        draw.text((x - 70, top_y + 10), ll["name"], font=get_font("segoeuib.ttf", 11.5, bold=True), fill=(248, 250, 252))

        for dy in range(top_y + 60, bottom_y, 14):
            draw.line([(x, dy), (x, dy + 8)], fill=(71, 85, 105), width=2)

    messages = [
        {"from": 0, "to": 1, "text": "1: Select Subject & Mark Attendance(date, status_list)", "y": 250, "is_return": False},
        {"from": 1, "to": 2, "text": "2: POST /api/attendance/mark with Session Cookie", "y": 310, "is_return": False},
        {"from": 2, "to": 3, "text": "3: Validate Faculty Role & Route Request", "y": 370, "is_return": False},
        {"from": 3, "to": 4, "text": "4: db.session.bulk_save_objects(AttendanceList)", "y": 430, "is_return": False},
        {"from": 4, "to": 4, "text": "5: Execute INSERT into scas_attendance & COMMIT", "y": 490, "is_return": False, "self": True},
        {"from": 4, "to": 3, "text": "6: Return Commit Success & Updated Aggregate %", "y": 550, "is_return": True},
        {"from": 3, "to": 3, "text": "7: Evaluate if Student Attendance < 75%", "y": 610, "is_return": False, "self": True},
        {"from": 3, "to": 5, "text": "8: Dispatch Warning Email via SMTP (low_attendance_alert)", "y": 670, "is_return": False},
        {"from": 3, "to": 1, "text": "9: HTTP 200 OK {success: true, flagged_students: count}", "y": 740, "is_return": True},
        {"from": 1, "to": 0, "text": "10: Render Success Toast & Re-render Chart.js Analytics", "y": 810, "is_return": True}
    ]

    for msg in messages:
        y = msg["y"]
        if msg.get("self"):
            x = lifelines[msg["from"]]["x"]
            draw.line([(x, y), (x + 60, y)], fill=(245, 158, 11), width=2)
            draw.line([(x + 60, y), (x + 60, y + 25)], fill=(245, 158, 11), width=2)
            draw.line([(x + 60, y + 25), (x, y + 25)], fill=(245, 158, 11), width=2)
            draw.polygon([(x, y + 25), (x + 10, y + 20), (x + 10, y + 30)], fill=(245, 158, 11))
            draw.text((x + 70, y + 6), msg["text"], font=get_font("segoeuib.ttf", 11, bold=True), fill=(251, 191, 36))
        else:
            x1 = lifelines[msg["from"]]["x"]
            x2 = lifelines[msg["to"]]["x"]
            color = (56, 189, 248) if not msg["is_return"] else (74, 222, 128)
            
            if msg["is_return"]:
                step = 10 if x1 < x2 else -10
                for dx in range(x1, x2, step * 2):
                    draw.line([(dx, y), (dx + step, y)], fill=color, width=2)
            else:
                draw.line([(x1, y), (x2, y)], fill=color, width=2)

            if x2 > x1:
                draw.polygon([(x2, y), (x2 - 10, y - 5), (x2 - 10, y + 5)], fill=color)
            else:
                draw.polygon([(x2, y), (x2 + 10, y - 5), (x2 + 10, y + 5)], fill=color)

            mid_x = min(x1, x2) + 20
            draw.text((mid_x, y - 18), msg["text"], font=get_font("segoeuib.ttf", 11, bold=True), fill=(248, 250, 252))

    draw_footer(draw, W, H)
    out_path = os.path.join(os.getcwd(), "scas_sequence_diagram.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# =========================================================================
# 6. COLLABORATION / COMMUNICATION DIAGRAM (4.4.4 Collaboration Diagram)
# =========================================================================
def generate_collaboration_diagram():
    W, H = 1920, 1080
    img = Image.new("RGB", (W, H), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)
    draw_header(draw, W, "4.4.4 UML COLLABORATION / COMMUNICATION DIAGRAM - OBJECT INTERACTION", "4.4 USER MODELING LANGUAGE (UML) DIAGRAMS")

    # Clean 4-Column x 2-Row Layout
    nodes = [
        {"id": "1", "name": "1: User Client\n(Browser)", "x": 100, "y": 240, "color": (56, 189, 248)},
        {"id": "2", "name": "2: React SPA Engine\n(Vite + Tailwind)", "x": 560, "y": 240, "color": (59, 130, 246)},
        {"id": "3", "name": "3: Flask WSGI Server\n(App Router)", "x": 1020, "y": 240, "color": (245, 158, 11)},
        {"id": "4", "name": "4: SQLAlchemy ORM\n(Data Mapper)", "x": 1480, "y": 240, "color": (34, 197, 94)},
        {"id": "5", "name": "5: SMTP Mail Service\n(Email Dispatcher)", "x": 100, "y": 660, "color": (236, 72, 153)},
        {"id": "6", "name": "6: Analytics Engine\n(Chart.js Processor)", "x": 560, "y": 660, "color": (168, 85, 247)},
        {"id": "7", "name": "7: Auth Security\n(Werkzeug Hashing)", "x": 1020, "y": 660, "color": (239, 68, 68)},
        {"id": "8", "name": "8: MySQL Relational DB\n(12 Normalized Tables)", "x": 1480, "y": 660, "color": (20, 184, 166)}
    ]

    for n in nodes:
        x, y = n["x"], n["y"]
        draw.rounded_rectangle([(x, y), (x + 340, y + 120)], radius=12, fill=(30, 41, 59), outline=n["color"], width=2)
        draw.text((x + 20, y + 32), n["name"], font=get_font("segoeuib.ttf", 14, bold=True), fill=(248, 250, 252))

    # Clean Orthogonal Connector Lines and Cards
    def draw_link_with_badge(x1, y1, x2, y2, msgs):
        draw.line([(x1, y1), (x2, y2)], fill=(100, 116, 139), width=2)
        mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
        
        # Text Callout Card
        card_h = len(msgs) * 20 + 16
        draw.rounded_rectangle([(mid_x - 130, mid_y - card_h//2), (mid_x + 130, mid_y + card_h//2)], radius=6, fill=(24, 34, 53), outline=(56, 189, 248), width=1)
        for idx, m in enumerate(msgs):
            draw.text((mid_x - 120, mid_y - card_h//2 + 8 + idx * 20), m, font=get_font("segoeuib.ttf", 10.5, bold=True), fill=(251, 191, 36))

    # Top Row Horizontal Links
    draw_link_with_badge(440, 300, 560, 300, ["1.1: Submit Action()", "1.8: Render UI Response()"])
    draw_link_with_badge(900, 300, 1020, 300, ["1.2: POST /api/route", "1.7: HTTP 200 JSON"])
    draw_link_with_badge(1360, 300, 1480, 300, ["1.5: db.session.add()", "1.6: db.session.commit()"])

    # Vertical Links
    draw_link_with_badge(270, 360, 270, 660, ["1.9: Dispatch Alert Mail()", "1.10: Log sent_emails.log"])
    draw_link_with_badge(730, 360, 730, 660, ["1.2a: Compute SGPA/CGPA", "1.2b: Format Chart Data"])
    draw_link_with_badge(1190, 360, 1190, 660, ["1.3: check_password_hash()", "1.4: Verify RBAC Session"])
    draw_link_with_badge(1650, 360, 1650, 660, ["SQL INSERT / SELECT", "Return Record Tuples"])

    # Info card on top
    draw.rounded_rectangle([(450, 135), (1450, 205)], radius=10, fill=(24, 34, 53), outline=(56, 189, 248), width=1)
    draw.text((470, 148), "COLLABORATION ARCHITECTURE HIGHLIGHTS:", font=get_font("segoeuib.ttf", 14, bold=True), fill=(56, 189, 248))
    draw.text((470, 172), "• Highlights structural organization of objects & numbered synchronous message sequences.", font=get_font("segoeui.ttf", 12), fill=(226, 232, 240))

    draw_footer(draw, W, H)
    out_path = os.path.join(os.getcwd(), "scas_collaboration_diagram.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# =========================================================================
# 7. CLASS DIAGRAM (4.4.5 Class Diagram)
# =========================================================================
def generate_class_diagram():
    W, H = 1920, 1080
    img = Image.new("RGB", (W, H), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)
    draw_header(draw, W, "4.4.5 UML CLASS DIAGRAM - OBJECT-ORIENTED DOMAIN MODEL", "4.4 USER MODELING LANGUAGE (UML) DIAGRAMS")

    classes = [
        {
            "name": "User", "x": 60, "y": 140, "w": 280, "h": 220,
            "attrs": ["- id: Integer", "- username: String", "- password_hash: String", "- email: String", "- role: String"],
            "methods": ["+ set_password(pwd)", "+ check_password(pwd): bool", "+ get_profile(): Profile"],
            "color": (59, 130, 246)
        },
        {
            "name": "StudentProfile", "x": 420, "y": 140, "w": 290, "h": 220,
            "attrs": ["- id: Integer", "- user_id: Integer", "- roll_no: String", "- batch_id: Integer", "- phone: String"],
            "methods": ["+ calculate_attendance_pct(): float", "+ compute_sgpa(): float", "+ compute_cgpa(): float"],
            "color": (34, 197, 94)
        },
        {
            "name": "FacultyProfile", "x": 790, "y": 140, "w": 280, "h": 220,
            "attrs": ["- id: Integer", "- user_id: Integer", "- department: String", "- designation: String"],
            "methods": ["+ get_assigned_subjects(): List", "+ mark_attendance(batch, sub)", "+ approve_leave(app_id)"],
            "color": (168, 85, 247)
        },
        {
            "name": "Subject", "x": 1150, "y": 140, "w": 280, "h": 220,
            "attrs": ["- id: Integer", "- name: String", "- code: String", "- course_id: Integer", "- faculty_id: Integer"],
            "methods": ["+ get_enrolled_students()", "+ get_attendance_log()", "+ get_marks_distribution()"],
            "color": (245, 158, 11)
        },
        {
            "name": "Attendance", "x": 60, "y": 420, "w": 280, "h": 200,
            "attrs": ["- id: Integer", "- student_id: Integer", "- subject_id: Integer", "- date: Date", "- status: String"],
            "methods": ["+ log_attendance()", "+ check_threshold(): bool", "+ get_shortage_report()"],
            "color": (14, 165, 233)
        },
        {
            "name": "Mark", "x": 420, "y": 420, "w": 290, "h": 200,
            "attrs": ["- id: Integer", "- student_id: Integer", "- subject_id: Integer", "- exam_type: String", "- marks_obtained: Float"],
            "methods": ["+ upload_csv()", "+ validate_score_bounds()", "+ calculate_percentage()"],
            "color": (249, 115, 22)
        },
        {
            "name": "Result", "x": 790, "y": 420, "w": 280, "h": 200,
            "attrs": ["- id: Integer", "- student_id: Integer", "- subject_id: Integer", "- semester: Integer", "- credits: Integer"],
            "methods": ["+ compute_grade_point()", "+ get_semester_transcript()", "+ export_grade_card()"],
            "color": (20, 184, 166)
        },
        {
            "name": "FeePayment", "x": 1150, "y": 420, "w": 280, "h": 200,
            "attrs": ["- id: Integer", "- student_id: Integer", "- amount: Float", "- status: String", "- receipt_no: String"],
            "methods": ["+ process_payment()", "+ generate_receipt()", "+ get_pending_dues()"],
            "color": (239, 68, 68)
        },
        {
            "name": "LeaveApplication", "x": 240, "y": 680, "w": 320, "h": 220,
            "attrs": ["- id: Integer", "- user_id: Integer", "- leave_type: String", "- start_date, end_date: Date", "- status: String"],
            "methods": ["+ submit_application()", "+ approve_request()", "+ reject_request()"],
            "color": (236, 72, 153)
        },
        {
            "name": "TestAssessment", "x": 640, "y": 680, "w": 330, "h": 220,
            "attrs": ["- id: Integer", "- student_id: Integer", "- subject_id: Integer", "- unit_number: Integer", "- score, pct: Float"],
            "methods": ["+ submit_exam()", "+ calculate_mastery_level()", "+ get_unit_leaderboard()"],
            "color": (99, 102, 241)
        }
    ]

    for c in classes:
        x, y, w, h = c["x"], c["y"], c["w"], c["h"]
        draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=8, fill=(30, 41, 59), outline=c["color"], width=2)
        draw.rectangle([(x, y), (x + w, y + 32)], fill=c["color"])
        draw.text((x + 15, y + 6), c["name"], font=get_font("segoeuib.ttf", 13, bold=True), fill=(15, 23, 42))

        ay = y + 38
        for attr in c["attrs"]:
            draw.text((x + 10, ay), attr, font=get_font("segoeui.ttf", 11), fill=(226, 232, 240))
            ay += 18
        draw.line([(x, ay + 4), (x + w, ay + 4)], fill=c["color"], width=1)

        my = ay + 8
        for meth in c["methods"]:
            draw.text((x + 10, my), meth, font=get_font("segoeuib.ttf", 11), fill=(251, 191, 36))
            my += 18

    # UML Legend Box on Right
    draw.rounded_rectangle([(1520, 140), (W - 50, 900)], radius=12, fill=(24, 34, 53), outline=(56, 189, 248), width=1)
    draw.text((1540, 160), "UML CLASS RELATIONSHIPS", font=get_font("segoeuib.ttf", 14, bold=True), fill=(56, 189, 248))
    notes = [
        "• Inheritance & Composition:",
        "  User 1 <--> 1 StudentProfile",
        "  User 1 <--> 1 FacultyProfile",
        "",
        "• 1-to-Many Associations:",
        "  Student 1 <--> * Attendance",
        "  Student 1 <--> * Marks",
        "  Student 1 <--> * Results",
        "  Student 1 <--> * FeePayment",
        "  Student 1 <--> * TestAssessment",
        "  Faculty 1 <--> * Subject",
        "  User 1 <--> * LeaveApplication",
        "",
        "• Notation Standard:",
        "  - Private field",
        "  + Public method",
        "  Strict Python type hints",
        "  SQLAlchemy ORM models"
    ]
    ny = 200
    for note in notes:
        draw.text((1540, ny), note, font=get_font("segoeui.ttf", 12), fill=(226, 232, 240))
        ny += 22

    draw_footer(draw, W, H)
    out_path = os.path.join(os.getcwd(), "scas_class_diagram.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# =========================================================================
# 8. 3-TIER SYSTEM ARCHITECTURE & DATA FLOW DIAGRAM (DFD)
# =========================================================================
def generate_system_architecture():
    W, H = 1920, 1080
    img = Image.new("RGB", (W, H), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)
    draw_header(draw, W, "3-TIER SYSTEM ARCHITECTURE & DATA FLOW DIAGRAM (DFD)", "SYSTEM ARCHITECTURE")

    tiers = [
        {
            "title": "TIER 1: PRESENTATION TIER (CLIENT SPA)",
            "sub": "React 19 • TypeScript • Vite • Tailwind CSS • Chart.js • Lucide Icons",
            "x": 60, "w": 560, "color": (59, 130, 246),
            "modules": [
                "• Student Academic Portal (GPA & Attendance Views)",
                "• Faculty Portal (1-Click Roll Call & CSV Upload)",
                "• Administrator Central Governance Dashboard",
                "• Interactive Chart.js Progression Graphs",
                "• Timed Mock Placement Aptitude Exam Engine",
                "• Real-Time Notification & Leave Application UI"
            ]
        },
        {
            "title": "TIER 2: APPLICATION & LOGIC TIER (API WSGI)",
            "sub": "Python 3.x • Flask WSGI • Werkzeug Security • REST Blueprint Controllers",
            "x": 680, "w": 560, "color": (245, 158, 11),
            "modules": [
                "• REST API Routing & JSON Serializers",
                "• Werkzeug SHA-256 Authentication & RBAC Guard",
                "• GPA & CGPA Calculation Engine (100% Accuracy)",
                "• Attendance Risk Evaluator (<75% Threshold Alert)",
                "• Automated SMTP Email Dispatcher (smtplib)",
                "• System Diagnostic & Health Verifier (verify_system.py)"
            ]
        },
        {
            "title": "TIER 3: DATA STORAGE TIER (RELATIONAL DB)",
            "sub": "MySQL 8.0 / SQLite3 • Flask-SQLAlchemy ORM • 12 Normalized Tables",
            "x": 1300, "w": 560, "color": (34, 197, 94),
            "modules": [
                "• scas_users & scas_student_profiles",
                "• scas_faculty_profiles & scas_courses",
                "• scas_subjects & scas_batches",
                "• scas_attendance & scas_marks",
                "• scas_results & scas_fee_payments",
                "• scas_leave_applications & scas_test_assessments"
            ]
        }
    ]

    for t in tiers:
        x, w = t["x"], t["w"]
        draw.rounded_rectangle([(x, 150), (x + w, 780)], radius=14, fill=(24, 34, 53), outline=t["color"], width=2)
        draw.rounded_rectangle([(x, 150), (x + w, 220)], radius=14, fill=t["color"])
        draw.rectangle([(x, 190), (x + w, 220)], fill=t["color"])
        draw.text((x + 18, 162), t["title"], font=get_font("segoeuib.ttf", 13.5, bold=True), fill=(15, 23, 42))
        draw.text((x + 18, 190), t["sub"], font=get_font("segoeui.ttf", 10.5, bold=True), fill=(15, 23, 42))

        my = 250
        for m in t["modules"]:
            draw.text((x + 25, my), m, font=get_font("segoeui.ttf", 13), fill=(226, 232, 240))
            my += 36

    draw.line([(620, 460), (680, 460)], fill=(56, 189, 248), width=4)
    draw.polygon([(680, 460), (668, 452), (668, 468)], fill=(56, 189, 248))
    draw.text((630, 430), "HTTP/REST", font=get_font("segoeuib.ttf", 10, bold=True), fill=(56, 189, 248))

    draw.line([(1240, 460), (1300, 460)], fill=(34, 197, 94), width=4)
    draw.polygon([(1300, 460), (1288, 452), (1288, 468)], fill=(34, 197, 94))
    draw.text((1250, 430), "SQLAlchemy", font=get_font("segoeuib.ttf", 10, bold=True), fill=(34, 197, 94))

    draw.rounded_rectangle([(60, 815), (W - 60, 980)], radius=12, fill=(30, 41, 59), outline=(56, 189, 248), width=1)
    draw.text((85, 830), "LEVEL 0 DFD CONTEXT SUMMARY:", font=get_font("segoeuib.ttf", 14, bold=True), fill=(56, 189, 248))
    dfd_points = [
        "1. External Entities: Administrator, Faculty Member, and Enrolled Student interact securely through SSL-encrypted HTTPS sessions.",
        "2. Core Central Process (0.0): SCAS Engine orchestrates User Authentication, Attendance Logging, Internal Marks Evaluation, and Notifications.",
        "3. Data Stores: Normalized Relational Database (D1) persists student records, exam scores, attendance sessions, and transaction audit trails."
    ]
    dy = 865
    for p in dfd_points:
        draw.text((85, dy), p, font=get_font("segoeui.ttf", 12.5), fill=(226, 232, 240))
        dy += 30

    draw_footer(draw, W, H)
    out_path = os.path.join(os.getcwd(), "scas_system_architecture_dfd.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

if __name__ == "__main__":
    generate_timeline_chart()
    generate_er_diagram()
    generate_usecase_diagram()
    generate_activity_diagram()
    generate_sequence_diagram()
    generate_collaboration_diagram()
    generate_class_diagram()
    generate_system_architecture()
    print("Refined diagrams generated successfully!")

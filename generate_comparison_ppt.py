import os
import sys
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_comparison_presentation():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Cohesive Color Palette
    BG_DARK = RGBColor(15, 23, 42)          # Slate 900
    CARD_BG = RGBColor(255, 255, 255)       # Pure White
    NAVY_PRIMARY = RGBColor(26, 54, 93)     # #1A365D - Deep Navy
    BLUE_ACCENT = RGBColor(49, 130, 206)    # #3182CE - Vibrant Blue
    BLUE_LIGHT = RGBColor(235, 248, 255)    # Light Blue Tint
    RED_ACCENT = RGBColor(220, 38, 38)      # #DC2626 - Crimson Red
    RED_LIGHT = RGBColor(254, 242, 242)     # Light Red Tint
    GREEN_ACCENT = RGBColor(22, 163, 74)    # #16A34A - Forest Green
    GREEN_LIGHT = RGBColor(240, 253, 244)   # Light Green Tint
    TEXT_LIGHT = RGBColor(248, 250, 252)     # White Text
    TEXT_MUTED = RGBColor(100, 116, 139)    # Slate 500
    TEXT_DARK = RGBColor(30, 41, 59)        # Slate 800

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="SCAS COMPARATIVE STUDY & EVALUATION"):
        # Header banner
        banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
        banner.fill.solid()
        banner.fill.fore_color.rgb = NAVY_PRIMARY
        banner.line.fill.background()

        # Category / Subtitle
        tx_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.7), Inches(0.28))
        tf_c = tx_cat.text_frame
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
        p_c = tf_c.paragraphs[0]
        p_c.text = category_text.upper()
        p_c.font.size = Pt(10)
        p_c.font.bold = True
        p_c.font.color.rgb = BLUE_ACCENT
        p_c.font.name = 'Segoe UI'

        # Main Title
        tx_t = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(11.7), Inches(0.55))
        tf_t = tx_t.text_frame
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_LIGHT
        p_t.font.name = 'Segoe UI'

        # Footer
        tx_foot = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(11.7), Inches(0.3))
        p_f = tx_foot.text_frame.paragraphs[0]
        p_f.text = "Smart College Analytics System (SCAS) vs Legacy System | MCA Comparative Study"
        p_f.font.size = Pt(9)
        p_f.font.color.rgb = TEXT_MUTED
        p_f.font.name = 'Segoe UI'

    # =========================================================================
    # SLIDE 1: Title Slide (Dark Themed, High Visual Impact)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = BG_DARK
    bg1.line.fill.background()

    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.2), Inches(3.8), Inches(0.45))
    pill.fill.solid()
    pill.fill.fore_color.rgb = NAVY_PRIMARY
    pill.line.color.rgb = BLUE_ACCENT
    p_pill = pill.text_frame.paragraphs[0]
    p_pill.text = "ACADEMIC SYSTEM EVALUATION"
    p_pill.font.size = Pt(11)
    p_pill.font.bold = True
    p_pill.font.color.rgb = BLUE_ACCENT
    p_pill.alignment = PP_ALIGN.CENTER
    p_pill.font.name = 'Segoe UI'

    tb_title = s1.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.333), Inches(2.2))
    tf1 = tb_title.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "COMPARATIVE STUDY:"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_LIGHT
    p1.font.name = 'Segoe UI'

    p2 = tf1.add_paragraph()
    p2.text = "Legacy Manual System vs. Smart College Analytics System (SCAS)"
    p2.font.size = Pt(24)
    p2.font.bold = True
    p2.font.color.rgb = BLUE_ACCENT
    p2.font.name = 'Segoe UI'

    p3 = tf1.add_paragraph()
    p3.text = "A Quantitative & Architectural Analysis of Higher Education Digital Transformation"
    p3.font.size = Pt(14)
    p3.font.color.rgb = TEXT_MUTED
    p3.font.name = 'Segoe UI'

    div = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(4.5), Inches(11.333), Inches(0.04))
    div.fill.solid()
    div.fill.fore_color.rgb = BLUE_ACCENT
    div.line.fill.background()

    box_old = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.8), Inches(5.4), Inches(2.0))
    box_old.fill.solid()
    box_old.fill.fore_color.rgb = RGBColor(30, 41, 59)
    box_old.line.color.rgb = RED_ACCENT
    tf_old = box_old.text_frame
    tf_old.margin_left = tf_old.margin_top = Inches(0.2)
    p = tf_old.paragraphs[0]
    p.text = "[X] LEGACY TRADITIONAL SYSTEM"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(248, 113, 113)
    points_old = [
        "Paper registers & fragmented Excel sheets",
        "3-5 days delay in GPA/Attendance calculations",
        "High human error rate & zero predictive alerts"
    ]
    for pt in points_old:
        p_pt = tf_old.add_paragraph()
        p_pt.text = "• " + pt
        p_pt.font.size = Pt(11)
        p_pt.font.color.rgb = TEXT_LIGHT

    box_new = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(4.8), Inches(5.4), Inches(2.0))
    box_new.fill.solid()
    box_new.fill.fore_color.rgb = RGBColor(30, 41, 59)
    box_new.line.color.rgb = GREEN_ACCENT
    tf_new = box_new.text_frame
    tf_new.margin_left = tf_new.margin_top = Inches(0.2)
    p = tf_new.paragraphs[0]
    p.text = "[OK] SCAS PROPOSED PLATFORM"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(74, 222, 128)
    points_new = [
        "Unified Web ERP (React 19 + Flask + MySQL)",
        "Real-time instant GPA & attendance tracking",
        "100% calculation accuracy + Aptitude engine"
    ]
    for pt in points_new:
        p_pt = tf_new.add_paragraph()
        p_pt.text = "• " + pt
        p_pt.font.size = Pt(11)
        p_pt.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 2: Full-Slide High-Resolution Infographic Visual
    # =========================================================================
    infographic_path = os.path.join(os.getcwd(), "scas_vs_old_system_infographic.png")
    if os.path.exists(infographic_path):
        s2 = prs.slides.add_slide(blank_layout)
        s2.shapes.add_picture(infographic_path, Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))

    # =========================================================================
    # SLIDE 3: Full-Slide High-Resolution Workflow Architecture Visual
    # =========================================================================
    workflow_path = os.path.join(os.getcwd(), "scas_vs_old_system_workflow_diagram.png")
    if os.path.exists(workflow_path):
        s3 = prs.slides.add_slide(blank_layout)
        s3.shapes.add_picture(workflow_path, Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))

    # =========================================================================
    # SLIDE 4: Comprehensive Comparison Matrix (Table View)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "FEATURE-BY-FEATURE COMPARISON MATRIX", "DETAILED MODULE EVALUATION")

    rows, cols = 8, 3
    left, top, width, height = Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.4)
    table_shape = s4.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    table.columns[0].width = Inches(2.5)
    table.columns[1].width = Inches(4.6)
    table.columns[2].width = Inches(4.6)

    headers = ["Evaluation Metric / Module", "Legacy Traditional System", "SCAS (Smart College Analytics System)"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_LIGHT
        p.font.name = 'Segoe UI'

    matrix_data = [
        ["1. Attendance Tracking", "Paper registers, manual tallying at term-end, no alert triggers", "Real-time session logging with automated badge alerts (<75%)"],
        ["2. Result & GPA Processing", "Manual spreadsheet calculation, high latency, error-prone", "Automated SGPA/CGPA computing + dynamic Chart.js analytics graphs"],
        ["3. Leave & On-Duty Slips", "Physical paper applications, manual sign-offs, untracked", "Online application portal, real-time approval, status tracking"],
        ["4. Fee Ledger Management", "Physical receipt books, separate bank queues, delay in status", "Centralized fee status (Paid/Pending), auto receipt generation"],
        ["5. Campus Circulars & Alerts", "Physical notice boards, paper circulars, high notice miss rate", "Digital Notice Board with priority pinning and SMTP email alerts"],
        ["6. Placement & Skill Building", "Completely unaddressed; zero assessment integration", "Integrated Mock Placement Aptitude Engine with timed assessments"],
        ["7. Security & Data Integrity", "Physical ledgers vulnerable to loss, no role access control", "RBAC security, Werkzeug password hashing, normalized database"]
    ]

    for row_idx, row in enumerate(matrix_data):
        for col_idx, cell_value in enumerate(row):
            cell = table.cell(row_idx + 1, col_idx)
            cell.text = cell_value
            cell.fill.solid()
            bg_col = RGBColor(241, 245, 249) if row_idx % 2 == 1 else RGBColor(255, 255, 255)
            cell.fill.fore_color.rgb = bg_col
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_DARK
            p.font.name = 'Segoe UI'
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = NAVY_PRIMARY
            elif col_idx == 1:
                p.font.color.rgb = RGBColor(185, 28, 28)
            elif col_idx == 2:
                p.font.color.rgb = RGBColor(21, 128, 61)

    # =========================================================================
    # SLIDE 5: Visual Step-by-Step Flow Dynamics
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "STEP-BY-STEP WORKFLOW DYNAMICS", "PROCESS COMPARISON")

    phases = ["1. ATTENDANCE", "2. MARKS / GPA", "3. LEAVE APPROVAL", "4. NOTICES & ALERTS"]
    col_width = Inches(2.7)
    gap = Inches(0.25)
    start_left = Inches(0.8)

    for i, phase in enumerate(phases):
        left_pos = start_left + i * (col_width + gap)

        stg_box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.4), col_width, Inches(0.4))
        stg_box.fill.solid()
        stg_box.fill.fore_color.rgb = NAVY_PRIMARY
        stg_box.line.fill.background()
        p = stg_box.text_frame.paragraphs[0]
        p.text = phase
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_LIGHT
        p.alignment = PP_ALIGN.CENTER

        # Old Box
        old_box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.9), col_width, Inches(2.2))
        old_box.fill.solid()
        old_box.fill.fore_color.rgb = RED_LIGHT
        old_box.line.color.rgb = RED_ACCENT
        tf_o = old_box.text_frame
        tf_o.margin_left = tf_o.margin_top = tf_o.margin_right = Inches(0.15)
        tf_o.word_wrap = True
        p_o_h = tf_o.paragraphs[0]
        p_o_h.text = "[X] Traditional"
        p_o_h.font.bold = True
        p_o_h.font.size = Pt(11)
        p_o_h.font.color.rgb = RED_ACCENT

        old_step_texts = [
            ["Physical pen & paper", "Manual roll call", "No warning if <75%"],
            ["End-semester Excel tally", "Manual grade formulas", "Risk of human error"],
            ["Handwritten letter", "Physical faculty signatures", "Frequent lost requests"],
            ["Paper flyers on notice board", "Ignored circulars", "No direct notifications"]
        ]
        for t in old_step_texts[i]:
            p_t = tf_o.add_paragraph()
            p_t.text = "• " + t
            p_t.font.size = Pt(9.5)
            p_t.font.color.rgb = TEXT_DARK

        # SCAS Box
        scas_box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(4.3), col_width, Inches(2.5))
        scas_box.fill.solid()
        scas_box.fill.fore_color.rgb = GREEN_LIGHT
        scas_box.line.color.rgb = GREEN_ACCENT
        tf_s = scas_box.text_frame
        tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = Inches(0.15)
        tf_s.word_wrap = True
        p_s_h = tf_s.paragraphs[0]
        p_s_h.text = "[OK] SCAS Solution"
        p_s_h.font.bold = True
        p_s_h.font.size = Pt(11)
        p_s_h.font.color.rgb = GREEN_ACCENT

        scas_step_texts = [
            ["1-Click digital portal", "Real-time sync to DB", "Auto low-attendance alert"],
            ["Instant SGPA/CGPA engine", "Interactive visual charts", "Zero calculation error"],
            ["Multi-tier digital submit", "1-Click faculty approval", "Audit trail & live status"],
            ["Digital notice feed", "Instant priority pinning", "Automated SMTP emails"]
        ]
        for t in scas_step_texts[i]:
            p_t = tf_s.add_paragraph()
            p_t.text = "• " + t
            p_t.font.size = Pt(9.5)
            p_t.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 6: Quantitative Performance Metrics & Impact (Visual Scorecards)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "QUANTITATIVE PERFORMANCE METRICS & EFFICIENCY GAINS", "MEASURABLE IMPACT STUDY")

    kpis = [
        {
            "title": "ATTENDANCE TALLY TIME",
            "old": "3 - 5 Days per sem",
            "new": "Instant (0 sec)",
            "impact": "99.8% Time Saved",
            "desc": "Eliminates end-of-term manual counting of register books across all subjects."
        },
        {
            "title": "GPA EVALUATION ACCURACY",
            "old": "~85% - 90% (human error)",
            "new": "100% Deterministic",
            "impact": "Zero Calculation Bugs",
            "desc": "Automated formula processing eliminates rounding mistakes & mark discrepancies."
        },
        {
            "title": "LEAVE APPROVAL CYCLE",
            "old": "2 - 4 Days turnaround",
            "new": "< 5 Minutes",
            "impact": "95% Faster Approvals",
            "desc": "Digital notification & single-click faculty review replaces physical letter routing."
        },
        {
            "title": "NOTICE DISSEMINATION",
            "old": "24 - 48 Hours lag",
            "new": "Real-time + SMTP Mail",
            "impact": "100% Delivery Reach",
            "desc": "Instant notice broadcast directly to student/faculty dashboards & inboxes."
        },
        {
            "title": "PAPER CONSUMPTION",
            "old": "10,000+ Sheets / Year",
            "new": "0 Paper (100% Digital)",
            "impact": "Zero Paper Footprint",
            "desc": "Eco-friendly, paperless academic administration saving institutional costs."
        },
        {
            "title": "STUDENT CAREER PREP",
            "old": "Zero integrated support",
            "new": "Built-in Aptitude Engine",
            "impact": "Placement Ready",
            "desc": "Direct access to domain-specific practice exams and instant performance scoring."
        }
    ]

    card_w = Inches(3.7)
    card_h = Inches(2.55)
    row_gap = Inches(0.25)
    col_gap = Inches(0.3)

    for idx, kpi in enumerate(kpis):
        r_idx = idx // 3
        c_idx = idx % 3
        c_left = Inches(0.8) + c_idx * (card_w + col_gap)
        c_top = Inches(1.4) + r_idx * (card_h + row_gap)

        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, c_top, card_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BLUE_ACCENT

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = Inches(0.2)

        p_h = tf.paragraphs[0]
        p_h.text = kpi["title"]
        p_h.font.bold = True
        p_h.font.size = Pt(11)
        p_h.font.color.rgb = NAVY_PRIMARY

        p_imp = tf.add_paragraph()
        p_imp.text = ">>> " + kpi["impact"]
        p_imp.font.bold = True
        p_imp.font.size = Pt(12)
        p_imp.font.color.rgb = GREEN_ACCENT

        p_comp = tf.add_paragraph()
        r_o = p_comp.add_run()
        r_o.text = "Old: " + kpi["old"] + " -> "
        r_o.font.size = Pt(10)
        r_o.font.color.rgb = RED_ACCENT
        r_n = p_comp.add_run()
        r_n.text = "SCAS: " + kpi["new"]
        r_n.font.bold = True
        r_n.font.size = Pt(10)
        r_n.font.color.rgb = GREEN_ACCENT

        p_d = tf.add_paragraph()
        p_d.text = kpi["desc"]
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_before = Pt(4)

    # =========================================================================
    # SLIDE 7: Stakeholder Impact Breakdown (Admin, Faculty, Student)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "STAKEHOLDER BENEFITS: BEFORE VS AFTER SCAS", "VALUE PROPOSITION ANALYSIS")

    stakeholders = [
        {
            "role": "ADMINISTRATORS",
            "badge": "Institutional Governance",
            "color": BLUE_ACCENT,
            "before": [
                "Manual student/faculty records",
                "Paper-based fee reconciliations",
                "High administrative overhead",
                "Difficult to audit historical data"
            ],
            "after": [
                "Unified central admin dashboard",
                "Instant fee dues & receipt tracking",
                "Automated user credentials dispatch",
                "100% auditable SQL relational data"
            ]
        },
        {
            "role": "FACULTY MEMBERS",
            "badge": "Academic Execution",
            "color": NAVY_PRIMARY,
            "before": [
                "15+ minutes per session roll calling",
                "Manual mark registers & calculations",
                "Physical leave forms processing",
                "No instant alert for low attendance"
            ],
            "after": [
                "1-click digital attendance marking",
                "Direct CSV upload for internal marks",
                "Instant online leave approvals",
                "Automated student shortage flags (<75%)"
            ]
        },
        {
            "role": "STUDENTS",
            "badge": "Learner Experience",
            "color": GREEN_ACCENT,
            "before": [
                "Zero visibility into attendance %",
                "Surprise shortages during exam time",
                "Waiting weeks for internal marks",
                "No integrated placement prep"
            ],
            "after": [
                "Real-time attendance percentage",
                "Interactive SGPA & CGPA charts",
                "Instant online leave applications",
                "Built-in mock placement exam engine"
            ]
        }
    ]

    col_w = Inches(3.7)
    col_h = Inches(5.4)
    start_x = Inches(0.8)

    for i, sh in enumerate(stakeholders):
        cx = start_x + i * (col_w + Inches(0.3))

        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(1.4), col_w, col_h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = sh["color"]

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = Inches(0.2)

        p_t = tf.paragraphs[0]
        p_t.text = sh["role"]
        p_t.font.bold = True
        p_t.font.size = Pt(14)
        p_t.font.color.rgb = NAVY_PRIMARY

        p_b = tf.add_paragraph()
        p_b.text = sh["badge"]
        p_b.font.size = Pt(10)
        p_b.font.bold = True
        p_b.font.color.rgb = BLUE_ACCENT
        p_b.space_after = Pt(8)

        p_bf = tf.add_paragraph()
        p_bf.text = "[X] Before (Old System):"
        p_bf.font.bold = True
        p_bf.font.size = Pt(11)
        p_bf.font.color.rgb = RED_ACCENT
        for b in sh["before"]:
            p_item = tf.add_paragraph()
            p_item.text = "• " + b
            p_item.font.size = Pt(9.5)
            p_item.font.color.rgb = TEXT_DARK

        p_af = tf.add_paragraph()
        p_af.text = "[OK] After (SCAS Platform):"
        p_af.font.bold = True
        p_af.font.size = Pt(11)
        p_af.font.color.rgb = GREEN_ACCENT
        p_af.space_before = Pt(8)
        for a in sh["after"]:
            p_item = tf.add_paragraph()
            p_item.text = "• " + a
            p_item.font.size = Pt(9.5)
            p_item.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 8: Summary & Strategic Conclusion
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "SUMMARY & STRATEGIC CONCLUSION", "CONCLUSION & IMPACT")

    box_concl = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.4))
    box_concl.fill.solid()
    box_concl.fill.fore_color.rgb = BLUE_LIGHT
    box_concl.line.color.rgb = BLUE_ACCENT

    tf_c = box_concl.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = Inches(0.35)

    p_head = tf_c.paragraphs[0]
    p_head.text = "Key Conclusions from the Comparative Study:"
    p_head.font.bold = True
    p_head.font.size = Pt(18)
    p_head.font.color.rgb = NAVY_PRIMARY
    p_head.space_after = Pt(12)

    conclusions = [
        ("Operational Modernization: ", "SCAS transforms traditional fragmented paper registers and offline spreadsheets into a unified, cloud-ready Web ERP."),
        ("Significant Time & Cost Savings: ", "Reduces administrative calculation overhead by over 95%, eliminating paper costs and freeing faculty time for teaching."),
        ("Data Precision & Transparency: ", "Delivers 100% calculation accuracy for SGPA/CGPA and real-time attendance percentage tracking with automated threshold alerts (<75%)."),
        ("Holistic Career Empowerment: ", "Unlike legacy administrative tools, SCAS bridges academic tracking with career readiness via integrated mock placement aptitude testing."),
        ("High Scalability & Robust Architecture: ", "Modern 3-tier architecture (React 19 + Flask 3.0 + MySQL) ensures strict role-based access control (RBAC), data security, and seamless institutional scalability.")
    ]

    for title, desc in conclusions:
        p = tf_c.add_paragraph()
        r1 = p.add_run()
        r1.text = "[OK] " + title
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = NAVY_PRIMARY
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_DARK
        p.space_after = Pt(10)

    # Save output
    output_filename = "SCAS_vs_Old_System_Comparison.pptx"
    output_path = os.path.join(os.getcwd(), output_filename)
    prs.save(output_path)
    print(f"Comparison Presentation successfully created at: {output_path}")

if __name__ == "__main__":
    build_comparison_presentation()

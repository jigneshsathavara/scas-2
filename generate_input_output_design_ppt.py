"""
Smart College Analytics System (SCAS)
Master Script: Generate Comprehensive Input Design & Output Design Presentation (.pptx)
Aligned with Relational Database Data Dictionary (13 MySQL Tables)
"""

import os
import sys
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def add_run(p, text, bold=False, color=None, size=None, font_name='Segoe UI', italic=False):
    """Helper to safely append a styled run to a python-pptx paragraph."""
    run = p.add_run()
    run.text = text
    run.font.name = font_name
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color
    if size:
        run.font.size = size
    return run

def create_card(slide, left, top, width, height, bg_color, border_color=None, border_width=Pt(1)):
    """Helper to create a solid rounded rectangle card."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = border_width
    else:
        card.line.fill.background()
    return card

def draw_window_bar(slide, left, top, width, title_text, bg_color):
    """Draws a window / dialog header bar with macOS/modern style traffic light control dots."""
    bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.36))
    bar.fill.solid()
    bar.fill.fore_color.rgb = bg_color
    bar.line.fill.background()

    # Three window control dots
    dots = [RGBColor(239, 68, 68), RGBColor(245, 158, 11), RGBColor(34, 197, 94)]
    for i, c in enumerate(dots):
        d = slide.shapes.add_shape(MSO_SHAPE.OVAL, left + Inches(0.12 + i * 0.16), top + Inches(0.11), Inches(0.11), Inches(0.11))
        d.fill.solid()
        d.fill.fore_color.rgb = c
        d.line.fill.background()

    # Title text
    tx = slide.shapes.add_textbox(left + Inches(0.68), top + Inches(0.03), width - Inches(0.75), Inches(0.3))
    tf = tx.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.font.name = 'Segoe UI'

def style_spec_table(table, col_widths, headers, data, header_bg, text_light, row_alt, card_bg, navy_primary, fk_color, red_accent, green_accent, text_dark):
    """Styles a 5-column specification table for inputs/outputs."""
    for i, w in enumerate(col_widths):
        table.columns[i].width = w

    # Header Row
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = header_bg
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_left = cell.margin_right = Inches(0.05)
        cell.margin_top = cell.margin_bottom = Inches(0.02)
        tf = cell.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = h
        p.font.name = 'Segoe UI'
        p.font.bold = True
        p.font.size = Pt(8.5)
        p.font.color.rgb = text_light
        if j in [2, 3]:
            p.alignment = PP_ALIGN.CENTER
        else:
            p.alignment = PP_ALIGN.LEFT

    # Data Rows
    for r_idx, row in enumerate(data):
        bg = row_alt if r_idx % 2 == 1 else card_bg
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_left = cell.margin_right = Inches(0.05)
            cell.margin_top = cell.margin_bottom = Inches(0.02)
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = str(val)
            p.font.name = 'Segoe UI'
            p.font.size = Pt(8.0)

            if c_idx == 0:  # Field / Attribute
                p.font.bold = True
                p.font.color.rgb = navy_primary
            elif c_idx == 1:  # Control / Format
                p.font.color.rgb = RGBColor(67, 56, 202)
                p.font.size = Pt(7.8)
            elif c_idx == 2:  # Data Type & Length
                p.alignment = PP_ALIGN.CENTER
                p.font.name = 'Consolas'
                p.font.size = Pt(7.8)
                p.font.color.rgb = fk_color
            elif c_idx == 3:  # Required
                p.alignment = PP_ALIGN.CENTER
                p.font.bold = True
                if "YES" in str(val).upper():
                    p.font.color.rgb = red_accent
                else:
                    p.font.color.rgb = green_accent
            else:  # Constraints & Validation
                p.font.color.rgb = text_dark

def draw_input_wireframe(slide, left, top, width, height, form_title, fields, button_text, badge_text, navy_color, blue_accent, border_color):
    """Draws a visual UI wireframe representing a web form with input boxes, labels, and actions."""
    # Outer Container Card
    container = create_card(slide, left, top, width, height, RGBColor(255, 255, 255), border_color, Pt(1.5))
    
    # Header bar
    draw_window_bar(slide, left, top, width, form_title, navy_color)

    # Role Badge
    badge_w = Inches(2.2)
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + width - badge_w - Inches(0.2), top + Inches(0.44), badge_w, Inches(0.25))
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(238, 242, 255)
    badge.line.color.rgb = RGBColor(99, 102, 241)
    p_b = badge.text_frame.paragraphs[0]
    p_b.text = badge_text
    p_b.font.size = Pt(7.5)
    p_b.font.bold = True
    p_b.font.color.rgb = RGBColor(67, 56, 202)
    p_b.alignment = PP_ALIGN.CENTER

    # Render Form Fields
    curr_y = top + Inches(0.72)
    avail_h = height - Inches(1.4)
    num_fields = len(fields)
    step_y = avail_h / max(num_fields, 1)

    for f_idx, field in enumerate(fields):
        flabel, fval, ftype = field[0], field[1], field[2] if len(field) > 2 else "text"
        
        # Label
        lbl_box = slide.shapes.add_textbox(left + Inches(0.2), curr_y, width - Inches(0.4), Inches(0.22))
        lbl_tf = lbl_box.text_frame
        lbl_tf.margin_left = lbl_tf.margin_top = lbl_tf.margin_right = lbl_tf.margin_bottom = 0
        lbl_p = lbl_tf.paragraphs[0]
        lbl_p.text = flabel.upper()
        lbl_p.font.size = Pt(7.5)
        lbl_p.font.bold = True
        lbl_p.font.color.rgb = RGBColor(71, 85, 105)

        # Input Box
        box_h = Inches(0.30)
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.2), curr_y + Inches(0.20), width - Inches(0.4), box_h)
        box.fill.solid()
        box.fill.fore_color.rgb = RGBColor(248, 250, 252)
        box.line.color.rgb = RGBColor(203, 213, 225)
        box.line.width = Pt(1)

        val_tf = box.text_frame
        val_tf.margin_left = Inches(0.1)
        val_tf.margin_top = Inches(0.04)
        val_p = val_tf.paragraphs[0]
        val_p.text = fval
        val_p.font.size = Pt(8.0)
        val_p.font.color.rgb = RGBColor(30, 41, 59) if ftype != "placeholder" else RGBColor(148, 163, 184)
        if ftype == "placeholder":
            val_p.font.italic = True

        # Dropdown arrow indicator if select
        if ftype == "select":
            arrow = slide.shapes.add_textbox(left + width - Inches(0.55), curr_y + Inches(0.22), Inches(0.3), Inches(0.25))
            ap = arrow.text_frame.paragraphs[0]
            ap.text = "▼"
            ap.font.size = Pt(7.5)
            ap.font.color.rgb = RGBColor(100, 116, 139)

        curr_y += step_y

    # Action Button
    btn_w = width - Inches(0.4)
    btn = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.2), top + height - Inches(0.48), btn_w, Inches(0.34))
    btn.fill.solid()
    btn.fill.fore_color.rgb = blue_accent
    btn.line.fill.background()
    btn_p = btn.text_frame.paragraphs[0]
    btn_p.text = button_text
    btn_p.font.size = Pt(9.0)
    btn_p.font.bold = True
    btn_p.font.color.rgb = RGBColor(255, 255, 255)
    btn_p.alignment = PP_ALIGN.CENTER

def build_full_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Master Color Theme
    BG_DARK = RGBColor(15, 23, 42)          # Slate 900
    NAVY_PRIMARY = RGBColor(26, 54, 93)     # #1A365D - Deep Navy
    BLUE_ACCENT = RGBColor(49, 130, 206)    # #3182CE - Tech Blue
    BLUE_LIGHT = RGBColor(235, 248, 255)    # #EBF8FF - Light Card Tint
    CARD_BG = RGBColor(255, 255, 255)       # White
    ROW_ALT = RGBColor(248, 250, 252)       # Slate 50
    TEXT_LIGHT = RGBColor(248, 250, 252)    # White
    TEXT_MUTED = RGBColor(100, 116, 139)    # Slate 500
    TEXT_DARK = RGBColor(30, 41, 59)        # Slate 800
    BORDER_LIGHT = RGBColor(203, 213, 225)  # Slate 300
    BORDER_DARK = RGBColor(71, 85, 105)     # Slate 600

    PK_COLOR = RGBColor(180, 83, 9)         # Amber 700
    FK_COLOR = RGBColor(29, 78, 216)        # Blue 700
    GREEN_ACCENT = RGBColor(22, 163, 74)    # Green 600
    GREEN_LIGHT = RGBColor(240, 253, 244)   # Green 50
    RED_ACCENT = RGBColor(220, 38, 38)      # Red 600
    RED_LIGHT = RGBColor(254, 242, 242)     # Red 50
    AMBER_ACCENT = RGBColor(217, 119, 6)    # Amber 600
    PURPLE_ACCENT = RGBColor(126, 34, 206)  # Purple 700

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="SCAS - INPUT & OUTPUT DESIGN SPECIFICATION"):
        banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.12))
        banner.fill.solid()
        banner.fill.fore_color.rgb = NAVY_PRIMARY
        banner.line.fill.background()

        # Category tag
        tx_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.10), Inches(11.733), Inches(0.26))
        tf_c = tx_cat.text_frame
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
        p_c = tf_c.paragraphs[0]
        p_c.text = category_text.upper()
        p_c.font.size = Pt(9.5)
        p_c.font.bold = True
        p_c.font.color.rgb = BLUE_ACCENT
        p_c.font.name = 'Segoe UI'

        # Main Title
        tx_t = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.733), Inches(0.60))
        tf_t = tx_t.text_frame
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(21)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_LIGHT
        p_t.font.name = 'Segoe UI'

        # Footer
        tx_foot = slide.shapes.add_textbox(Inches(0.8), Inches(7.14), Inches(11.733), Inches(0.28))
        p_f = tx_foot.text_frame.paragraphs[0]
        p_f.text = "Smart College Analytics System (SCAS) | Input & Output Design Specification | Master of Computer Applications (MCA)"
        p_f.font.size = Pt(9)
        p_f.font.color.rgb = TEXT_MUTED
        p_f.font.name = 'Segoe UI'

    # Headers for specification tables
    HEADERS_SPEC = ["Field / Element", "UI Control", "Data Type", "Req?", "Validation Rules & Logic"]
    COL_W_SPEC = [Inches(1.5), Inches(1.2), Inches(1.0), Inches(0.6), Inches(2.2)]

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = BG_DARK
    bg1.line.fill.background()

    # Pill badge
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.1), Inches(4.8), Inches(0.42))
    pill.fill.solid()
    pill.fill.fore_color.rgb = NAVY_PRIMARY
    pill.line.color.rgb = BLUE_ACCENT
    p_pill = pill.text_frame.paragraphs[0]
    p_pill.text = "SOFTWARE ENGINEERING & SYSTEM DESIGN DEFENSE"
    p_pill.font.size = Pt(10.0)
    p_pill.font.bold = True
    p_pill.font.color.rgb = BLUE_ACCENT

    # Main Title
    tx1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(1.5))
    tf1 = tx1.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "Smart College Analytics System"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_LIGHT

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Comprehensive Input Design & Output Design Specification"
    p1_sub.font.size = Pt(22)
    p1_sub.font.color.rgb = BLUE_ACCENT
    p1_sub.space_before = Pt(6)

    # 4 Feature Badges
    badges = [
        ("🔐 12 Input Forms & Ingestion", "Form Controls, Validations, Bulk CSV Engine, RBAC Security"),
        ("📊 10 Output Displays & Reports", "Executive Dashboards, AI Dropout Risk, Official Transcripts, Receipts"),
        ("🗄️ Relational Schema Traceability", "Full Field-to-Entity Mapping Across 13 MySQL Tables (scas_*)"),
        ("⚡ Machine Learning & Automation", "Real-Time SGPA/CGPA Tabulation, Predictive Heuristics, SMTP Mail")
    ]
    for b_idx, (b_title, b_desc) in enumerate(badges):
        bx = Inches(1.0 + (b_idx % 2) * 5.8)
        by = Inches(3.7 + (b_idx // 2) * 1.5)
        card = create_card(s1, bx, by, Inches(5.5), Inches(1.25), RGBColor(30, 41, 59), BLUE_ACCENT)
        tf = card.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.16)
        pt = tf.paragraphs[0]
        pt.text = b_title
        pt.font.size = Pt(13)
        pt.font.bold = True
        pt.font.color.rgb = TEXT_LIGHT
        pd = tf.add_paragraph()
        pd.text = b_desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = RGBColor(148, 163, 184)
        pd.space_before = Pt(4)

    # Author metadata
    tx_meta = s1.shapes.add_textbox(Inches(1.0), Inches(6.8), Inches(11.333), Inches(0.4))
    pm = tx_meta.text_frame.paragraphs[0]
    pm.text = "Master of Computer Applications (MCA) | Department of Computer Science & Applications | Academic Year 2024-2026"
    pm.font.size = Pt(10)
    pm.font.color.rgb = RGBColor(148, 163, 184)

    # =========================================================================
    # SLIDE 2: System Design Methodology & Principles
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "System Design Philosophy: Input vs. Output Architecture", "DESIGN METHODOLOGY & CORE PRINCIPLES")

    # Left Column: Input Design Framework
    c_in = create_card(s2, Inches(0.8), Inches(1.3), Inches(5.6), Inches(4.3), CARD_BG, BORDER_LIGHT)
    tf_in = c_in.text_frame
    tf_in.margin_left = tf_in.margin_right = tf_in.margin_top = Inches(0.2)
    p = tf_in.paragraphs[0]
    p.text = "📥 INPUT DESIGN PRINCIPLES & GOALS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY

    in_pts = [
        ("Ergonomic Data Entry: ", "Intuitive form controls (text, date pickers, dropdowns, switches) minimizing user keystrokes."),
        ("Defensive Validation Tier: ", "Multi-tier checks (Client-side HTML5/JS + Server-side Flask/WTForms + DB Integrity Constraints)."),
        ("Strict Data Integrity: ", "FK integrity, composite unique constraints, Scrypt password hashing, and anti-tamper controls."),
        ("Bulk Asynchronous Ingestion: ", "High-throughput CSV import with header parsing, transactional rollback, and error logging."),
        ("Role-Based Input Access: ", "@role_required gatekeepers ensuring users only access authorized entry forms.")
    ]
    for h, b in in_pts:
        pi = tf_in.add_paragraph()
        pi.space_before = Pt(8)
        add_run(pi, "• " + h, bold=True, color=NAVY_PRIMARY, size=Pt(9.0))
        add_run(pi, b, color=TEXT_DARK, size=Pt(8.8))

    # Right Column: Output Design Framework
    c_out = create_card(s2, Inches(6.9), Inches(1.3), Inches(5.6), Inches(4.3), CARD_BG, BORDER_LIGHT)
    tf_out = c_out.text_frame
    tf_out.margin_left = tf_out.margin_right = tf_out.margin_top = Inches(0.2)
    p2 = tf_out.paragraphs[0]
    p2.text = "📤 OUTPUT DESIGN PRINCIPLES & GOALS"
    p2.font.size = Pt(13)
    p2.font.bold = True
    p2.font.color.rgb = NAVY_PRIMARY

    out_pts = [
        ("Executive & Operational Visibility: ", "Instant KPI metric cards, progress bars, and historical activity streams."),
        ("Predictive Risk Intelligence: ", "Automated AI decision models flagging dropout risks with actionable color-coded alerts."),
        ("Official Formal Documents: ", "Print-optimized CSS templates for Semester Grade Transcripts and Payment Receipts."),
        ("Multi-Format Deliverables: ", "Screen dashboards, exportable CSV registers, printable HTML, and transactional SMTP emails."),
        ("Ergonomic Visual Hierarchy: ", "WCAG 2.1 AA contrast compliance, responsive cards, and clean typography.")
    ]
    for h, b in out_pts:
        po = tf_out.add_paragraph()
        po.space_before = Pt(8)
        add_run(po, "• " + h, bold=True, color=BLUE_ACCENT, size=Pt(9.0))
        add_run(po, b, color=TEXT_DARK, size=Pt(8.8))

    # Bottom Callout: End-to-End Flow
    flow_card = create_card(s2, Inches(0.8), Inches(5.8), Inches(11.7), Inches(1.15), BLUE_LIGHT, BLUE_ACCENT)
    tf_f = flow_card.text_frame
    tf_f.margin_left = tf_f.margin_right = tf_f.margin_top = Inches(0.14)
    pf_title = tf_f.paragraphs[0]
    pf_title.text = "🔄 END-TO-END DATA CONVERSION PIPELINE"
    pf_title.font.size = Pt(11)
    pf_title.font.bold = True
    pf_title.font.color.rgb = NAVY_PRIMARY

    pf_flow = tf_f.add_paragraph()
    pf_flow.space_before = Pt(4)
    flow_steps = [
        ("User Input Forms", "Web controls & CSV upload"),
        ("Validation & Sanitization", "CSRF, Scrypt, Type casts"),
        ("MySQL DB Entities", "13 Relational Tables (scas_*)"),
        ("Analytics Engine", "SGPA/CGPA, 45/55 AI Risk Model"),
        ("Stakeholder Outputs", "Dashboards, Printables & Mails")
    ]
    for idx, (st, desc) in enumerate(flow_steps):
        add_run(pf_flow, f"[{st}]", bold=True, color=NAVY_PRIMARY, size=Pt(9.0))
        if idx < len(flow_steps) - 1:
            add_run(pf_flow, "  ➔  ", bold=True, color=BLUE_ACCENT, size=Pt(9.5))

    # =========================================================================
    # SLIDE 3: Input Architecture & UI Control Framework
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Standardized Input Architecture & UI Control Matrix", "INPUT CONTROL CATALOG & VALIDATION TIERS")

    # Table of standard controls
    ctrl_headers = ["Control Type", "HTML / Component Element", "Target Database Binding", "Client Validation Tier", "Server Validation & Security"]
    ctrl_widths = [Inches(1.8), Inches(2.2), Inches(2.2), Inches(2.6), Inches(2.9)]
    ctrl_data = [
        ("Single-Line Text", "<input type='text'>", "scas_users.name / roll_no", "required, maxlength, pattern", "strip(), XSS escape, regex checks"),
        ("Masked Secret", "<input type='password'>", "scas_users.password_hash", "minlength='8', complexity meter", "Scrypt hash (scrypt:32768:8:1)"),
        ("Email Identifier", "<input type='email'>", "scas_users.email", "HTML5 email regex RFC 5322", "DNS domain lookup, uniqueness test"),
        ("Calendar Date", "<input type='date'>", "scas_attendance.date, leave", "min/max bounds, format YYYY-MM-DD", "datetime.strptime validation"),
        ("Searchable Select", "<select> dropdown", "course_id, batch_id, faculty_id", "required selection (!= '')", "FK existence check in DB session"),
        ("Binary Switch Toggle", "<input type='checkbox/radio'>", "scas_attendance.status", "Default checked state", "Enum constraint ('Present'/'Absent')"),
        ("Numeric Score Box", "<input type='number' step='0.5'>", "scas_marks.marks_obtained", "min='0', max=max_marks", "Float cast, range: 0.0 <= mark <= max"),
        ("Multi-Part File Drop", "<input type='file' accept='.csv'>", "Batch Ingestion Buffer", "File extension filter (.csv)", "MIME check, UTF-8 parse, rollback"),
        ("Multi-Line Text Area", "<textarea rows='4'>", "scas_leave_applications.reason", "maxlength='500', char counter", "HTML entity encoding, SQL escape")
    ]
    t_ctrl = s3.shapes.add_table(len(ctrl_data) + 1, 5, Inches(0.8), Inches(1.3), Inches(11.7), Inches(4.3)).table
    style_spec_table(t_ctrl, ctrl_widths, ctrl_headers, ctrl_data, NAVY_PRIMARY, TEXT_LIGHT, ROW_ALT, CARD_BG, NAVY_PRIMARY, FK_COLOR, RED_ACCENT, GREEN_ACCENT, TEXT_DARK)

    # Callout at bottom
    c_note = create_card(s3, Inches(0.8), Inches(5.8), Inches(11.7), Inches(1.15), BLUE_LIGHT, BLUE_ACCENT)
    tf_cn = c_note.text_frame
    tf_cn.margin_left = tf_cn.margin_right = tf_cn.margin_top = Inches(0.14)
    pcn = tf_cn.paragraphs[0]
    pcn.text = "🛡️ DEFENSIVE THREE-TIER VALIDATION ARCHITECTURE"
    pcn.font.size = Pt(11)
    pcn.font.bold = True
    pcn.font.color.rgb = NAVY_PRIMARY

    pcn_sub = tf_cn.add_paragraph()
    pcn_sub.space_before = Pt(4)
    add_run(pcn_sub, "• Tier 1 (Client): ", bold=True, color=NAVY_PRIMARY, size=Pt(9.0))
    add_run(pcn_sub, "Instant browser validation preventing unnecessary HTTP requests; dynamic DOM error indicators. ", color=TEXT_DARK, size=Pt(8.8))
    add_run(pcn_sub, "• Tier 2 (Flask Server): ", bold=True, color=BLUE_ACCENT, size=Pt(9.0))
    add_run(pcn_sub, "Sanitization, role decorator verification (@role_required), cryptographic token checks, flash messages. ", color=TEXT_DARK, size=Pt(8.8))
    add_run(pcn_sub, "• Tier 3 (Database): ", bold=True, color=GREEN_ACCENT, size=Pt(9.0))
    add_run(pcn_sub, "Strict MySQL relational schema, Foreign Key cascade rules, and unique index constraints prevent corrupt state.", color=TEXT_DARK, size=Pt(8.8))

    # =========================================================================
    # SLIDE 4: Input Design 1 — Authentication & Login Interface
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Input Design 1: System Authentication & Portal Login", "AUTHENTICATION & ACCESS CONTROL (AUTH)")

    # Left: Specs Table & Security Callout
    t_s4 = s4.shapes.add_table(5, 5, Inches(0.8), Inches(1.3), Inches(6.5), Inches(2.6)).table
    s4_data = [
        ("username / email", "Text Input", "VARCHAR(120)", "YES", "Accepts either unique username or email"),
        ("password", "Password Box", "VARCHAR(255)", "YES", "Masked chars; checked against Scrypt hash"),
        ("remember_me", "Checkbox", "BOOLEAN", "NO", "Preserves Flask session cookie across restart"),
        ("csrf_token", "Hidden Field", "VARCHAR(64)", "YES", "Synchronizer Token Pattern CSRF prevention")
    ]
    style_spec_table(t_s4, [Inches(1.5), Inches(1.1), Inches(1.0), Inches(0.5), Inches(2.4)], HEADERS_SPEC, s4_data, NAVY_PRIMARY, TEXT_LIGHT, ROW_ALT, CARD_BG, NAVY_PRIMARY, FK_COLOR, RED_ACCENT, GREEN_ACCENT, TEXT_DARK)

    # Security Box
    c_sec4 = create_card(s4, Inches(0.8), Inches(4.1), Inches(6.5), Inches(2.8), BLUE_LIGHT, BLUE_ACCENT)
    tf_s4 = c_sec4.text_frame
    tf_s4.margin_left = tf_s4.margin_right = tf_s4.margin_top = Inches(0.16)
    ps4_t = tf_s4.paragraphs[0]
    ps4_t.text = "🔒 AUTHENTICATION LOGIC & ROLE ROUTING"
    ps4_t.font.size = Pt(11)
    ps4_t.font.bold = True
    ps4_t.font.color.rgb = NAVY_PRIMARY

    sec4_notes = [
        ("Scrypt Hash Verification: ", "Passwords validated via check_password_hash() (Werkzeug). Plaintext is never stored or logged."),
        ("Multi-Role Gateway: ", "Single unified entry point automatically inspects session['role'] and redirects to /admin, /faculty, or /student."),
        ("Brute-Force Mitigation: ", "Failed login increments attempt counter; flash warnings alert users without revealing account existence.")
    ]
    for h, b in sec4_notes:
        p = tf_s4.add_paragraph()
        p.space_before = Pt(6)
        add_run(p, "• " + h, bold=True, color=NAVY_PRIMARY, size=Pt(8.8))
        add_run(p, b, color=TEXT_DARK, size=Pt(8.6))

    # Right: Wireframe Mockup
    s4_fields = [
        ("Username or Institutional Email", "admin@college.edu", "text"),
        ("Password", "••••••••••••", "text"),
        ("Role Selector", "Administrator / Faculty / Student", "select")
    ]
    draw_input_wireframe(s4, Inches(7.6), Inches(1.3), Inches(4.9), Inches(5.6), "SCAS - Secure Institutional Login", s4_fields, "Sign In to Portal", "ROLE: ALL USERS", NAVY_PRIMARY, BLUE_ACCENT, BORDER_LIGHT)

    # =========================================================================
    # SLIDE 5: Input Design 2 — Password Recovery & Reset
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Input Design 2: Self-Service Password Recovery & Reset", "CREDENTIAL LIFECYCLE (AUTH)")

    t_s5 = s5.shapes.add_table(5, 5, Inches(0.8), Inches(1.3), Inches(6.5), Inches(2.6)).table
    s5_data = [
        ("registered_email", "Email Input", "VARCHAR(120)", "YES", "Must exist in scas_users; RFC 5322 regex"),
        ("reset_token", "URL / Hidden", "VARCHAR(255)", "YES", "URL-safe HMAC token; 3600s TTL expiry"),
        ("new_password", "Password Box", "VARCHAR(80)", "YES", "Min 8 chars, 1 uppercase, 1 digit, 1 symbol"),
        ("confirm_password", "Password Box", "VARCHAR(80)", "YES", "Must match new_password exactly")
    ]
    style_spec_table(t_s5, [Inches(1.5), Inches(1.1), Inches(1.0), Inches(0.5), Inches(2.4)], HEADERS_SPEC, s5_data, NAVY_PRIMARY, TEXT_LIGHT, ROW_ALT, CARD_BG, NAVY_PRIMARY, FK_COLOR, RED_ACCENT, GREEN_ACCENT, TEXT_DARK)

    c_sec5 = create_card(s5, Inches(0.8), Inches(4.1), Inches(6.5), Inches(2.8), BLUE_LIGHT, BLUE_ACCENT)
    tf_s5 = c_sec5.text_frame
    tf_s5.margin_left = tf_s5.margin_right = tf_s5.margin_top = Inches(0.16)
    ps5_t = tf_s5.paragraphs[0]
    ps5_t.text = "🔑 CRYPTOGRAPHIC TOKEN WORKFLOW"
    ps5_t.font.size = Pt(11)
    ps5_t.font.bold = True
    ps5_t.font.color.rgb = NAVY_PRIMARY

    sec5_notes = [
        ("itsdangerous TimedSerializer: ", "Generates signed token encoding user email and timestamp with secret salt."),
        ("1-Hour Expiration: ", "Tokens older than 3600 seconds trigger SignatureExpired exception and are rejected."),
        ("Transactional Dispatch: ", "Delivers tokenized reset link via SMTP (or transactional mock transport in sent_emails.log).")
    ]
    for h, b in sec5_notes:
        p = tf_s5.add_paragraph()
        p.space_before = Pt(6)
        add_run(p, "• " + h, bold=True, color=NAVY_PRIMARY, size=Pt(8.8))
        add_run(p, b, color=TEXT_DARK, size=Pt(8.6))

    s5_fields = [
        ("Registered Institutional Email", "student@college.edu", "text"),
        ("Enter Security Reset Token", "arvpQQ.T52BADI8Hexb6GsFdLe...", "placeholder"),
        ("New Secure Password", "••••••••••••", "text"),
        ("Confirm New Password", "••••••••••••", "text")
    ]
    draw_input_wireframe(s5, Inches(7.6), Inches(1.3), Inches(4.9), Inches(5.6), "Self-Service Password Reset", s5_fields, "Reset & Save Password", "ROLE: ALL USERS", NAVY_PRIMARY, BLUE_ACCENT, BORDER_LIGHT)

    # =========================================================================
    # SLIDE 6: Input Design 3 — In-App User Credential Update
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Input Design 3: In-App User Profile & Credential Update", "USER ACCOUNT SECURITY (SHARED)")

    t_s6 = s6.shapes.add_table(4, 5, Inches(0.8), Inches(1.3), Inches(6.5), Inches(2.5)).table
    s6_data = [
        ("current_password", "Password Box", "VARCHAR(255)", "YES", "Verified against active session user hash"),
        ("new_password", "Password Box", "VARCHAR(80)", "YES", "Must differ from current; min 8 characters"),
        ("confirm_password", "Password Box", "VARCHAR(80)", "YES", "Exact match check on client & server")
    ]
    style_spec_table(t_s6, [Inches(1.5), Inches(1.1), Inches(1.0), Inches(0.5), Inches(2.4)], HEADERS_SPEC, s6_data, NAVY_PRIMARY, TEXT_LIGHT, ROW_ALT, CARD_BG, NAVY_PRIMARY, FK_COLOR, RED_ACCENT, GREEN_ACCENT, TEXT_DARK)

    c_sec6 = create_card(s6, Inches(0.8), Inches(4.0), Inches(6.5), Inches(2.9), BLUE_LIGHT, BLUE_ACCENT)
    tf_s6 = c_sec6.text_frame
    tf_s6.margin_left = tf_s6.margin_right = tf_s6.margin_top = Inches(0.16)
    ps6_t = tf_s6.paragraphs[0]
    ps6_t.text = "🛡️ SESSION VALIDATION & AUDITING"
    ps6_t.font.size = Pt(11)
    ps6_t.font.bold = True
    ps6_t.font.color.rgb = NAVY_PRIMARY

    sec6_notes = [
        ("Zero Privilege Escalation: ", "Users can only alter their own credentials bound to session['user_id']."),
        ("Non-Reuse Policy: ", "Prevents setting new password identical to current hash to enforce credential rotation."),
        ("Audit Telemetry: ", "Successful password updates flash an affirmative alert and log an event in server activity history.")
    ]
    for h, b in sec6_notes:
        p = tf_s6.add_paragraph()
        p.space_before = Pt(6)
        add_run(p, "• " + h, bold=True, color=NAVY_PRIMARY, size=Pt(8.8))
        add_run(p, b, color=TEXT_DARK, size=Pt(8.6))

    s6_fields = [
        ("Current Password", "••••••••••••", "text"),
        ("New Password", "Enter at least 8 chars...", "placeholder"),
        ("Confirm New Password", "Re-enter new password...", "placeholder")
    ]
    draw_input_wireframe(s6, Inches(7.6), Inches(1.3), Inches(4.9), Inches(5.6), "In-App Password Management", s6_fields, "Update Password", "ROLE: AUTHENTICATED", NAVY_PRIMARY, BLUE_ACCENT, BORDER_LIGHT)

    # =========================================================================
    # SLIDE 7: Input Design 4 — Administrator User Creation
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Input Design 4: Admin Account Creation & Credential Dispatch", "USER LIFECYCLE MANAGEMENT (ADMIN)")

    t_s7 = s7.shapes.add_table(7, 5, Inches(0.8), Inches(1.3), Inches(6.5), Inches(3.0)).table
    s7_data = [
        ("name", "Text Input", "VARCHAR(100)", "YES", "Full legal institutional name"),
        ("username", "Text Input", "VARCHAR(80)", "YES", "Unique login identifier across system"),
        ("email", "Email Input", "VARCHAR(120)", "YES", "Globally unique contact email address"),
        ("role", "Dropdown", "VARCHAR(20)", "YES", "Enum selector: 'faculty' or 'student'"),
        ("department / roll_no", "Text Input", "VARCHAR(100/30)", "YES", "Dept for faculty; unique Roll No for student"),
        ("batch_id / course_id", "Dropdown", "INT(11)", "COND", "Required if student; maps to scas_batches")
    ]
    style_spec_table(t_s7, [Inches(1.5), Inches(1.1), Inches(1.0), Inches(0.5), Inches(2.4)], HEADERS_SPEC, s7_data, NAVY_PRIMARY, TEXT_LIGHT, ROW_ALT, CARD_BG, NAVY_PRIMARY, FK_COLOR, RED_ACCENT, GREEN_ACCENT, TEXT_DARK)

    c_sec7 = create_card(s7, Inches(0.8), Inches(4.5), Inches(6.5), Inches(2.4), BLUE_LIGHT, BLUE_ACCENT)
    tf_s7 = c_sec7.text_frame
    tf_s7.margin_left = tf_s7.margin_right = tf_s7.margin_top = Inches(0.14)
    ps7_t = tf_s7.paragraphs[0]
    ps7_t.text = "⚙️ AUTOMATED PROVISIONING LOGIC"
    ps7_t.font.size = Pt(11)
    ps7_t.font.bold = True
    ps7_t.font.color.rgb = NAVY_PRIMARY

    sec7_notes = [
        ("Atomic Multi-Table Insert: ", "Inserts into scas_users and simultaneously creates 1:1 profile in faculty or student profile table."),
        ("Temporary Credential Dispatch: ", "Generates random default password and triggers email dispatch with login credentials.")
    ]
    for h, b in sec7_notes:
        p = tf_s7.add_paragraph()
        p.space_before = Pt(4)
        add_run(p, "• " + h, bold=True, color=NAVY_PRIMARY, size=Pt(8.8))
        add_run(p, b, color=TEXT_DARK, size=Pt(8.6))

    s7_fields = [
        ("Full Legal Name", "Prof. CD Patel", "text"),
        ("Email Address", "cdpatel@college.edu", "text"),
        ("Portal Role", "Faculty Member", "select"),
        ("Department / Designation", "Computer Applications | Professor", "text"),
        ("Auto-Email Credentials", "☑ Send temporary credentials via email", "placeholder")
    ]
    draw_input_wireframe(s7, Inches(7.6), Inches(1.3), Inches(4.9), Inches(5.6), "Create New User Account", s7_fields, "Provision Account", "ROLE: ADMINISTRATOR", NAVY_PRIMARY, BLUE_ACCENT, BORDER_LIGHT)

    # =========================================================================
    # SLIDE 8: Input Design 5 — Bulk CSV Ingestion Engine
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Input Design 5: Bulk CSV Data Ingestion Engine", "BATCH IMPORT & DATA PIPELINE (ADMIN)")

    t_s8 = s8.shapes.add_table(5, 5, Inches(0.8), Inches(1.3), Inches(6.5), Inches(2.6)).table
    s8_data = [
        ("csv_file", "File Dropzone", "MIME: text/csv", "YES", "Max 5MB file; UTF-8 encoding mandatory"),
        ("import_entity", "Dropdown", "ENUM", "YES", "Target: 'students', 'faculty', 'subjects', 'marks'"),
        ("header_mapping", "Auto-Detected", "ARRAY", "YES", "Validates presence of required schema headers"),
        ("on_conflict", "Radio Group", "ENUM", "YES", "'Skip duplicates' or 'Update existing records'")
    ]
    style_spec_table(t_s8, [Inches(1.5), Inches(1.1), Inches(1.0), Inches(0.5), Inches(2.4)], HEADERS_SPEC, s8_data, NAVY_PRIMARY, TEXT_LIGHT, ROW_ALT, CARD_BG, NAVY_PRIMARY, FK_COLOR, RED_ACCENT, GREEN_ACCENT, TEXT_DARK)

    c_sec8 = create_card(s8, Inches(0.8), Inches(4.1), Inches(6.5), Inches(2.8), BLUE_LIGHT, BLUE_ACCENT)
    tf_s8 = c_sec8.text_frame
    tf_s8.margin_left = tf_s8.margin_right = tf_s8.margin_top = Inches(0.16)
    ps8_t = tf_s8.paragraphs[0]
    ps8_t.text = "⚡ BATCH PARSING & ERROR RESILIENCE"
    ps8_t.font.size = Pt(11)
    ps8_t.font.bold = True
    ps8_t.font.color.rgb = NAVY_PRIMARY

    sec8_notes = [
        ("Streaming Row Validation: ", "Inspects each row for missing cells, bad emails, or duplicate roll numbers before staging."),
        ("Transactional Isolation: ", "Utilizes db.session.begin_nested() to guarantee partial rollback if corrupt records occur."),
        ("Error Log Telemetry: ", "Generates detailed error report showing specific row index and offending column for bad rows.")
    ]
    for h, b in sec8_notes:
        p = tf_s8.add_paragraph()
        p.space_before = Pt(6)
        add_run(p, "• " + h, bold=True, color=NAVY_PRIMARY, size=Pt(8.8))
        add_run(p, b, color=TEXT_DARK, size=Pt(8.6))

    s8_fields = [
        ("Select Upload Category", "Student Enrollment Roster", "select"),
        ("Attach CSV Spreadsheet", "students_mca_2026.csv (24.5 KB)", "text"),
        ("Conflict Resolution", "Skip existing duplicates and log", "select"),
        ("Validation Status", "✓ 60 Rows Detected | Headers Match", "placeholder")
    ]
    draw_input_wireframe(s8, Inches(7.6), Inches(1.3), Inches(4.9), Inches(5.6), "Bulk CSV Upload Portal", s8_fields, "Upload & Import Roster", "ROLE: ADMINISTRATOR", NAVY_PRIMARY, BLUE_ACCENT, BORDER_LIGHT)

    # =========================================================================
    # SLIDE 9: Input Design 6 — Academic Program, Batch & Subject Setup
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Input Design 6: Academic Program, Batch & Curriculum Setup", "ACADEMIC SETUP & CURRICULUM (ADMIN)")

    t_s9 = s9.shapes.add_table(7, 5, Inches(0.8), Inches(1.3), Inches(6.5), Inches(3.0)).table
    s9_data = [
        ("course.name", "Text Input", "VARCHAR(100)", "YES", "Degree name: 'Master of Computer Applications'"),
        ("course.code", "Text Input", "VARCHAR(20)", "YES", "Unique uppercase course code: 'MCA'"),
        ("batch.name", "Text Input", "VARCHAR(50)", "YES", "Cohort label: 'MCA 2024-2026'"),
        ("batch.year", "Number Box", "INT(11)", "YES", "Graduation calendar year (e.g. 2026)"),
        ("subject.name", "Text Input", "VARCHAR(100)", "YES", "Curriculum course title (e.g. 'Compiler Design')"),
        ("subject.faculty_id", "Dropdown", "INT(11)", "YES", "Foreign key linking assigned teacher (scas_users.id)")
    ]
    style_spec_table(t_s9, [Inches(1.5), Inches(1.1), Inches(1.0), Inches(0.5), Inches(2.4)], HEADERS_SPEC, s9_data, NAVY_PRIMARY, TEXT_LIGHT, ROW_ALT, CARD_BG, NAVY_PRIMARY, FK_COLOR, RED_ACCENT, GREEN_ACCENT, TEXT_DARK)

    c_sec9 = create_card(s9, Inches(0.8), Inches(4.5), Inches(6.5), Inches(2.4), BLUE_LIGHT, BLUE_ACCENT)
    tf_s9 = c_sec9.text_frame
    tf_s9.margin_left = tf_s9.margin_right = tf_s9.margin_top = Inches(0.14)
    ps9_t = tf_s9.paragraphs[0]
    ps9_t.text = "🏛️ RELATIONAL CURRICULUM CONSTRAINTS"
    ps9_t.font.size = Pt(11)
    ps9_t.font.bold = True
    ps9_t.font.color.rgb = NAVY_PRIMARY

    sec9_notes = [
        ("Hierarchical 1:N Cascades: ", "Course ➔ Batches ➔ Students. Subject ➔ Attendance, Marks, Schedules."),
        ("Faculty Isolation: ", "Assigning faculty_id in scas_subjects enforces RBAC boundary so faculty only evaluate their subjects.")
    ]
    for h, b in sec9_notes:
        p = tf_s9.add_paragraph()
        p.space_before = Pt(4)
        add_run(p, "• " + h, bold=True, color=NAVY_PRIMARY, size=Pt(8.8))
        add_run(p, b, color=TEXT_DARK, size=Pt(8.6))

    s9_fields = [
        ("Course / Degree Program", "Master of Computer Applications (MCA)", "select"),
        ("Academic Batch Cohort", "MCA 2024-2026 (Passing 2026)", "select"),
        ("Subject Title & Code", "Theory of Computation (MCA-104)", "text"),
        ("Assigned Faculty Member", "Dr. CD Patel (cdpatel@college.edu)", "select")
    ]
    draw_input_wireframe(s9, Inches(7.6), Inches(1.3), Inches(4.9), Inches(5.6), "Curriculum & Faculty Allocation", s9_fields, "Save Academic Structure", "ROLE: ADMINISTRATOR", NAVY_PRIMARY, BLUE_ACCENT, BORDER_LIGHT)

    # =========================================================================
    # SLIDE 10: Input Design 7 — Faculty Daily Attendance Register
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Input Design 7: Faculty Daily Class Attendance Register", "ATTENDANCE REGISTER ENGINE (FACULTY)")

    t_s10 = s10.shapes.add_table(5, 5, Inches(0.8), Inches(1.3), Inches(6.5), Inches(2.6)).table
    s10_data = [
        ("subject_id", "Dropdown", "INT(11)", "YES", "Faculty assigned subject selector"),
        ("batch_id", "Dropdown", "INT(11)", "YES", "Target academic cohort"),
        ("date", "Date Picker", "DATE", "YES", "Lecture session date (defaults to today)"),
        ("status[student_id]", "Toggle Switches", "VARCHAR(10)", "YES", "Radio/switch: 'Present' or 'Absent' per student")
    ]
    style_spec_table(t_s10, [Inches(1.5), Inches(1.1), Inches(1.0), Inches(0.5), Inches(2.4)], HEADERS_SPEC, s10_data, NAVY_PRIMARY, TEXT_LIGHT, ROW_ALT, CARD_BG, NAVY_PRIMARY, FK_COLOR, RED_ACCENT, GREEN_ACCENT, TEXT_DARK)

    c_sec10 = create_card(s10, Inches(0.8), Inches(4.1), Inches(6.5), Inches(2.8), BLUE_LIGHT, BLUE_ACCENT)
    tf_s10 = c_sec10.text_frame
    tf_s10.margin_left = tf_s10.margin_right = tf_s10.margin_top = Inches(0.16)
    ps10_t = tf_s10.paragraphs[0]
    ps10_t.text = "⚡ ERGONOMIC ATTENDANCE DISPATCH"
    ps10_t.font.size = Pt(11)
    ps10_t.font.bold = True
    ps10_t.font.color.rgb = NAVY_PRIMARY

    sec10_notes = [
        ("Bulk 'Mark All Present' Switch: ", "One-click toggle presets all enrolled students to 'Present'; faculty only marks absentees."),
        ("Duplicate Safeguard: ", "Composite unique check (student_id, subject_id, date) prevents accidental double-submission."),
        ("Live Metric Re-calculation: ", "Submitting attendance immediately refreshes student attendance percentages and AI risk scores.")
    ]
    for h, b in sec10_notes:
        p = tf_s10.add_paragraph()
        p.space_before = Pt(6)
        add_run(p, "• " + h, bold=True, color=NAVY_PRIMARY, size=Pt(8.8))
        add_run(p, b, color=TEXT_DARK, size=Pt(8.6))

    s10_fields = [
        ("Select Assigned Subject", "Theory of Computation (MCA-104)", "select"),
        ("Class Attendance Date", "2026-09-29 (Today)", "text"),
        ("Quick Master Action", "☑ Toggle All Present (Fast Mark)", "placeholder"),
        ("Student 1: MCA24004 - Himanshu", "● Present  ○ Absent", "text"),
        ("Student 2: MCA24005 - Jignesh", "● Present  ○ Absent", "text")
    ]
    draw_input_wireframe(s10, Inches(7.6), Inches(1.3), Inches(4.9), Inches(5.6), "Daily Class Attendance Register", s10_fields, "Submit Attendance Sheet", "ROLE: FACULTY", NAVY_PRIMARY, BLUE_ACCENT, BORDER_LIGHT)

    # =========================================================================
    # SLIDE 11: Input Design 8 — Continuous Internal Evaluation (CIE) Marks
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Input Design 8: Continuous Internal Evaluation (CIE) Marks", "EXAMINATION & EVALUATION (FACULTY)")

    t_s11 = s11.shapes.add_table(6, 5, Inches(0.8), Inches(1.3), Inches(6.5), Inches(2.8)).table
    s11_data = [
        ("subject_id", "Dropdown", "INT(11)", "YES", "Assigned subject selector"),
        ("exam_type", "Dropdown / Tabs", "VARCHAR(30)", "YES", "'Midterm 1', 'Midterm 2', 'Assignment', 'Final'"),
        ("max_marks", "Numeric Input", "FLOAT", "YES", "Benchmark total (30 for Midterm, 20 for Assign)"),
        ("marks_obtained", "Numeric Grid", "FLOAT", "YES", "Numeric score achieved per student"),
        ("student_id", "Hidden Input", "INT(11)", "YES", "Foreign key linking student profile")
    ]
    style_spec_table(t_s11, [Inches(1.5), Inches(1.1), Inches(1.0), Inches(0.5), Inches(2.4)], HEADERS_SPEC, s11_data, NAVY_PRIMARY, TEXT_LIGHT, ROW_ALT, CARD_BG, NAVY_PRIMARY, FK_COLOR, RED_ACCENT, GREEN_ACCENT, TEXT_DARK)

    c_sec11 = create_card(s11, Inches(0.8), Inches(4.3), Inches(6.5), Inches(2.6), BLUE_LIGHT, BLUE_ACCENT)
    tf_s11 = c_sec11.text_frame
    tf_s11.margin_left = tf_s11.margin_right = tf_s11.margin_top = Inches(0.14)
    ps11_t = tf_s11.paragraphs[0]
    ps11_t.text = "📈 MATHEMATICAL RANGE VALIDATION"
    ps11_t.font.size = Pt(11)
    ps11_t.font.bold = True
    ps11_t.font.color.rgb = NAVY_PRIMARY

    sec11_notes = [
        ("Boundary Integrity: ", "JavaScript and SQLAlchemy constraints enforce 0.0 <= marks_obtained <= max_marks."),
        ("Live Class Statistics: ", "Real-time client calculations compute class average, highest score, and passing % as marks are typed.")
    ]
    for h, b in sec11_notes:
        p = tf_s11.add_paragraph()
        p.space_before = Pt(4)
        add_run(p, "• " + h, bold=True, color=NAVY_PRIMARY, size=Pt(8.8))
        add_run(p, b, color=TEXT_DARK, size=Pt(8.6))

    s11_fields = [
        ("Assigned Subject", "Compiler Design (MCA-105)", "select"),
        ("Assessment Type", "Midterm Examination 1", "select"),
        ("Maximum Benchmark Marks", "30.0 Points", "text"),
        ("MCA24004 - Himanshu Goswami", "Score: 26.0 / 30.0  (86.6%)", "text"),
        ("MCA24005 - Jignesh Sathavara", "Score: 28.0 / 30.0  (93.3%)", "text")
    ]
    draw_input_wireframe(s11, Inches(7.6), Inches(1.3), Inches(4.9), Inches(5.6), "Marks & CIE Evaluation Entry", s11_fields, "Save & Lock Marks", "ROLE: FACULTY", NAVY_PRIMARY, BLUE_ACCENT, BORDER_LIGHT)

    # =========================================================================
    # SLIDE 12: Input Design 9 — Lecture Timetable & Room Allocation
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Input Design 9: Weekly Lecture Timetable & Room Allocation", "SCHEDULING & RESOURCE ALLOCATION (FACULTY/ADMIN)")

    t_s12 = s12.shapes.add_table(6, 5, Inches(0.8), Inches(1.3), Inches(6.5), Inches(2.8)).table
    s12_data = [
        ("subject_id", "Dropdown", "INT(11)", "YES", "Subject to be scheduled"),
        ("batch_id", "Dropdown", "INT(11)", "YES", "Cohort batch receiving the lecture"),
        ("day_of_week", "Dropdown", "VARCHAR(20)", "YES", "Day: 'Monday', 'Tuesday', ..., 'Friday'"),
        ("start_time / end_time", "Time Picker", "VARCHAR(10)", "YES", "Slot interval (e.g. '09:00 AM' to '10:30 AM')"),
        ("room", "Text Input", "VARCHAR(20)", "YES", "Classroom or lab (e.g. 'Lab 3', 'Room 204')")
    ]
    style_spec_table(t_s12, [Inches(1.5), Inches(1.1), Inches(1.0), Inches(0.5), Inches(2.4)], HEADERS_SPEC, s12_data, NAVY_PRIMARY, TEXT_LIGHT, ROW_ALT, CARD_BG, NAVY_PRIMARY, FK_COLOR, RED_ACCENT, GREEN_ACCENT, TEXT_DARK)

    c_sec12 = create_card(s12, Inches(0.8), Inches(4.3), Inches(6.5), Inches(2.6), BLUE_LIGHT, BLUE_ACCENT)
    tf_s12 = c_sec12.text_frame
    tf_s12.margin_left = tf_s12.margin_right = tf_s12.margin_top = Inches(0.14)
    ps12_t = tf_s12.paragraphs[0]
    ps12_t.text = "🗓️ CONFLICT DETECTION ENGINE"
    ps12_t.font.size = Pt(11)
    ps12_t.font.bold = True
    ps12_t.font.color.rgb = NAVY_PRIMARY

    sec12_notes = [
        ("Classroom Collision Prevention: ", "Prevents scheduling two lectures in the same room at the same day and time interval."),
        ("Faculty Dual-Booking Guard: ", "Validates that assigned faculty is not already booked for another subject during that slot.")
    ]
    for h, b in sec12_notes:
        p = tf_s12.add_paragraph()
        p.space_before = Pt(4)
        add_run(p, "• " + h, bold=True, color=NAVY_PRIMARY, size=Pt(8.8))
        add_run(p, b, color=TEXT_DARK, size=Pt(8.6))

    s12_fields = [
        ("Curriculum Subject", "Theory of Computation (MCA-104)", "select"),
        ("Target Batch", "MCA 2024-2026", "select"),
        ("Lecture Day", "Monday", "select"),
        ("Time Window", "09:00 AM – 10:30 AM", "text"),
        ("Classroom / Lab Venue", "Advanced Computing Lab 3", "text")
    ]
    draw_input_wireframe(s12, Inches(7.6), Inches(1.3), Inches(4.9), Inches(5.6), "Class Timetable Slot Setup", s12_fields, "Add Schedule Slot", "ROLE: FACULTY / ADMIN", NAVY_PRIMARY, BLUE_ACCENT, BORDER_LIGHT)

    # =========================================================================
    # SLIDE 13: Input Design 10 — Student Fee Payment Gateway
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Input Design 10: Student Online Fee Payment Gateway", "FINANCIAL TRANSACTION GATEWAY (STUDENT)")

    t_s13 = s13.shapes.add_table(6, 5, Inches(0.8), Inches(1.3), Inches(6.5), Inches(2.8)).table
    s13_data = [
        ("student_id", "Read-Only / Token", "INT(11)", "YES", "Authenticated student identity"),
        ("amount", "Read-Only / Currency", "FLOAT", "YES", "Outstanding semester fee balance (₹65,000)"),
        ("payment_mode", "Radio / Tabs", "VARCHAR(20)", "YES", "'UPI QR', 'Credit/Debit Card', 'Net Banking'"),
        ("card_or_upi_id", "Masked Input", "VARCHAR(50)", "YES", "Banking reference / card details"),
        ("transaction_id", "Generated / Ext", "VARCHAR(50)", "YES", "Unique transaction reference (TXN-984712-SUCCESS)")
    ]
    style_spec_table(t_s13, [Inches(1.5), Inches(1.1), Inches(1.0), Inches(0.5), Inches(2.4)], HEADERS_SPEC, s13_data, NAVY_PRIMARY, TEXT_LIGHT, ROW_ALT, CARD_BG, NAVY_PRIMARY, FK_COLOR, RED_ACCENT, GREEN_ACCENT, TEXT_DARK)

    c_sec13 = create_card(s13, Inches(0.8), Inches(4.3), Inches(6.5), Inches(2.6), BLUE_LIGHT, BLUE_ACCENT)
    tf_s13 = c_sec13.text_frame
    tf_s13.margin_left = tf_s13.margin_right = tf_s13.margin_top = Inches(0.14)
    ps13_t = tf_s13.paragraphs[0]
    ps13_t.text = "💳 AUDIT TRAILS & IDEMPOTENCY"
    ps13_t.font.size = Pt(11)
    ps13_t.font.bold = True
    ps13_t.font.color.rgb = NAVY_PRIMARY

    sec13_notes = [
        ("Idempotent Transactions: ", "Unique constraints on receipt_no and transaction_id prevent duplicate fee deduction."),
        ("Instant Clearance: ", "Successful payment updates status='Paid', generates receipt, and clears hall ticket dues immediately.")
    ]
    for h, b in sec13_notes:
        p = tf_s13.add_paragraph()
        p.space_before = Pt(4)
        add_run(p, "• " + h, bold=True, color=NAVY_PRIMARY, size=Pt(8.8))
        add_run(p, b, color=TEXT_DARK, size=Pt(8.6))

    s13_fields = [
        ("Student Identity", "MCA24005 – Jignesh Sathavara", "text"),
        ("Fee Invoice Breakdown", "Semester 1 Tuition & Lab Dues", "text"),
        ("Total Amount Payable", "₹ 65,000.00 INR", "text"),
        ("Payment Gateway Channel", "Instant UPI / NetBanking / Debit Card", "select"),
        ("Card Number / UPI Handle", "4532 •••• •••• 8821  |  12/28", "text")
    ]
    draw_input_wireframe(s13, Inches(7.6), Inches(1.3), Inches(4.9), Inches(5.6), "Secure Fee Payment Gateway", s13_fields, "Pay ₹65,000 & Get Receipt", "ROLE: STUDENT", NAVY_PRIMARY, BLUE_ACCENT, BORDER_LIGHT)

    # =========================================================================
    # SLIDE 14: Input Design 11 — Institutional Leave Application
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Input Design 11: Institutional Leave Application Submission", "LEAVE APPLICATION WORKFLOW (STUDENT / FACULTY)")

    t_s14 = s14.shapes.add_table(6, 5, Inches(0.8), Inches(1.3), Inches(6.5), Inches(2.8)).table
    s14_data = [
        ("user_id", "Session Binding", "INT(11)", "YES", "Authenticated applicant (scas_users.id)"),
        ("leave_type", "Dropdown", "VARCHAR(50)", "YES", "'Sick Leave', 'Casual Leave', 'Duty Leave'"),
        ("start_date", "Date Picker", "DATE", "YES", "First day of proposed absence"),
        ("end_date", "Date Picker", "DATE", "YES", "Final day of absence (start_date <= end_date)"),
        ("reason", "Textarea", "TEXT", "YES", "Detailed written explanation & doctor note")
    ]
    style_spec_table(t_s14, [Inches(1.5), Inches(1.1), Inches(1.0), Inches(0.5), Inches(2.4)], HEADERS_SPEC, s14_data, NAVY_PRIMARY, TEXT_LIGHT, ROW_ALT, CARD_BG, NAVY_PRIMARY, FK_COLOR, RED_ACCENT, GREEN_ACCENT, TEXT_DARK)

    c_sec14 = create_card(s14, Inches(0.8), Inches(4.3), Inches(6.5), Inches(2.6), BLUE_LIGHT, BLUE_ACCENT)
    tf_s14 = c_sec14.text_frame
    tf_s14.margin_left = tf_s14.margin_right = tf_s14.margin_top = Inches(0.14)
    ps14_t = tf_s14.paragraphs[0]
    ps14_t.text = "📋 APPROVAL WORKFLOW INTEGRATION"
    ps14_t.font.size = Pt(11)
    ps14_t.font.bold = True
    ps14_t.font.color.rgb = NAVY_PRIMARY

    sec14_notes = [
        ("Chronological Validation: ", "Prevents start_date in past or end_date < start_date; calculates total calendar days."),
        ("Duty Leave Waiver Credit: ", "Approved 'Duty Leave' automatically flags attendance waivers in student compliance records.")
    ]
    for h, b in sec14_notes:
        p = tf_s14.add_paragraph()
        p.space_before = Pt(4)
        add_run(p, "• " + h, bold=True, color=NAVY_PRIMARY, size=Pt(8.8))
        add_run(p, b, color=TEXT_DARK, size=Pt(8.6))

    s14_fields = [
        ("Leave Category", "Sick Leave (Medical Certificate Attached)", "select"),
        ("Absence Start Date", "2026-10-02 (Friday)", "text"),
        ("Absence End Date", "2026-10-04 (Sunday)", "text"),
        ("Detailed Justification", "Medical appointment and dental procedure.", "text"),
        ("Workflow Reviewer", "Assigned: Dean System Administrator", "placeholder")
    ]
    draw_input_wireframe(s14, Inches(7.6), Inches(1.3), Inches(4.9), Inches(5.6), "Leave Application Portal", s14_fields, "Submit for Approval", "ROLE: ALL APPLICANTS", NAVY_PRIMARY, BLUE_ACCENT, BORDER_LIGHT)

    # =========================================================================
    # SLIDE 15: Input Design 12 — Continuous Diagnostic Unit Assessment
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Input Design 12: Continuous Diagnostic Unit Assessment Engine", "DIAGNOSTIC TEST ENGINE (STUDENT)")

    t_s15 = s15.shapes.add_table(6, 5, Inches(0.8), Inches(1.3), Inches(6.5), Inches(2.8)).table
    s15_data = [
        ("unit_number", "Dropdown / Tabs", "INT(11)", "YES", "Target unit sequence (Unit 1 to Unit 5)"),
        ("test_type", "Radio", "VARCHAR(20)", "YES", "Diagnostic mode: 'pre-test' or 'post-test'"),
        ("total_questions", "Hidden Constant", "INT(11)", "YES", "Standardized 25 multiple-choice questions"),
        ("selected_options", "Radio Array", "VARCHAR(1)", "YES", "Radio choice per item ('A', 'B', 'C', 'D')"),
        ("submitted_at", "System Timestamp", "DATETIME", "YES", "Telemetry timestamp for speed & placement")
    ]
    style_spec_table(t_s15, [Inches(1.5), Inches(1.1), Inches(1.0), Inches(0.5), Inches(2.4)], HEADERS_SPEC, s15_data, NAVY_PRIMARY, TEXT_LIGHT, ROW_ALT, CARD_BG, NAVY_PRIMARY, FK_COLOR, RED_ACCENT, GREEN_ACCENT, TEXT_DARK)

    c_sec15 = create_card(s15, Inches(0.8), Inches(4.3), Inches(6.5), Inches(2.6), BLUE_LIGHT, BLUE_ACCENT)
    tf_s15 = c_sec15.text_frame
    tf_s15.margin_left = tf_s15.margin_right = tf_s15.margin_top = Inches(0.14)
    ps15_t = tf_s15.paragraphs[0]
    ps15_t.text = "🎯 REAL-TIME MASTERY SCORING"
    ps15_t.font.size = Pt(11)
    ps15_t.font.bold = True
    ps15_t.font.color.rgb = NAVY_PRIMARY

    sec15_notes = [
        ("Automated Grading: ", "Calculates score, percentage = (score / 25) * 100, and categorizes mastery level immediately."),
        ("Growth Delta Analysis: ", "Compares pre-test vs post-test score differential to measure learning velocity per chapter.")
    ]
    for h, b in sec15_notes:
        p = tf_s15.add_paragraph()
        p.space_before = Pt(4)
        add_run(p, "• " + h, bold=True, color=NAVY_PRIMARY, size=Pt(8.8))
        add_run(p, b, color=TEXT_DARK, size=Pt(8.6))

    s15_fields = [
        ("Diagnostic Curriculum Unit", "Unit 2: Lexical Analysis & Finite Automata", "select"),
        ("Assessment Mode", "● Post-Test Diagnostic   ○ Pre-Test Diagnostic", "text"),
        ("Question 1 of 25", "What is the primary function of a lexical analyzer?", "text"),
        ("Options", "○ Syntax Tree  ● Token Stream  ○ Parsing  ○ Code Gen", "placeholder"),
        ("Time Remaining", "⏱ 18 minutes 42 seconds left", "placeholder")
    ]
    draw_input_wireframe(s15, Inches(7.6), Inches(1.3), Inches(4.9), Inches(5.6), "Online Unit Diagnostic Exam", s15_fields, "Submit Diagnostic Test", "ROLE: STUDENT", NAVY_PRIMARY, BLUE_ACCENT, BORDER_LIGHT)

    # =========================================================================
    # SLIDE 16: Output Architecture & Reporting Framework
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "Standardized Output Architecture & Reporting Taxonomy", "OUTPUT TAXONOMY & DELIVERY CHANNELS")

    # 4 Output Tier Cards
    tiers = [
        ("📊 1. Real-Time Interactive Dashboards", 
         "• Role-specific views for Admin, Faculty, and Students.\n• High-impact KPI tiles, dynamic donut enrollment charts, and live activity streams.\n• Instant reactivity on attendance or marks updates.",
         Inches(0.8), Inches(1.3)),
        ("🤖 2. Predictive AI Analytics Displays", 
         "• Automated student academic risk classification (High, Medium, Low).\n• 45% Attendance + 55% Midterm weighted decision heuristics.\n• Actionable intervention alerts to prevent course dropouts.",
         Inches(6.9), Inches(1.3)),
        ("📄 3. Official Printable Documents", 
         "• Semester Grade Sheets / Official Transcripts with SGPA/CGPA calculations.\n• Official Fee Payment Receipt Vouchers with banking transaction IDs and stamps.\n• Print-optimized CSS (@media print) with formal typography.",
         Inches(0.8), Inches(4.2)),
        ("📧 4. Automated Transactional Emails", 
         "• Account Welcome & Credential Dispatch (Single/Bulk).\n• Cryptographic Password Reset Links (1-hour expiry).\n• Low Attendance Compliance Defaulter Notices sent directly to students & guardians.",
         Inches(6.9), Inches(4.2))
    ]

    for title, body, left, top in tiers:
        card = create_card(s16, left, top, Inches(5.6), Inches(2.7), CARD_BG, BORDER_LIGHT)
        tf = card.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = NAVY_PRIMARY
        
        for line in body.split("\n"):
            pl = tf.add_paragraph()
            pl.space_before = Pt(4)
            pl.text = line
            pl.font.size = Pt(8.8)
            pl.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 17: Output Design 1 — Executive Administrator Analytics Dashboard
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "Output Design 1: Executive Administrator Analytics Dashboard", "EXECUTIVE KPI MONITORING (ADMIN)")

    # Left: Output Specs
    t_s17 = s17.shapes.add_table(6, 4, Inches(0.8), Inches(1.3), Inches(6.0), Inches(2.6)).table
    s17_headers = ["Output Component", "Metric / Display Type", "Source DB Tables", "Business Utility"]
    s17_data = [
        ("Total Students KPI", "Live Count Badge", "scas_student_profiles", "Institutional enrollment tracking"),
        ("Faculty Count KPI", "Live Count Badge", "scas_faculty_profiles", "Staffing & faculty ratio analysis"),
        ("Course Revenue KPI", "Currency Stat (₹)", "scas_fee_payments", "Financial collection monitoring"),
        ("Program Donut Chart", "Visual Chart (Chart.js)", "scas_courses, batches", "Cohort distribution across degrees"),
        ("System Audit Stream", "Timestamped Feed", "scas_users, leaves, pay", "Compliance auditing & activity logs")
    ]
    style_spec_table(t_s17, [Inches(1.6), Inches(1.3), Inches(1.3), Inches(1.8)], s17_headers, s17_data, NAVY_PRIMARY, TEXT_LIGHT, ROW_ALT, CARD_BG, NAVY_PRIMARY, FK_COLOR, RED_ACCENT, GREEN_ACCENT, TEXT_DARK)

    c_s17 = create_card(s17, Inches(0.8), Inches(4.1), Inches(6.0), Inches(2.8), BLUE_LIGHT, BLUE_ACCENT)
    tf_s17 = c_s17.text_frame
    tf_s17.margin_left = tf_s17.margin_right = tf_s17.margin_top = Inches(0.16)
    p_s17_t = tf_s17.paragraphs[0]
    p_s17_t.text = "📊 EXECUTIVE DECISION HIGHLIGHTS"
    p_s17_t.font.size = Pt(11)
    p_s17_t.font.bold = True
    p_s17_t.font.color.rgb = NAVY_PRIMARY

    s17_notes = [
        ("Single-Pane Governance: ", "Dean administrators view high-level institutional health across academics, finance, and attendance in real time."),
        ("One-Click Batch Dispatch: ", "Executive action buttons enable single-click credential dispatch to all newly admitted students."),
        ("Financial Clearance Visibility: ", "Instantly isolates pending dues from collected fees to support fiscal planning.")
    ]
    for h, b in s17_notes:
        p = tf_s17.add_paragraph()
        p.space_before = Pt(6)
        add_run(p, "• " + h, bold=True, color=NAVY_PRIMARY, size=Pt(8.8))
        add_run(p, b, color=TEXT_DARK, size=Pt(8.6))

    # Right: Dashboard Mockup Card
    d_card = create_card(s17, Inches(7.1), Inches(1.3), Inches(5.4), Inches(5.6), CARD_BG, BORDER_LIGHT, Pt(1.5))
    draw_window_bar(s17, Inches(7.1), Inches(1.3), Inches(5.4), "Admin Analytics Portal – Executive View", NAVY_PRIMARY)

    # 4 Stat Cards
    kpis = [
        ("TOTAL STUDENTS", "60 Enrolled", GREEN_ACCENT),
        ("FACULTY MEMBERS", "12 Active", BLUE_ACCENT),
        ("FEE REVENUE", "₹ 7,80,000", PURPLE_ACCENT),
        ("PENDING DUES", "₹ 1,30,000", RED_ACCENT)
    ]
    for idx, (label, val, col) in enumerate(kpis):
        kx = Inches(7.3 + (idx % 2) * 2.5)
        ky = Inches(1.8 + (idx // 2) * 0.9)
        kc = create_card(s17, kx, ky, Inches(2.3), Inches(0.75), ROW_ALT, col, Pt(1.2))
        ktf = kc.text_frame
        ktf.margin_left = ktf.margin_top = ktf.margin_right = ktf.margin_bottom = Inches(0.08)
        kp_l = ktf.paragraphs[0]
        kp_l.text = label
        kp_l.font.size = Pt(7.0)
        kp_l.font.bold = True
        kp_l.font.color.rgb = TEXT_MUTED
        kp_v = ktf.add_paragraph()
        kp_v.text = val
        kp_v.font.size = Pt(11)
        kp_v.font.bold = True
        kp_v.font.color.rgb = col

    # Chart Mockup Box
    ch_box = create_card(s17, Inches(7.3), Inches(3.7), Inches(5.0), Inches(1.4), BLUE_LIGHT, BLUE_ACCENT)
    ctf = ch_box.text_frame
    ctf.margin_left = ctf.margin_top = Inches(0.1)
    cp1 = ctf.paragraphs[0]
    cp1.text = "📈 PROGRAM ENROLLMENT BREAKDOWN"
    cp1.font.size = Pt(8.5)
    cp1.font.bold = True
    cp1.font.color.rgb = NAVY_PRIMARY
    cp2 = ctf.add_paragraph()
    cp2.space_before = Pt(4)
    cp2.text = "■ MCA (Postgrad): 65%   ■ BCA: 25%   ■ M.Tech: 10%"
    cp2.font.size = Pt(8.0)
    cp2.font.color.rgb = TEXT_DARK

    # Recent Activity Feed
    act_box = create_card(s17, Inches(7.3), Inches(5.2), Inches(5.0), Inches(1.5), ROW_ALT, BORDER_LIGHT)
    atf = act_box.text_frame
    atf.margin_left = atf.margin_top = Inches(0.1)
    ap1 = atf.paragraphs[0]
    ap1.text = "🕒 RECENT SYSTEM ACTIVITY FEED"
    ap1.font.size = Pt(8.5)
    ap1.font.bold = True
    ap1.font.color.rgb = NAVY_PRIMARY

    acts = [
        "• Fee Payment of ₹65,000 confirmed for MCA24005 (TXN-984712)",
        "• Daily Attendance recorded for MCA-104 (58 Present, 2 Absent)",
        "• Sick Leave Application submitted by Himanshu Goswami"
    ]
    for act in acts:
        p = atf.add_paragraph()
        p.space_before = Pt(2)
        p.text = act
        p.font.size = Pt(7.5)
        p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 18: Output Design 2 — Faculty Academic Dashboard & AI Risk Alerts
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    add_header(s18, "Output Design 2: Faculty Dashboard & AI Student Dropout Risk Alerts", "PREDICTIVE ACADEMIC ANALYTICS (FACULTY)")

    # Left: Risk Model Specification
    t_s18 = s18.shapes.add_table(4, 4, Inches(0.8), Inches(1.3), Inches(6.0), Inches(2.2)).table
    s18_headers = ["Risk Tier", "Score Range", "Visual Badge", "Required Intervention Strategy"]
    s18_data = [
        ("High Academic Risk", "Score >= 65", "🔴 RED BADGE", "Urgent 1-on-1 counseling & guardian email alert"),
        ("Medium Academic Risk", "40 <= Score < 65", "🟡 YELLOW BADGE", "Remedial assignment & tutorial class scheduling"),
        ("Low Academic Risk", "Score < 40", "🟢 GREEN BADGE", "Normal academic progression & peer mentorship")
    ]
    style_spec_table(t_s18, [Inches(1.5), Inches(1.0), Inches(1.2), Inches(2.3)], s18_headers, s18_data, NAVY_PRIMARY, TEXT_LIGHT, ROW_ALT, CARD_BG, NAVY_PRIMARY, FK_COLOR, RED_ACCENT, GREEN_ACCENT, TEXT_DARK)

    # Heuristic Formula Box
    c_s18 = create_card(s18, Inches(0.8), Inches(3.7), Inches(6.0), Inches(3.2), BLUE_LIGHT, BLUE_ACCENT)
    tf_s18 = c_s18.text_frame
    tf_s18.margin_left = tf_s18.margin_right = tf_s18.margin_top = Inches(0.16)
    p_fml = tf_s18.paragraphs[0]
    p_fml.text = "🤖 PREDICTIVE AI DECISION HEURISTIC FORMULA"
    p_fml.font.size = Pt(11)
    p_fml.font.bold = True
    p_fml.font.color.rgb = NAVY_PRIMARY

    p_eq = tf_s18.add_paragraph()
    p_eq.space_before = Pt(6)
    add_run(p_eq, "Risk_Score = [ 0.45 × (100 - Attendance_%) ] + [ 0.55 × (100 - Midterm_% ) ]", bold=True, color=RGBColor(67, 56, 202), size=Pt(9.0), font_name='Consolas')

    fml_notes = [
        ("45% Attendance Weighting: ", "Reflects classroom engagement and regulatory exam eligibility (< 75% triggers penalty)."),
        ("55% Academic Score Weighting: ", "Measures conceptual mastery across Midterm 1 & Midterm 2 evaluations."),
        ("Proactive Prevention: ", "Identifies vulnerable students at week 4 before end-semester exam failure occurs.")
    ]
    for h, b in fml_notes:
        p = tf_s18.add_paragraph()
        p.space_before = Pt(4)
        add_run(p, "• " + h, bold=True, color=NAVY_PRIMARY, size=Pt(8.8))
        add_run(p, b, color=TEXT_DARK, size=Pt(8.6))

    # Right: Wireframe Mockup of Risk Alert Cards
    f_card = create_card(s18, Inches(7.1), Inches(1.3), Inches(5.4), Inches(5.6), CARD_BG, BORDER_LIGHT, Pt(1.5))
    draw_window_bar(s18, Inches(7.1), Inches(1.3), Inches(5.4), "Faculty Portal – AI Academic Risk Monitor", NAVY_PRIMARY)

    # Assigned Subjects Bar
    sub_bar = create_card(s18, Inches(7.3), Inches(1.8), Inches(5.0), Inches(0.5), ROW_ALT, BLUE_ACCENT)
    sbtf = sub_bar.text_frame
    sbtf.margin_left = sbtf.margin_top = Inches(0.08)
    sp = sbtf.paragraphs[0]
    sp.text = "📚 Assigned: MCA-104 Theory of Computation | Batch: MCA 2024-2026"
    sp.font.size = Pt(8.0)
    sp.font.bold = True
    sp.font.color.rgb = NAVY_PRIMARY

    # Risk Warning Alert Cards
    alert1 = create_card(s18, Inches(7.3), Inches(2.4), Inches(5.0), Inches(1.4), RED_LIGHT, RED_ACCENT, Pt(1.2))
    atf1 = alert1.text_frame
    atf1.margin_left = atf1.margin_top = Inches(0.1)
    ap1 = atf1.paragraphs[0]
    ap1.text = "🔴 HIGH DROPOUT RISK: Roll No MCA24004 (Himanshu)"
    ap1.font.size = Pt(9.0)
    ap1.font.bold = True
    ap1.font.color.rgb = RED_ACCENT
    ap1_sub = atf1.add_paragraph()
    ap1_sub.space_before = Pt(3)
    ap1_sub.text = "• Attendance: 62.5% (Below 75% Statutory Limit) | Midterm: 58.0%\n• Computed Risk Score: 68.4 / 100\n• Action Recommended: Send Formal Guardian Alert & Schedule Remedial Lab"
    ap1_sub.font.size = Pt(7.8)
    ap1_sub.font.color.rgb = TEXT_DARK

    alert2 = create_card(s18, Inches(7.3), Inches(3.9), Inches(5.0), Inches(1.3), GREEN_LIGHT, GREEN_ACCENT, Pt(1.2))
    atf2 = alert2.text_frame
    atf2.margin_left = atf2.margin_top = Inches(0.1)
    ap2 = atf2.paragraphs[0]
    ap2.text = "🟢 LOW RISK (ON TRACK): Roll No MCA24005 (Jignesh)"
    ap2.font.size = Pt(9.0)
    ap2.font.bold = True
    ap2.font.color.rgb = GREEN_ACCENT
    ap2_sub = atf2.add_paragraph()
    ap2_sub.space_before = Pt(3)
    ap2_sub.text = "• Attendance: 93.3% (Compliant) | Midterm: 91.5%\n• Computed Risk Score: 18.2 / 100\n• Academic Status: Eligible for Advanced Research / Merit Honor"
    ap2_sub.font.size = Pt(7.8)
    ap2_sub.font.color.rgb = TEXT_DARK

    # Quick Action Buttons
    act_btn = create_card(s18, Inches(7.3), Inches(5.4), Inches(5.0), Inches(0.4), BLUE_ACCENT)
    abtf = act_btn.text_frame
    abp = abtf.paragraphs[0]
    abp.text = "Export Defaulters Roster & Email Guardian Warnings"
    abp.font.size = Pt(8.5)
    abp.font.bold = True
    abp.font.color.rgb = RGBColor(255, 255, 255)
    abp.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 19: Output Design 3 — Student Academic Portal Dashboard
    # =========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    add_header(s19, "Output Design 3: Student Academic Portal Dashboard", "STUDENT ACADEMIC EXPERIENCE (STUDENT)")

    t_s19 = s19.shapes.add_table(5, 4, Inches(0.8), Inches(1.3), Inches(6.0), Inches(2.4)).table
    s19_headers = ["Dashboard Element", "Display Format", "Data Source", "Student Objective"]
    s19_data = [
        ("Attendance Progress Gauge", "Radial Dial (75% goal)", "scas_attendance", "Track exam eligibility threshold"),
        ("Cumulative GPA (CGPA)", "Numerical Badge (8.8/10)", "scas_results", "View cumulative academic standing"),
        ("Today's Timetable Card", "Class Schedule Grid", "scas_schedules", "Locate daily lectures & room numbers"),
        ("Fee Clearance Alert", "Status Ribbon (Paid)", "scas_fee_payments", "Verify hall ticket financial release")
    ]
    style_spec_table(t_s19, [Inches(1.6), Inches(1.3), Inches(1.3), Inches(1.8)], s19_headers, s19_data, NAVY_PRIMARY, TEXT_LIGHT, ROW_ALT, CARD_BG, NAVY_PRIMARY, FK_COLOR, RED_ACCENT, GREEN_ACCENT, TEXT_DARK)

    c_s19 = create_card(s19, Inches(0.8), Inches(3.9), Inches(6.0), Inches(3.0), BLUE_LIGHT, BLUE_ACCENT)
    tf_s19 = c_s19.text_frame
    tf_s19.margin_left = tf_s19.margin_right = tf_s19.margin_top = Inches(0.16)
    ps19_t = tf_s19.paragraphs[0]
    ps19_t.text = "📱 STUDENT SELF-SERVICE EMPOWERMENT"
    ps19_t.font.size = Pt(11)
    ps19_t.font.bold = True
    ps19_t.font.color.rgb = NAVY_PRIMARY

    s19_notes = [
        ("75% Statutory Compliance Dial: ", "Immediate red color-shift if attendance drops below 75%, notifying student to submit medical leave."),
        ("One-Click Receipt Download: ", "Students download officially stamped PDF fee receipts without visiting the college finance office."),
        ("Semester Scorecard Viewer: ", "Displays official credits, letter grades (O, A+, A), and SGPA calculation instantaneously.")
    ]
    for h, b in s19_notes:
        p = tf_s19.add_paragraph()
        p.space_before = Pt(6)
        add_run(p, "• " + h, bold=True, color=NAVY_PRIMARY, size=Pt(8.8))
        add_run(p, b, color=TEXT_DARK, size=Pt(8.6))

    # Right: Student Dashboard Wireframe
    std_card = create_card(s19, Inches(7.1), Inches(1.3), Inches(5.4), Inches(5.6), CARD_BG, BORDER_LIGHT, Pt(1.5))
    draw_window_bar(s19, Inches(7.1), Inches(1.3), Inches(5.4), "Student Academic Portal – Dashboard", NAVY_PRIMARY)

    # Student Welcome Banner
    wb = create_card(s19, Inches(7.3), Inches(1.8), Inches(5.0), Inches(0.65), BLUE_LIGHT, BLUE_ACCENT)
    wbtf = wb.text_frame
    wbtf.margin_left = wbtf.margin_top = Inches(0.08)
    wp = wbtf.paragraphs[0]
    wp.text = "👋 Welcome back, Jignesh Sathavara (Roll: MCA24005)"
    wp.font.size = Pt(9.0)
    wp.font.bold = True
    wp.font.color.rgb = NAVY_PRIMARY
    wp_sub = wbtf.add_paragraph()
    wp_sub.text = "Master of Computer Applications | Cohort 2024-2026"
    wp_sub.font.size = Pt(7.5)
    wp_sub.font.color.rgb = TEXT_MUTED

    # Attendance & CGPA Dual Cards
    att_card = create_card(s19, Inches(7.3), Inches(2.6), Inches(2.4), Inches(1.4), GREEN_LIGHT, GREEN_ACCENT)
    atf = att_card.text_frame
    atf.margin_left = atf.margin_top = Inches(0.1)
    atp = atf.paragraphs[0]
    atp.text = "ATTENDANCE"
    atp.font.size = Pt(8.0)
    atp.font.bold = True
    atp.font.color.rgb = GREEN_ACCENT
    atp_v = atf.add_paragraph()
    atp_v.text = "93.3 %"
    atp_v.font.size = Pt(18)
    atp_v.font.bold = True
    atp_v.font.color.rgb = GREEN_ACCENT
    atp_s = atf.add_paragraph()
    atp_s.text = "✓ Eligible for Semester Exam"
    atp_s.font.size = Pt(7.0)
    atp_s.font.color.rgb = TEXT_DARK

    gpa_card = create_card(s19, Inches(9.9), Inches(2.6), Inches(2.4), Inches(1.4), BLUE_LIGHT, BLUE_ACCENT)
    gtf = gpa_card.text_frame
    gtf.margin_left = gtf.margin_top = Inches(0.1)
    gtp = gtf.paragraphs[0]
    gtp.text = "CURRENT CGPA"
    gtp.font.size = Pt(8.0)
    gtp.font.bold = True
    gtp.font.color.rgb = BLUE_ACCENT
    gtp_v = gtf.add_paragraph()
    gtp_v.text = "8.80 / 10"
    gtp_v.font.size = Pt(18)
    gtp_v.font.bold = True
    gtp_v.font.color.rgb = BLUE_ACCENT
    gtp_s = gtf.add_paragraph()
    gtp_s.text = "Grade: A+ (First Class with Dist.)"
    gtp_s.font.size = Pt(7.0)
    gtp_s.font.color.rgb = TEXT_DARK

    # Today's Lectures Card
    lec_card = create_card(s19, Inches(7.3), Inches(4.2), Inches(5.0), Inches(1.6), ROW_ALT, BORDER_LIGHT)
    ltf = lec_card.text_frame
    ltf.margin_left = ltf.margin_top = Inches(0.1)
    lp = ltf.paragraphs[0]
    lp.text = "📅 TODAY'S LECTURE TIMETABLE"
    lp.font.size = Pt(8.5)
    lp.font.bold = True
    lp.font.color.rgb = NAVY_PRIMARY

    lecs = [
        "• 09:00 AM – 10:30 AM: Theory of Computation (Lab 3)",
        "• 11:00 AM – 12:30 PM: Compiler Design (Room 204)",
        "• Financial Status: Fee Paid (Receipt #REC-MCA24005-CSV)"
    ]
    for l in lecs:
        p = ltf.add_paragraph()
        p.space_before = Pt(2)
        p.text = l
        p.font.size = Pt(7.8)
        p.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 20: Output Design 4 — Semester Grade Sheet & Official Transcript
    # =========================================================================
    s20 = prs.slides.add_slide(blank_layout)
    add_header(s20, "Output Design 4: Semester Grade Sheet & Official Academic Transcript", "EXAMINATION & TRANSCRIPT ENGINE (EXAM)")

    # Left: Grading Formula Specifications
    t_s20 = s20.shapes.add_table(6, 4, Inches(0.8), Inches(1.3), Inches(6.0), Inches(2.6)).table
    s20_headers = ["Marks Range (%)", "Letter Grade", "Grade Points", "Academic Classification"]
    s20_data = [
        (">= 90.0 %", "Grade 'O'", "10.0 Points", "Outstanding Performance"),
        ("80.0 – 89.9 %", "Grade 'A+'", "9.0 Points", "Excellent Mastery"),
        ("70.0 – 79.9 %", "Grade 'A'", "8.0 Points", "Very Good Standing"),
        ("60.0 – 69.9 %", "Grade 'B+'", "7.0 Points", "Good / Above Average"),
        ("< 50.0 %", "Grade 'F'", "0.0 Points", "Fail / Backlog (Requires Re-exam)")
    ]
    style_spec_table(t_s20, [Inches(1.5), Inches(1.1), Inches(1.2), Inches(2.2)], s20_headers, s20_data, NAVY_PRIMARY, TEXT_LIGHT, ROW_ALT, CARD_BG, NAVY_PRIMARY, FK_COLOR, RED_ACCENT, GREEN_ACCENT, TEXT_DARK)

    # GPA Calculation Formula Box
    c_s20 = create_card(s20, Inches(0.8), Inches(4.1), Inches(6.0), Inches(2.8), BLUE_LIGHT, BLUE_ACCENT)
    tf_s20 = c_s20.text_frame
    tf_s20.margin_left = tf_s20.margin_right = tf_s20.margin_top = Inches(0.16)
    p_gpa_t = tf_s20.paragraphs[0]
    p_gpa_t.text = "📐 SGPA / CGPA COMPUTATIONAL SPECIFICATIONS"
    p_gpa_t.font.size = Pt(11)
    p_gpa_t.font.bold = True
    p_gpa_t.font.color.rgb = NAVY_PRIMARY

    p_sgpa = tf_s20.add_paragraph()
    p_sgpa.space_before = Pt(4)
    add_run(p_sgpa, "SGPA = ∑ ( Grade_Point_i × Credits_i ) / ∑ ( Credits_i )", bold=True, color=RGBColor(67, 56, 202), size=Pt(9.0), font_name='Consolas')

    gpa_notes = [
        ("Credit-Weighted Calculation: ", "Standard courses carry 4.0 academic credits. Sum of credit-points divides by total registered semester credits."),
        ("Tamper-Proof Print Styling: ", "Rendered via @media print CSS with university crest watermark, eliminating navigation bars on physical print."),
        ("Permanent Ledger Record: ", "Stored permanently in scas_results with foreign keys to scas_student_profiles and scas_subjects.")
    ]
    for h, b in gpa_notes:
        p = tf_s20.add_paragraph()
        p.space_before = Pt(4)
        add_run(p, "• " + h, bold=True, color=NAVY_PRIMARY, size=Pt(8.8))
        add_run(p, b, color=TEXT_DARK, size=Pt(8.6))

    # Right: Formal Academic Transcript Mockup
    trans_card = create_card(s20, Inches(7.1), Inches(1.3), Inches(5.4), Inches(5.6), CARD_BG, BORDER_DARK, Pt(2.0))
    
    # Institution Banner inside Transcript
    tx_th = trans_card.text_frame
    tx_th.margin_left = tx_th.margin_right = tx_th.margin_top = Inches(0.14)
    tp1 = tx_th.paragraphs[0]
    tp1.text = "SMART COLLEGE OF ENGINEERING & TECHNOLOGY"
    tp1.font.size = Pt(9.5)
    tp1.font.bold = True
    tp1.font.color.rgb = NAVY_PRIMARY
    tp1.alignment = PP_ALIGN.CENTER

    tp2 = tx_th.add_paragraph()
    tp2.text = "OFFICIAL SEMESTER GRADE STATEMENT"
    tp2.font.size = Pt(8.5)
    tp2.font.bold = True
    tp2.font.color.rgb = BLUE_ACCENT
    tp2.alignment = PP_ALIGN.CENTER

    # Student metadata inside Transcript
    t_sm = s20.shapes.add_table(2, 4, Inches(7.3), Inches(2.2), Inches(5.0), Inches(0.6)).table
    t_sm.columns[0].width = Inches(1.2)
    t_sm.columns[1].width = Inches(1.3)
    t_sm.columns[2].width = Inches(1.2)
    t_sm.columns[3].width = Inches(1.3)
    sm_data = [
        [("Roll No:", True), ("MCA24005", False), ("Program:", True), ("MCA (Sem 1)", False)],
        [("Student Name:", True), ("Jignesh Sathavara", False), ("Result Date:", True), ("2026-09-29", False)]
    ]
    for r, row in enumerate(sm_data):
        for c, (val, is_b) in enumerate(row):
            cell = t_sm.cell(r, c)
            cell.margin_left = cell.margin_right = cell.margin_top = cell.margin_bottom = Inches(0.02)
            cp = cell.text_frame.paragraphs[0]
            cp.text = val
            cp.font.size = Pt(7.5)
            cp.font.bold = is_b
            cp.font.color.rgb = NAVY_PRIMARY if is_b else TEXT_DARK

    # Transcript Subject Table
    t_res = s20.shapes.add_table(3, 5, Inches(7.3), Inches(3.0), Inches(5.0), Inches(1.2)).table
    for i, w in enumerate([Inches(1.0), Inches(1.8), Inches(0.6), Inches(0.8), Inches(0.8)]):
        t_res.columns[i].width = w
    res_headers = ["Code", "Subject Title", "Credits", "Score / 100", "Grade"]
    res_rows = [
        ["MCA-104", "Theory of Computation", "4", "92.0", "O (10.0)"],
        ["MCA-105", "Compiler Design", "4", "76.0", "A (8.0)"]
    ]
    for j, h in enumerate(res_headers):
        c = t_res.cell(0, j)
        c.fill.solid()
        c.fill.fore_color.rgb = NAVY_PRIMARY
        c.margin_left = c.margin_right = c.margin_top = c.margin_bottom = Inches(0.02)
        p = c.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(7.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
    for r, row in enumerate(res_rows):
        for c, val in enumerate(row):
            cell = t_res.cell(r + 1, c)
            cell.margin_left = cell.margin_right = cell.margin_top = cell.margin_bottom = Inches(0.02)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(7.5)
            p.font.color.rgb = TEXT_DARK

    # SGPA Summary Card
    sgpa_card = create_card(s20, Inches(7.3), Inches(4.4), Inches(5.0), Inches(0.9), BLUE_LIGHT, BLUE_ACCENT)
    stf = sgpa_card.text_frame
    stf.margin_left = stf.margin_top = Inches(0.08)
    sp = stf.paragraphs[0]
    sp.text = "SEMESTER SGPA: 9.00 / 10.00   |   CUMULATIVE CGPA: 9.00"
    sp.font.size = Pt(9.0)
    sp.font.bold = True
    sp.font.color.rgb = NAVY_PRIMARY
    sp_sub = stf.add_paragraph()
    sp_sub.text = "Total Credits Earned: 8 / 8   |   Academic Result: PASS (FIRST CLASS WITH DISTINCTION)"
    sp_sub.font.size = Pt(7.5)
    sp_sub.font.color.rgb = GREEN_ACCENT

    # Signature Seal
    sig_tx = s20.shapes.add_textbox(Inches(7.3), Inches(5.5), Inches(5.0), Inches(1.1))
    stf2 = sig_tx.text_frame
    stf2.margin_left = stf2.margin_top = 0
    stp = stf2.paragraphs[0]
    stp.text = "Dean of Academic Affairs                    Controller of Examinations\n(Digital Cryptographic Seal)                 (Verified & Approved)"
    stp.font.size = Pt(7.0)
    stp.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 21: Output Design 5 — Institutional Fee Payment Receipt Voucher
    # =========================================================================
    s21 = prs.slides.add_slide(blank_layout)
    add_header(s21, "Output Design 5: Institutional Fee Payment Receipt Voucher", "FINANCIAL LEDGER & RECEIPTS (FINANCE)")

    t_s21 = s21.shapes.add_table(6, 4, Inches(0.8), Inches(1.3), Inches(6.0), Inches(2.6)).table
    s21_headers = ["Receipt Field", "Voucher Format", "Database Source", "Audit Significance"]
    s21_data = [
        ("Receipt Number", "REC-MCA24005-CSV", "scas_fee_payments.receipt_no", "Unique institutional voucher audit number"),
        ("Banking Reference", "TXN-984712-SUCCESS", "scas_fee_payments.transaction_id", "External UPI/Bank reconciliation key"),
        ("Student Identity", "Roll No & Full Name", "scas_student_profiles, users", "Matriculation account attribution"),
        ("Payment Timestamp", "UTC Date & Time", "scas_fee_payments.payment_date", "Fiscal period clearance verification"),
        ("Payment Status Seal", "PAID & VERIFIED", "scas_fee_payments.status", "Prerequisite for exam hall ticket release")
    ]
    style_spec_table(t_s21, [Inches(1.6), Inches(1.5), Inches(1.3), Inches(1.6)], s21_headers, s21_data, NAVY_PRIMARY, TEXT_LIGHT, ROW_ALT, CARD_BG, NAVY_PRIMARY, FK_COLOR, RED_ACCENT, GREEN_ACCENT, TEXT_DARK)

    c_s21 = create_card(s21, Inches(0.8), Inches(4.1), Inches(6.0), Inches(2.8), BLUE_LIGHT, BLUE_ACCENT)
    tf_s21 = c_s21.text_frame
    tf_s21.margin_left = tf_s21.margin_right = tf_s21.margin_top = Inches(0.16)
    p_s21_t = tf_s21.paragraphs[0]
    p_s21_t.text = "🧾 STATUTORY FINANCIAL RECONCILIATION"
    p_s21_t.font.size = Pt(11)
    p_s21_t.font.bold = True
    p_s21_t.font.color.rgb = NAVY_PRIMARY

    s21_notes = [
        ("No-Dues Hall Ticket Integration: ", "Automated check validates status='Paid' before the student can download their final semester exam hall ticket."),
        ("Exportable Ledger Formats: ", "Receipts can be printed directly as verified PDF vouchers or exported into master administrative CSV accounts spreadsheets.")
    ]
    for h, b in s21_notes:
        p = tf_s21.add_paragraph()
        p.space_before = Pt(6)
        add_run(p, "• " + h, bold=True, color=NAVY_PRIMARY, size=Pt(8.8))
        add_run(p, b, color=TEXT_DARK, size=Pt(8.6))

    # Right: Printable Receipt Mockup Card
    rec_card = create_card(s21, Inches(7.1), Inches(1.3), Inches(5.4), Inches(5.6), CARD_BG, BORDER_DARK, Pt(2.0))
    rtf = rec_card.text_frame
    rtf.margin_left = rtf.margin_right = rtf.margin_top = Inches(0.14)
    rp1 = rtf.paragraphs[0]
    rp1.text = "SMART COLLEGE OF ENGINEERING & TECHNOLOGY"
    rp1.font.size = Pt(9.5)
    rp1.font.bold = True
    rp1.font.color.rgb = NAVY_PRIMARY
    rp1.alignment = PP_ALIGN.CENTER
    rp2 = rtf.add_paragraph()
    rp2.text = "OFFICIAL TUITION FEE RECEIPT VOUCHER"
    rp2.font.size = Pt(8.5)
    rp2.font.bold = True
    rp2.font.color.rgb = GREEN_ACCENT
    rp2.alignment = PP_ALIGN.CENTER

    # Receipt Metadata Table
    t_rm = s21.shapes.add_table(3, 2, Inches(7.3), Inches(2.2), Inches(5.0), Inches(1.0)).table
    t_rm.columns[0].width = Inches(2.0)
    t_rm.columns[1].width = Inches(3.0)
    rm_data = [
        ["Receipt Number: REC-MCA24005-CSV", "Transaction ID: TXN-984712-SUCCESS"],
        ["Student: Jignesh Sathavara", "Roll No: MCA24005 (MCA 2024-2026)"],
        ["Payment Date: 2026-09-29 16:30 UTC", "Payment Mode: Online Banking / UPI"]
    ]
    for r, row in enumerate(rm_data):
        for c, val in enumerate(row):
            cell = t_rm.cell(r, c)
            cell.margin_left = cell.margin_right = cell.margin_top = cell.margin_bottom = Inches(0.02)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(7.5)
            p.font.color.rgb = TEXT_DARK

    # Itemized Breakdown Table
    t_fee = s21.shapes.add_table(4, 2, Inches(7.3), Inches(3.4), Inches(5.0), Inches(1.3)).table
    t_fee.columns[0].width = Inches(3.5)
    t_fee.columns[1].width = Inches(1.5)
    fee_data = [
        ["Semester 1 Tuition & Instruction Fee", "₹ 45,000.00"],
        ["Advanced Computer Laboratory & Cloud Dues", "₹ 12,000.00"],
        ["Digital Library & Institutional Sports Fund", "₹ 5,000.00"],
        ["University Examination & Transcript Levy", "₹ 3,000.00"]
    ]
    for r, (head, amt) in enumerate(fee_data):
        cell1 = t_fee.cell(r, 0)
        cell2 = t_fee.cell(r, 1)
        cell1.margin_left = cell2.margin_left = cell1.margin_top = cell2.margin_top = Inches(0.02)
        cell1.text_frame.paragraphs[0].text = head
        cell1.text_frame.paragraphs[0].font.size = Pt(7.5)
        cell2.text_frame.paragraphs[0].text = amt
        cell2.text_frame.paragraphs[0].font.size = Pt(7.5)
        cell2.text_frame.paragraphs[0].alignment = PP_ALIGN.RIGHT

    # Grand Total Banner
    tot_card = create_card(s21, Inches(7.3), Inches(4.9), Inches(5.0), Inches(0.55), GREEN_LIGHT, GREEN_ACCENT)
    tot_tf = tot_card.text_frame
    tot_p = tot_tf.paragraphs[0]
    tot_p.text = "TOTAL PAID: ₹ 65,000.00 INR   |   STATUS: PAID & VERIFIED"
    tot_p.font.size = Pt(9.0)
    tot_p.font.bold = True
    tot_p.font.color.rgb = GREEN_ACCENT
    tot_p.alignment = PP_ALIGN.CENTER

    # Verification Seal
    v_tx = s21.shapes.add_textbox(Inches(7.3), Inches(5.6), Inches(5.0), Inches(1.0))
    v_tf = v_tx.text_frame
    vp = v_tf.paragraphs[0]
    vp.text = "Finance Officer Signature: _______________________ (College Cashier Seal)\nSystem Generated E-Receipt – Verified via SCAS Financial Ledger."
    vp.font.size = Pt(7.0)
    vp.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 22: Output Design 6 — Class Attendance Register & Defaulters Sheet
    # =========================================================================
    s22 = prs.slides.add_slide(blank_layout)
    add_header(s22, "Output Design 6: Class Attendance Register & Defaulter Compliance Sheet", "ATTENDANCE REPORTING & COMPLIANCE (FACULTY/ADMIN)")

    t_s22 = s22.shapes.add_table(5, 4, Inches(0.8), Inches(1.3), Inches(6.0), Inches(2.4)).table
    s22_headers = ["Report Field", "Data Representation", "Calculation Logic", "Compliance Consequence"]
    s22_data = [
        ("Delivered Lectures", "Count Integer", "Total sessions conducted in date range", "Denominator for percentage"),
        ("Attended Lectures", "Count Integer", "Total 'Present' logs for student", "Numerator for percentage"),
        ("Attendance Rate (%)", "Percentage Stat", "(Attended / Total) * 100", "Must meet 75% threshold"),
        ("Defaulter Flag", "RED WARNING BADGE", "Triggered if Attendance < 75.0%", "Hall ticket debarment notice")
    ]
    style_spec_table(t_s22, [Inches(1.5), Inches(1.3), Inches(1.5), Inches(1.7)], s22_headers, s22_data, NAVY_PRIMARY, TEXT_LIGHT, ROW_ALT, CARD_BG, NAVY_PRIMARY, FK_COLOR, RED_ACCENT, GREEN_ACCENT, TEXT_DARK)

    c_s22 = create_card(s22, Inches(0.8), Inches(3.9), Inches(6.0), Inches(3.0), BLUE_LIGHT, BLUE_ACCENT)
    tf_s22 = c_s22.text_frame
    tf_s22.margin_left = tf_s22.margin_right = tf_s22.margin_top = Inches(0.16)
    ps22_t = tf_s22.paragraphs[0]
    ps22_t.text = "⚠️ STATUTORY DEFAULTER AUDIT TRAIL"
    ps22_t.font.size = Pt(11)
    ps22_t.font.bold = True
    ps22_t.font.color.rgb = NAVY_PRIMARY

    s22_notes = [
        ("Institutional Regulatory Mandate: ", "University regulations mandate minimum 75% class attendance for exam eligibility."),
        ("Medical Leave Offsets: ", "Approved leave applications in scas_leave_applications adjust eligible hours."),
        ("CSV Export Capability: ", "Single-click download delivers full tabular matrix formatted for university academic board review.")
    ]
    for h, b in s22_notes:
        p = tf_s22.add_paragraph()
        p.space_before = Pt(6)
        add_run(p, "• " + h, bold=True, color=NAVY_PRIMARY, size=Pt(8.8))
        add_run(p, b, color=TEXT_DARK, size=Pt(8.6))

    # Right: Attendance Register Mockup Card
    att_mock = create_card(s22, Inches(7.1), Inches(1.3), Inches(5.4), Inches(5.6), CARD_BG, BORDER_LIGHT, Pt(1.5))
    draw_window_bar(s22, Inches(7.1), Inches(1.3), Inches(5.4), "Attendance Compliance & Defaulter Register", NAVY_PRIMARY)

    # Filter Bar Preview
    f_bar = create_card(s22, Inches(7.3), Inches(1.8), Inches(5.0), Inches(0.45), ROW_ALT, BLUE_ACCENT)
    fbtf = f_bar.text_frame
    fbtf.margin_left = fbtf.margin_top = Inches(0.08)
    fbp = fbtf.paragraphs[0]
    fbp.text = "Course: MCA | Subject: Theory of Computation (MCA-104) | Month: Sept 2026"
    fbp.font.size = Pt(7.5)
    fbp.font.bold = True
    fbp.font.color.rgb = NAVY_PRIMARY

    # Register Matrix Table
    t_am = s22.shapes.add_table(4, 6, Inches(7.3), Inches(2.4), Inches(5.0), Inches(2.2)).table
    for i, w in enumerate([Inches(0.9), Inches(1.3), Inches(0.6), Inches(0.6), Inches(0.7), Inches(0.9)]):
        t_am.columns[i].width = w
    am_headers = ["Roll No", "Student Name", "Total", "Att", "Rate %", "Status"]
    am_rows = [
        ["MCA24004", "Himanshu Goswami", "20", "13", "65.0%", "🔴 DEFAULTER"],
        ["MCA24005", "Jignesh Sathavara", "20", "19", "95.0%", "🟢 COMPLIANT"],
        ["MCA24006", "Rahul Sharma", "20", "17", "85.0%", "🟢 COMPLIANT"]
    ]
    for j, h in enumerate(am_headers):
        c = t_am.cell(0, j)
        c.fill.solid()
        c.fill.fore_color.rgb = NAVY_PRIMARY
        c.margin_left = c.margin_right = c.margin_top = c.margin_bottom = Inches(0.02)
        p = c.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(7.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
    for r, row in enumerate(am_rows):
        bg = RED_LIGHT if "DEFAULTER" in row[5] else ROW_ALT
        for c, val in enumerate(row):
            cell = t_am.cell(r + 1, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            cell.margin_left = cell.margin_right = cell.margin_top = cell.margin_bottom = Inches(0.02)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(7.5)
            if c == 5:
                p.font.bold = True
                p.font.color.rgb = RED_ACCENT if "DEFAULTER" in val else GREEN_ACCENT
            else:
                p.font.color.rgb = TEXT_DARK

    # Summary Card
    sum_card = create_card(s22, Inches(7.3), Inches(4.8), Inches(5.0), Inches(0.9), BLUE_LIGHT, BLUE_ACCENT)
    stf = sum_card.text_frame
    stf.margin_left = stf.margin_top = Inches(0.08)
    stp = stf.paragraphs[0]
    stp.text = "📊 BATCH ATTENDANCE SUMMARY"
    stp.font.size = Pt(8.5)
    stp.font.bold = True
    stp.font.color.rgb = NAVY_PRIMARY
    stp_sub = stf.add_paragraph()
    stp_sub.text = "• Total Enrolled: 60   |   Compliant (>=75%): 54 (90%)   |   Defaulters (<75%): 6 (10%)\n• Action: Warning letters generated automatically via Email Engine."
    stp_sub.font.size = Pt(7.5)
    stp_sub.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 23: Output Design 7 — CIE Mark Sheet & Assessment Breakdown
    # =========================================================================
    s23 = prs.slides.add_slide(blank_layout)
    add_header(s23, "Output Design 7: Continuous Internal Evaluation (CIE) Mark Sheet", "INTERNAL ASSESSMENT & EXAMINATION (FACULTY)")

    t_s23 = s23.shapes.add_table(5, 4, Inches(0.8), Inches(1.3), Inches(6.0), Inches(2.4)).table
    s23_headers = ["Evaluation Head", "Benchmark Weight", "Database Column", "Scaling Formula"]
    s23_data = [
        ("Midterm Exam 1", "30.0 Marks (20%)", "exam_type = 'Midterm 1'", "(Score / 30) * 20"),
        ("Midterm Exam 2", "30.0 Marks (20%)", "exam_type = 'Midterm 2'", "(Score / 30) * 20"),
        ("Assignments / Quizzes", "20.0 Marks (10%)", "exam_type = 'Assignment'", "(Score / 20) * 10"),
        ("Final Semester Exam", "70.0 Marks (50%)", "exam_type = 'Final Exam'", "(Score / 70) * 50")
    ]
    style_spec_table(t_s23, [Inches(1.6), Inches(1.4), Inches(1.4), Inches(1.6)], s23_headers, s23_data, NAVY_PRIMARY, TEXT_LIGHT, ROW_ALT, CARD_BG, NAVY_PRIMARY, FK_COLOR, RED_ACCENT, GREEN_ACCENT, TEXT_DARK)

    c_s23 = create_card(s23, Inches(0.8), Inches(3.9), Inches(6.0), Inches(3.0), BLUE_LIGHT, BLUE_ACCENT)
    tf_s23 = c_s23.text_frame
    tf_s23.margin_left = tf_s23.margin_right = tf_s23.margin_top = Inches(0.16)
    ps23_t = tf_s23.paragraphs[0]
    ps23_t.text = "📈 CONTINUOUS INTERNAL EVALUATION SCHEME"
    ps23_t.font.size = Pt(11)
    ps23_t.font.bold = True
    ps23_t.font.color.rgb = NAVY_PRIMARY

    s23_notes = [
        ("Multi-Component Aggregate: ", "Combines midterms, assignments, and practical labs to evaluate continuous student growth."),
        ("Faculty Approval Workflow: ", "Marks remain editable during assessment window; finalized marks lock into immutable semester results."),
        ("Statistical Distribution Metrics: ", "Calculates batch median, standard deviation, and identifies underperforming learning outcomes.")
    ]
    for h, b in s23_notes:
        p = tf_s23.add_paragraph()
        p.space_before = Pt(6)
        add_run(p, "• " + h, bold=True, color=NAVY_PRIMARY, size=Pt(8.8))
        add_run(p, b, color=TEXT_DARK, size=Pt(8.6))

    # Right: Mark Sheet Table Mockup
    m_mock = create_card(s23, Inches(7.1), Inches(1.3), Inches(5.4), Inches(5.6), CARD_BG, BORDER_LIGHT, Pt(1.5))
    draw_window_bar(s23, Inches(7.1), Inches(1.3), Inches(5.4), "Faculty Mark Register & CIE Ledger", NAVY_PRIMARY)

    # Subject header
    sh = create_card(s23, Inches(7.3), Inches(1.8), Inches(5.0), Inches(0.45), ROW_ALT, BLUE_ACCENT)
    shtf = sh.text_frame
    shtf.margin_left = shtf.margin_top = Inches(0.08)
    shp = shtf.paragraphs[0]
    shp.text = "Subject: Compiler Design (MCA-105) | Faculty: Prof. Sanjaybhai Patel"
    shp.font.size = Pt(7.5)
    shp.font.bold = True
    shp.font.color.rgb = NAVY_PRIMARY

    # Mark Ledger Table
    t_ml = s23.shapes.add_table(4, 6, Inches(7.3), Inches(2.4), Inches(5.0), Inches(2.2)).table
    for i, w in enumerate([Inches(0.9), Inches(1.2), Inches(0.7), Inches(0.7), Inches(0.7), Inches(0.8)]):
        t_ml.columns[i].width = w
    ml_headers = ["Roll No", "Student Name", "Mid 1 (30)", "Mid 2 (30)", "Assign (20)", "Total (100)"]
    ml_rows = [
        ["MCA24004", "Himanshu Goswami", "24.0", "25.0", "18.0", "82.0 (A)"],
        ["MCA24005", "Jignesh Sathavara", "28.0", "29.0", "20.0", "92.0 (O)"],
        ["MCA24006", "Rahul Sharma", "22.0", "23.5", "17.0", "76.0 (A)"]
    ]
    for j, h in enumerate(ml_headers):
        c = t_ml.cell(0, j)
        c.fill.solid()
        c.fill.fore_color.rgb = NAVY_PRIMARY
        c.margin_left = c.margin_right = c.margin_top = c.margin_bottom = Inches(0.02)
        p = c.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(7.2)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
    for r, row in enumerate(ml_rows):
        for c, val in enumerate(row):
            cell = t_ml.cell(r + 1, c)
            cell.margin_left = cell.margin_right = cell.margin_top = cell.margin_bottom = Inches(0.02)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(7.2)
            if c == 5:
                p.font.bold = True
                p.font.color.rgb = GREEN_ACCENT if "(O)" in val else BLUE_ACCENT
            else:
                p.font.color.rgb = TEXT_DARK

    # Class Performance Stats Box
    cp_card = create_card(s23, Inches(7.3), Inches(4.8), Inches(5.0), Inches(0.9), BLUE_LIGHT, BLUE_ACCENT)
    cptf = cp_card.text_frame
    cptf.margin_left = cptf.margin_top = Inches(0.08)
    cpp = cptf.paragraphs[0]
    cpp.text = "📊 COHORT STATISTICAL BENCHMARKS"
    cpp.font.size = Pt(8.5)
    cpp.font.bold = True
    cpp.font.color.rgb = NAVY_PRIMARY
    cpp_sub = cptf.add_paragraph()
    cpp_sub.text = "• Class Average: 83.3 / 100   |   Highest Score: 92.0 (Jignesh Sathavara)\n• Passing Rate: 100%   |   Grading Schema: Relative Bell Curve Compliant"
    cpp_sub.font.size = Pt(7.5)
    cpp_sub.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 24: Output Design 8 — Automated Transactional Email Communications
    # =========================================================================
    s24 = prs.slides.add_slide(blank_layout)
    add_header(s24, "Output Design 8: Automated Transactional Email Communications", "SMTP EMAIL ENGINE (NOTIFICATION)")

    t_s24 = s24.shapes.add_table(4, 4, Inches(0.8), Inches(1.3), Inches(6.0), Inches(2.2)).table
    s24_headers = ["Email Notification Type", "Trigger Event", "Dynamic Content Injected", "Delivery Mode"]
    s24_data = [
        ("Account Provisioning", "User creation (Admin)", "Username, Temp Password, Login URL", "SMTP / Mock Log"),
        ("Password Reset Link", "Self-service reset request", "1-Hour Signed Cryptographic URL", "SMTP / Mock Log"),
        ("Low Attendance Alert", "Attendance < 75% detected", "Attendance %, Course Title, Dean Warning", "SMTP / Mock Log")
    ]
    style_spec_table(t_s24, [Inches(1.6), Inches(1.4), Inches(1.8), Inches(1.2)], s24_headers, s24_data, NAVY_PRIMARY, TEXT_LIGHT, ROW_ALT, CARD_BG, NAVY_PRIMARY, FK_COLOR, RED_ACCENT, GREEN_ACCENT, TEXT_DARK)

    c_s24 = create_card(s24, Inches(0.8), Inches(3.7), Inches(6.0), Inches(3.2), BLUE_LIGHT, BLUE_ACCENT)
    tf_s24 = c_s24.text_frame
    tf_s24.margin_left = tf_s24.margin_right = tf_s24.margin_top = Inches(0.16)
    ps24_t = tf_s24.paragraphs[0]
    ps24_t.text = "✉️ DUAL-TRANSPORT EMAIL ARCHITECTURE"
    ps24_t.font.size = Pt(11)
    ps24_t.font.bold = True
    ps24_t.font.color.rgb = NAVY_PRIMARY

    s24_notes = [
        ("Live SMTP Production Delivery: ", "Connects to Gmail / Institutional SMTP server on port 587 using TLS encryption."),
        ("Transactional Fallback Logger: ", "If SMTP credentials are unset or offline, writes structured emails directly to sent_emails.log."),
        ("Non-Blocking Execution: ", "Email errors are handled gracefully without aborting core database transactions.")
    ]
    for h, b in s24_notes:
        p = tf_s24.add_paragraph()
        p.space_before = Pt(6)
        add_run(p, "• " + h, bold=True, color=NAVY_PRIMARY, size=Pt(8.8))
        add_run(p, b, color=TEXT_DARK, size=Pt(8.6))

    # Right: Formal Email Wireframe Preview
    em_mock = create_card(s24, Inches(7.1), Inches(1.3), Inches(5.4), Inches(5.6), CARD_BG, BORDER_LIGHT, Pt(1.5))
    draw_window_bar(s24, Inches(7.1), Inches(1.3), Inches(5.4), "System Email Dispatch Preview", NAVY_PRIMARY)

    # Email Envelope Header
    eh = create_card(s24, Inches(7.3), Inches(1.8), Inches(5.0), Inches(0.9), ROW_ALT, BORDER_LIGHT)
    ehtf = eh.text_frame
    ehtf.margin_left = ehtf.margin_top = Inches(0.08)
    ep1 = ehtf.paragraphs[0]
    ep1.text = "From: Smart College Portal <admin@college.edu>"
    ep1.font.size = Pt(7.5)
    ep1.font.bold = True
    ep1.font.color.rgb = NAVY_PRIMARY
    ep2 = ehtf.add_paragraph()
    ep2.text = "To: testmanstudent@college.edu (Test Manual Student)"
    ep2.font.size = Pt(7.5)
    ep2.font.color.rgb = TEXT_DARK
    ep3 = ehtf.add_paragraph()
    ep3.text = "Subject: Smart College Portal - Account Access Credentials"
    ep3.font.size = Pt(7.5)
    ep3.font.bold = True
    ep3.font.color.rgb = BLUE_ACCENT

    # Email Body Box
    eb = create_card(s24, Inches(7.3), Inches(2.8), Inches(5.0), Inches(3.9), BLUE_LIGHT, BLUE_ACCENT)
    ebtf = eb.text_frame
    ebtf.margin_left = ebtf.margin_right = ebtf.margin_top = Inches(0.12)
    ebp = ebtf.paragraphs[0]
    ebp.text = "Hello Test Manual Student,\n\nYour account on the Smart College Analytics System has been provisioned.\n\nPortal Access Credentials:\n• Portal Role: STUDENT\n• Login ID (Email): testmanstudent@college.edu\n• Temporary Password: tempPass123\n\n⚠️ IMPORTANT NOTICE:\nThis is a temporary system password. You are kindly requested to log in and change your password immediately upon first access.\n\nBest regards,\nDean System Administrator\nSmart College Portal Support Team"
    ebp.font.size = Pt(7.8)
    ebp.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 25: Master Traceability & Database Cross-Reference Matrix
    # =========================================================================
    s25 = prs.slides.add_slide(blank_layout)
    add_header(s25, "Master Traceability Matrix: Input Forms, Database & Outputs", "SYSTEM TRACEABILITY & INTEGRATION MATRIX")

    t_s25 = s25.shapes.add_table(11, 5, Inches(0.8), Inches(1.3), Inches(11.7), Inches(4.3)).table
    s25_headers = ["Subsystem / Screen", "Input Controls", "Underlying Database Table", "Validation & Business Rules", "Generated Output Deliverable"]
    s25_widths = [Inches(2.0), Inches(2.2), Inches(2.2), Inches(2.7), Inches(2.6)]
    s25_data = [
        ("Authentication & Login", "Text, Masked Password, CSRF", "scas_users", "Scrypt hash check, RBAC routing", "Role-directed portal dashboard"),
        ("Password Recovery", "Email, URL Token, New Pass", "scas_users, itsdangerous", "1-hr TTL signed URL token", "Transactional reset email & confirmation"),
        ("User Account Manager", "Single form & Multi-CSV", "scas_users, profiles", "Unique username/email, atomic", "Roster table & credential emails"),
        ("Curriculum Manager", "Course/Batch/Subject Select", "scas_courses, batches, sub", "Code uniqueness, cascade FKs", "Course catalog & timetable slots"),
        ("Attendance Register", "Subject select, Date, Toggles", "scas_attendance", "Composite unique date check", "Defaulter list (<75%) & export CSV"),
        ("Marks Entry (CIE)", "Exam Type, Max marks, Score", "scas_marks", "0.0 <= score <= max_marks", "CIE mark register & grade distribution"),
        ("Lecture Timetable", "Day, Time interval, Room", "scas_schedules", "Room & faculty collision guards", "Weekly schedule matrix grid"),
        ("Fee Payment Gateway", "Amount, Payment mode, UPI", "scas_fee_payments", "Idempotent TXN ID, no-dues", "Printable fee receipt & hall ticket release"),
        ("Leave Workflow", "Type, Date range, Reason", "scas_leave_applications", "start_date <= end_date", "Approval history & attendance waiver"),
        ("Unit Diagnostic Quiz", "25 Multiple-Choice Radios", "scas_test_assessments", "Auto-grading, mastery scale", "Learning growth delta & score summary")
    ]
    style_spec_table(t_s25, s25_widths, s25_headers, s25_data, NAVY_PRIMARY, TEXT_LIGHT, ROW_ALT, CARD_BG, NAVY_PRIMARY, FK_COLOR, RED_ACCENT, GREEN_ACCENT, TEXT_DARK)

    # Master Defense Summary Callout
    c_s25 = create_card(s25, Inches(0.8), Inches(5.8), Inches(11.7), Inches(1.15), BLUE_LIGHT, BLUE_ACCENT)
    tf_s25 = c_s25.text_frame
    tf_s25.margin_left = tf_s25.margin_right = tf_s25.margin_top = Inches(0.14)
    ps25_t = tf_s25.paragraphs[0]
    ps25_t.text = "🎓 ACADEMIC PROJECT DEFENSE SUMMARY & ARCHITECTURAL HIGHLIGHTS"
    ps25_t.font.size = Pt(11)
    ps25_t.font.bold = True
    ps25_t.font.color.rgb = NAVY_PRIMARY

    ps25_sub = tf_s25.add_paragraph()
    ps25_sub.space_before = Pt(4)
    add_run(ps25_sub, "• Comprehensive Traceability: ", bold=True, color=NAVY_PRIMARY, size=Pt(9.0))
    add_run(ps25_sub, "Every single user input correlates strictly to relational entities in scas_db and produces validated, multi-channel outputs. ", color=TEXT_DARK, size=Pt(8.8))
    add_run(ps25_sub, "• Robust Security: ", bold=True, color=BLUE_ACCENT, size=Pt(9.0))
    add_run(ps25_sub, "OWASP compliance via Scrypt hashing, role isolation decorators, CSRF mitigation, and transactional rollback. ", color=TEXT_DARK, size=Pt(8.8))
    add_run(ps25_sub, "• Decision Intelligence: ", bold=True, color=GREEN_ACCENT, size=Pt(9.0))
    add_run(ps25_sub, "Empowers institutional leaders and faculty with predictive analytics to proactively combat student academic attrition.", color=TEXT_DARK, size=Pt(8.8))

    return prs

if __name__ == '__main__':
    print("Building Smart College Analytics System (SCAS) Input & Output Design Presentation...")
    prs = build_full_deck()
    
    # Save target in scas-final and root workspace
    output_path1 = os.path.join(os.path.dirname(__file__), "SCAS_Input_and_Output_Design.pptx")
    prs.save(output_path1)
    print(f"[SUCCESS] Presentation saved to: {output_path1}")

    # Also save to root workspace directory
    output_path2 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "SCAS_Input_and_Output_Design.pptx"))
    prs.save(output_path2)
    print(f"[SUCCESS] Presentation copied to root: {output_path2}")

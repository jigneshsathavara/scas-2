import os
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

def draw_wrapped_text(draw, text, box_x, box_y, max_width, font, fill, line_spacing=4):
    words = text.split(" ")
    lines = []
    current_line = []
    
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(" ".join(current_line))
        
    y = box_y
    for line in lines:
        draw.text((box_x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), line, font=font)
        h = bbox[3] - bbox[1]
        y += h + line_spacing
    return y

def draw_status_badge(draw, x, y, is_positive=True, size=24):
    if is_positive:
        # Green Circle with checkmark
        draw.ellipse([(x, y), (x + size, y + size)], fill=(34, 197, 94))
        # Draw checkmark lines
        draw.line([(x + 6, y + 12), (x + 10, y + 17)], fill=(15, 23, 42), width=3)
        draw.line([(x + 10, y + 17), (x + 18, y + 7)], fill=(15, 23, 42), width=3)
    else:
        # Red Circle with X
        draw.ellipse([(x, y), (x + size, y + size)], fill=(239, 68, 68))
        # Draw X lines
        draw.line([(x + 7, y + 7), (x + 17, y + 17)], fill=(255, 255, 255), width=3)
        draw.line([(x + 17, y + 7), (x + 7, y + 17)], fill=(255, 255, 255), width=3)

def create_infographic():
    W, H = 1920, 1080
    img = Image.new("RGB", (W, H), color=(15, 23, 42)) # Slate 900
    draw = ImageDraw.Draw(img)

    font_title = get_font("segoeuib.ttf", 36, bold=True)
    font_sub = get_font("segoeuib.ttf", 16, bold=True)
    font_h1 = get_font("segoeuib.ttf", 22, bold=True)
    font_body_bold = get_font("segoeuib.ttf", 16, bold=True)
    font_body = get_font("segoeui.ttf", 14)
    font_small = get_font("segoeui.ttf", 12)
    font_kpi_num = get_font("segoeuib.ttf", 38, bold=True)
    font_kpi_lbl = get_font("segoeuib.ttf", 15, bold=True)

    # Top Header Banner
    draw.rectangle([(0, 0), (W, 130)], fill=(26, 54, 93))
    draw.text((60, 20), "SMART COLLEGE ANALYTICS SYSTEM (SCAS)", font=font_sub, fill=(56, 189, 248))
    draw.text((60, 50), "COMPARATIVE SYSTEM STUDY: LEGACY VS. SCAS PLATFORM", font=font_title, fill=(255, 255, 255))
    draw.line([(0, 130), (W, 130)], fill=(56, 189, 248), width=3)

    # -------------------------------------------------------------
    # 2 MAIN COLUMNS
    # -------------------------------------------------------------
    col_w = 880
    top_y = 155

    # Left Box: Traditional Legacy System
    draw.rounded_rectangle([(60, top_y), (60 + col_w, top_y + 655)], radius=16, fill=(30, 41, 59), outline=(239, 68, 68), width=2)
    draw.rounded_rectangle([(60, top_y), (60 + col_w, top_y + 60)], radius=16, fill=(69, 10, 10))
    draw.rectangle([(60, top_y + 40), (60 + col_w, top_y + 60)], fill=(69, 10, 10))
    draw_status_badge(draw, 85, top_y + 18, is_positive=False, size=24)
    draw.text((120, top_y + 16), "TRADITIONAL / LEGACY MANUAL SYSTEM", font=font_h1, fill=(248, 113, 113))

    # Right Box: SCAS System
    rx = 980
    draw.rounded_rectangle([(rx, top_y), (rx + col_w, top_y + 655)], radius=16, fill=(30, 41, 59), outline=(34, 197, 94), width=2)
    draw.rounded_rectangle([(rx, top_y), (rx + col_w, top_y + 60)], radius=16, fill=(5, 46, 22))
    draw.rectangle([(rx, top_y + 40), (rx + col_w, top_y + 60)], fill=(5, 46, 22))
    draw_status_badge(draw, rx + 25, top_y + 18, is_positive=True, size=24)
    draw.text((rx + 60, top_y + 16), "SCAS MODERN CLOUD-READY ERP PLATFORM", font=font_h1, fill=(74, 222, 128))

    features = [
        {
            "cat": "1. Attendance Tracking",
            "old": "Manual roll call in paper registers; end-semester tallying; high proxy vulnerability; zero real-time shortage alerts.",
            "new": "1-Click digital attendance; instant SQL sync; real-time % dashboard; automated low-attendance warnings (<75%)."
        },
        {
            "cat": "2. Marks & GPA Engine",
            "old": "Manual spreadsheet formulas; human calculation errors; delayed semester grade processing; disconnected records.",
            "new": "Automated SGPA & CGPA evaluation; 100% calculation precision; dynamic interactive Chart.js analytics graphs."
        },
        {
            "cat": "3. Leave & Duty Slips",
            "old": "Physical handwritten paper applications; manual faculty signatures; high rate of lost or delayed slips.",
            "new": "Online student leave application portal; instant 1-click faculty review & approval; full audit trail & history."
        },
        {
            "cat": "4. Fee Management",
            "old": "Physical fee receipt books; long counter queues; manual ledger reconciliation; lack of instant status.",
            "new": "Centralized fee status portal (Paid/Pending); automated receipt generation with unique IDs; instant admin audit."
        },
        {
            "cat": "5. Notice Dissemination",
            "old": "Paper flyers posted on corridor notice boards; high miss rate; delayed dissemination of urgent alerts.",
            "new": "Digital Notice Board with priority pinning, role targeting (Admin/Faculty/Student), and automated SMTP emails."
        },
        {
            "cat": "6. Placement Readiness",
            "old": "Zero preparation support integrated; students rely entirely on external third-party coaching portals.",
            "new": "Integrated Mock Placement Aptitude Engine with timed assessments, question banks, and instant scoreboards."
        }
    ]

    row_y = top_y + 70
    row_height = 96
    for idx, f in enumerate(features):
        curr_y = row_y + idx * row_height

        if idx % 2 == 1:
            draw.rectangle([(65, curr_y - 2), (60 + col_w - 5, curr_y + row_height - 6)], fill=(38, 50, 72))
            draw.rectangle([(rx + 5, curr_y - 2), (rx + col_w - 5, curr_y + row_height - 6)], fill=(38, 50, 72))

        # Left Column text
        draw.text((85, curr_y + 4), f["cat"], font=font_body_bold, fill=(252, 165, 165))
        draw_wrapped_text(draw, f["old"], 85, curr_y + 28, col_w - 60, font=font_body, fill=(226, 232, 240), line_spacing=3)

        # Right Column text
        draw.text((rx + 25, curr_y + 4), f["cat"], font=font_body_bold, fill=(134, 239, 172))
        draw_wrapped_text(draw, f["new"], rx + 25, curr_y + 28, col_w - 60, font=font_body, fill=(226, 232, 240), line_spacing=3)

    # -------------------------------------------------------------
    # BOTTOM KPI SCORECARDS
    # -------------------------------------------------------------
    kpis = [
        {"stat": "99.8%", "label": "Time Saved in Attendance", "sub": "Instant vs 5 Days manual end-sem audit", "color": (56, 189, 248)},
        {"stat": "100%", "label": "GPA & Calculation Precision", "sub": "Eliminates all human math & formula errors", "color": (74, 222, 128)},
        {"stat": "95%", "label": "Faster Leave Approvals", "sub": "< 5 min turnaround vs 4 days paper routing", "color": (251, 191, 36)},
        {"stat": "0", "label": "Paper Footprint / Eco-Friendly", "sub": "100% digitalized cloud-ready workflow", "color": (168, 85, 247)}
    ]

    kpi_y = 835
    kpi_w = 420
    kpi_gap = 33
    start_kx = 60

    for i, k in enumerate(kpis):
        kx = start_kx + i * (kpi_w + kpi_gap)
        draw.rounded_rectangle([(kx, kpi_y), (kx + kpi_w, kpi_y + 185)], radius=12, fill=(26, 41, 66), outline=k["color"], width=2)
        draw.text((kx + 20, kpi_y + 12), k["stat"], font=font_kpi_num, fill=k["color"])
        draw.text((kx + 20, kpi_y + 72), k["label"], font=font_kpi_lbl, fill=(255, 255, 255))
        draw.text((kx + 20, kpi_y + 105), k["sub"], font=font_small, fill=(148, 163, 184))

    # Footer
    draw.text((60, 1045), "Smart College Analytics System (SCAS) | Department of Computer Science & Applications | MCA Comparative Study", font=font_small, fill=(100, 116, 139))
    draw.text((1600, 1045), "Prepared for PPT Presentation", font=font_small, fill=(100, 116, 139))

    out_path = os.path.join(os.getcwd(), "scas_vs_old_system_infographic.png")
    img.save(out_path, quality=95)
    print(f"Infographic generated at: {out_path}")

def create_workflow_diagram():
    W, H = 1920, 1080
    img = Image.new("RGB", (W, H), color=(15, 23, 42)) # Slate 900
    draw = ImageDraw.Draw(img)

    font_title = get_font("segoeuib.ttf", 36, bold=True)
    font_h1 = get_font("segoeuib.ttf", 20, bold=True)
    font_step = get_font("segoeuib.ttf", 15, bold=True)
    font_body = get_font("segoeui.ttf", 13)
    font_small = get_font("segoeui.ttf", 12)
    font_badge = get_font("segoeuib.ttf", 13, bold=True)

    # Header
    draw.rectangle([(0, 0), (W, 125)], fill=(26, 54, 93))
    draw.text((60, 18), "VISUAL WORKFLOW ARCHITECTURE COMPARISON", font=get_font("segoeuib.ttf", 16, bold=True), fill=(56, 189, 248))
    draw.text((60, 48), "FRAGMENTED MANUAL PROCESS VS. UNIFIED SCAS DIGITAL PIPELINE", font=font_title, fill=(255, 255, 255))
    draw.line([(0, 125), (W, 125)], fill=(56, 189, 248), width=3)

    # Section 1: Legacy Fragmented Workflow
    top_y1 = 150
    draw.rounded_rectangle([(60, top_y1), (1860, top_y1 + 400)], radius=16, fill=(30, 41, 59), outline=(239, 68, 68), width=2)
    draw.rounded_rectangle([(60, top_y1), (1860, top_y1 + 50)], radius=16, fill=(69, 10, 10))
    draw.rectangle([(60, top_y1 + 30), (1860, top_y1 + 50)], fill=(69, 10, 10))
    draw_status_badge(draw, 85, top_y1 + 13, is_positive=False, size=24)
    draw.text((120, top_y1 + 12), "LEGACY SYSTEM: DISCONNECTED, PAPER-BOUND WORKFLOW (HIGH LATENCY & HIGH ERROR RATE)", font=font_h1, fill=(248, 113, 113))

    old_steps = [
        {"title": "Step 1: Paper Roll Call", "desc": "Faculty records attendance in physical paper register. High risk of proxy & register damage."},
        {"title": "Step 2: Isolated Excel Entry", "desc": "Marks entered on individual laptops in disconnected Excel files. Data redundancy & silos."},
        {"title": "Step 3: End-Term Manual Audit", "desc": "3-5 days calculating percentages & GPAs manually using calculator/Excel formulas."},
        {"title": "Step 4: Physical Notice Board", "desc": "Circulars & results printed and pinned on walls. Students miss critical updates."},
        {"title": "Step 5: Paper Leave Requests", "desc": "Physical handwritten slips carried between faculty & HOD offices. Frequently lost."}
    ]

    step_w = 310
    step_gap = 45
    start_x = 90
    step_y = top_y1 + 75

    for i, s in enumerate(old_steps):
        sx = start_x + i * (step_w + step_gap)
        # Step card
        draw.rounded_rectangle([(sx, step_y), (sx + step_w, step_y + 300)], radius=12, fill=(45, 55, 72), outline=(239, 68, 68), width=1)
        draw.rounded_rectangle([(sx, step_y), (sx + step_w, step_y + 45)], radius=12, fill=(80, 20, 20))
        draw.rectangle([(sx, step_y + 30), (sx + step_w, step_y + 45)], fill=(80, 20, 20))
        draw.text((sx + 15, step_y + 12), s["title"], font=font_step, fill=(254, 202, 202))

        # Description with wrap
        draw_wrapped_text(draw, s["desc"], sx + 15, step_y + 60, step_w - 30, font=font_body, fill=(226, 232, 240), line_spacing=4)
        
        # Bottleneck warning
        draw.rounded_rectangle([(sx + 15, step_y + 245), (sx + step_w - 15, step_y + 285)], radius=6, fill=(127, 29, 29))
        draw.text((sx + 25, step_y + 253), "[!] Bottleneck: Manual Delay", font=font_badge, fill=(254, 202, 202))

        # Connector arrow
        if i < len(old_steps) - 1:
            arr_x = sx + step_w + 10
            arr_y = step_y + 140
            draw.line([(arr_x, arr_y), (arr_x + 22, arr_y)], fill=(239, 68, 68), width=4)
            draw.polygon([(arr_x + 22, arr_y - 8), (arr_x + 32, arr_y), (arr_x + 22, arr_y + 8)], fill=(239, 68, 68))

    # Section 2: SCAS Digital Unified Pipeline
    top_y2 = 580
    draw.rounded_rectangle([(60, top_y2), (1860, top_y2 + 430)], radius=16, fill=(30, 41, 59), outline=(34, 197, 94), width=2)
    draw.rounded_rectangle([(60, top_y2), (1860, top_y2 + 50)], radius=16, fill=(5, 46, 22))
    draw.rectangle([(60, top_y2 + 30), (1860, top_y2 + 50)], fill=(5, 46, 22))
    draw_status_badge(draw, 85, top_y2 + 13, is_positive=True, size=24)
    draw.text((120, top_y2 + 12), "SCAS PLATFORM: AUTOMATED, REAL-TIME 3-TIER WEB PIPELINE (ZERO LATENCY & 100% PRECISION)", font=font_h1, fill=(74, 222, 128))

    new_steps = [
        {"title": "Step 1: 1-Click Digital Logging", "desc": "Faculty records attendance on React 19 UI in seconds; live sync to MySQL database.", "badge": "Instant Sync"},
        {"title": "Step 2: Centralized SQL Storage", "desc": "12 normalized tables store students, marks, subjects, and fees with relational integrity.", "badge": "Secure RBAC"},
        {"title": "Step 3: Auto GPA & Analytics", "desc": "Automated SGPA/CGPA evaluation engine with dynamic interactive Chart.js analytics.", "badge": "100% Precision"},
        {"title": "Step 4: Smart Alerts & Mail", "desc": "Real-time badge warning (<75%) + SMTP email notifications for notices & alerts.", "badge": "Real-time Alerts"},
        {"title": "Step 5: Placement Mock Engine", "desc": "Built-in aptitude exam engine with timed questions and instant scoreboards.", "badge": "Career Ready"}
    ]

    step_y2 = top_y2 + 75

    for i, s in enumerate(new_steps):
        sx = start_x + i * (step_w + step_gap)
        draw.rounded_rectangle([(sx, step_y2), (sx + step_w, step_y2 + 325)], radius=12, fill=(24, 38, 58), outline=(34, 197, 94), width=1)
        draw.rounded_rectangle([(sx, step_y2), (sx + step_w, step_y2 + 45)], radius=12, fill=(15, 75, 40))
        draw.rectangle([(sx, step_y2 + 30), (sx + step_w, step_y2 + 45)], fill=(15, 75, 40))
        draw.text((sx + 15, step_y2 + 12), s["title"], font=font_step, fill=(187, 247, 208))

        # Description with wrap
        draw_wrapped_text(draw, s["desc"], sx + 15, step_y2 + 60, step_w - 30, font=font_body, fill=(226, 232, 240), line_spacing=4)

        # Value Badge
        draw.rounded_rectangle([(sx + 15, step_y2 + 270), (sx + step_w - 15, step_y2 + 310)], radius=6, fill=(34, 197, 94))
        draw.text((sx + 25, step_y2 + 278), ">>> " + s["badge"], font=font_badge, fill=(15, 23, 42))

        # Connector arrow
        if i < len(new_steps) - 1:
            arr_x = sx + step_w + 10
            arr_y = step_y2 + 150
            draw.line([(arr_x, arr_y), (arr_x + 22, arr_y)], fill=(34, 197, 94), width=4)
            draw.polygon([(arr_x + 22, arr_y - 8), (arr_x + 32, arr_y), (arr_x + 22, arr_y + 8)], fill=(34, 197, 94))

    # Footer
    draw.text((60, 1045), "Smart College Analytics System (SCAS) | Department of Computer Science & Applications | MCA Comparative Study", font=font_small, fill=(100, 116, 139))

    out_path = os.path.join(os.getcwd(), "scas_vs_old_system_workflow_diagram.png")
    img.save(out_path, quality=95)
    print(f"Workflow Diagram generated at: {out_path}")

if __name__ == "__main__":
    create_infographic()
    create_workflow_diagram()

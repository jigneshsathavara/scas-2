"""
Generate an interactive, printable HTML version of the SCAS Data Dictionary
that mirrors the demo specification design.
"""

import json
from generate_data_dictionary import DATA_DICTIONARY_TABLES, DEMO_TABLE

def generate_html(output_path):
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SCAS Data Dictionary - Section 4.2 Specification</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #1e293b;
            --accent: #b91c1c;
            --border: #000000;
            --bg-light: #f8fafc;
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: #0f172a;
            background-color: #f1f5f9;
            padding: 24px;
            line-height: 1.5;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: #ffffff;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1);
        }}
        
        .no-print-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #1e293b;
            color: #ffffff;
            padding: 12px 24px;
            border-radius: 6px;
            margin-bottom: 24px;
        }}
        
        .btn {{
            background: #b91c1c;
            color: #ffffff;
            border: none;
            padding: 8px 18px;
            border-radius: 4px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            transition: background 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}
        .btn:hover {{
            background: #991b1b;
        }}
        
        .nav-select {{
            padding: 6px 12px;
            border-radius: 4px;
            border: 1px solid #cbd5e1;
            font-size: 14px;
            background: #ffffff;
            color: #0f172a;
        }}
        
        .header {{
            text-align: center;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 24px;
            margin-bottom: 32px;
        }}
        
        .univ-badge {{
            color: #b91c1c;
            font-weight: 700;
            font-size: 14px;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }}
        
        .inst-sub {{
            color: #64748b;
            font-size: 13px;
            margin-top: 2px;
            font-weight: 500;
        }}
        
        h1 {{
            font-size: 26px;
            font-weight: 700;
            margin-top: 10px;
            color: #0f172a;
        }}
        
        .subtitle {{
            color: #475569;
            font-size: 15px;
            margin-top: 4px;
        }}
        
        .section-badge {{
            display: inline-block;
            background: #f1f5f9;
            color: #0f172a;
            padding: 4px 12px;
            border-radius: 4px;
            font-weight: 700;
            font-size: 14px;
            margin-top: 8px;
            border: 1px solid #cbd5e1;
        }}
        
        .card {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 16px 20px;
            margin-bottom: 28px;
            font-size: 14px;
            color: #334155;
        }}
        
        .card h2 {{
            font-size: 16px;
            color: #0f172a;
            margin-bottom: 8px;
        }}
        
        /* Master Index Table */
        .index-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13.5px;
            margin-top: 12px;
        }}
        
        .index-table th, .index-table td {{
            border: 1px solid #cbd5e1;
            padding: 8px 12px;
            text-align: left;
        }}
        
        .index-table th {{
            background: #f1f5f9;
            font-weight: 600;
        }}
        
        /* --- DEMO SPECIFICATION DESIGN (Exact Match to screenshot) --- */
        .data-dict-unit {{
            margin-bottom: 40px;
            page-break-after: always;
        }}
        
        .data-dict-title {{
            font-size: 16px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .dict-container {{
            border: 1.5px solid #000000;
            background: #ffffff;
        }}
        
        .dict-header-box {{
            padding: 10px 14px;
            border-bottom: 1.5px solid #000000;
            font-size: 13.5px;
            line-height: 1.55;
            background: #ffffff;
        }}
        
        .dict-header-box .meta-line {{
            margin-bottom: 4px;
        }}
        
        .dict-header-box .meta-line:last-child {{
            margin-bottom: 0;
        }}
        
        .dict-header-box strong {{
            font-weight: 700;
            color: #000000;
        }}
        
        .dict-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}
        
        .dict-table th, .dict-table td {{
            border: 1px solid #000000;
            padding: 7px 10px;
            vertical-align: top;
            text-align: left;
        }}
        
        .dict-table th {{
            background: #ffffff;
            font-weight: 700;
            color: #000000;
        }}
        
        .dict-table th.center, .dict-table td.center {{
            text-align: center;
        }}
        
        .dict-table td.field-name {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 12.5px;
            font-weight: 500;
        }}
        
        .dict-table td.field-name.pk {{
            font-weight: 700;
        }}
        
        .dict-notes {{
            margin-top: 10px;
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            padding: 10px 14px;
            font-size: 12.5px;
            color: #475569;
            border-radius: 4px;
        }}
        
        /* Print Styles */
        @media print {{
            body {{
                padding: 0;
                background: #ffffff;
            }}
            .container {{
                max-width: 100%;
                box-shadow: none;
                padding: 10px;
            }}
            .no-print-bar {{
                display: none;
            }}
            .data-dict-unit {{
                page-break-after: always;
                margin-bottom: 0;
                padding-top: 15px;
            }}
            .data-dict-unit:last-child {{
                page-break-after: avoid;
            }}
            .dict-container {{
                border: 1.5px solid #000000 !important;
            }}
            .dict-header-box {{
                border-bottom: 1.5px solid #000000 !important;
            }}
            .dict-table th, .dict-table td {{
                border: 1px solid #000000 !important;
            }}
        }}
    </style>
</head>
<body>

<div class="container">
    <div class="no-print-bar">
        <div>
            <strong>SCAS Database Specification</strong> &bull; Section 4.2 Data Dictionary
        </div>
        <div style="display: flex; gap: 12px; align-items: center;">
            <select class="nav-select" onchange="if(this.value) location.hash = this.value;">
                <option value="">Jump to table...</option>
                {"".join([f'<option value="tbl-{t["table_name"]}">Table {t["table_no"]}: {t["table_name"]}</option>' for t in DATA_DICTIONARY_TABLES])}
            </select>
            <button class="btn" onclick="window.print()">
                <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M2.5 8a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1z"/><path d="M5 1a2 2 0 0 0-2 2v2H2a2 2 0 0 0-2 2v3a2 2 0 0 0 2 2h1v1a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-1h1a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-1V3a2 2 0 0 0-2-2H5zM4 3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2H4V3zm1 5a2 2 0 0 0-2 2v1H2a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v-1a2 2 0 0 0-2-2H5zm7 2v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1z"/></svg>
                Print / Save as PDF
            </button>
        </div>
    </div>

    <div class="header">
        <div class="univ-badge">Ganpat University</div>
        <div class="inst-sub">Acharya Motibhai Patel Institute of Computer Studies (AMPICS)</div>
        <h1>Student Central Administrative System (SCAS)</h1>
        <div class="subtitle">Comprehensive Relational Database Architecture & Schema Specification</div>
        <div class="section-badge">Section 4.2 Data Dictionary</div>
    </div>

    <div class="card">
        <h2>1. Design Specification & Standard Demo Format</h2>
        <p>This technical data dictionary documents all core entities comprising the SCAS relational database schema. Each entity is presented in accordance with the formal institutional data dictionary format featuring an integrated metadata box and a detailed attribute constraint grid.</p>
        
        <div style="margin-top: 14px;">
            <div style="font-weight: 700; color: #047857; margin-bottom: 6px; font-size: 13px;">Demo Reference Template:</div>
            <div class="dict-container">
                <div class="dict-header-box">
                    <div class="meta-line"><strong>Table Name:</strong> {DEMO_TABLE['table_name']}</div>
                    <div class="meta-line"><strong>Description:</strong> {DEMO_TABLE['description']}</div>
                    <div class="meta-line"><strong>Constraints:</strong> {DEMO_TABLE['constraints']}</div>
                </div>
                <table class="dict-table">
                    <thead>
                        <tr>
                            <th class="center" style="width: 70px;">Field No.</th>
                            <th style="width: 140px;">Field Name</th>
                            <th class="center" style="width: 90px;">Type</th>
                            <th class="center" style="width: 60px;">Size</th>
                            <th style="width: 220px;">Constraints</th>
                            <th>Description</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join([f'''<tr>
                            <td class="center">{f[0]}</td>
                            <td class="field-name{' pk' if 'id' in f[1] and 'PK' in f[4] else ''}">{f[1]}</td>
                            <td class="center">{f[2]}</td>
                            <td class="center">{f[3]}</td>
                            <td>{f[4]}</td>
                            <td>{f[5]}</td>
                        </tr>''' for f in DEMO_TABLE['fields']])}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <div class="card" style="page-break-after: always;">
        <h2>2. Master Register of System Entities (13 Tables)</h2>
        <p>Master registry of relational entities maintaining data integrity across user authentication, degree courses, academic timetables, examinations, continuous diagnostic evaluations, tuition fee accounting, and leave management:</p>
        <table class="index-table">
            <thead>
                <tr>
                    <th style="width: 80px; text-align: center;">Section</th>
                    <th style="width: 180px;">Table Name</th>
                    <th style="width: 90px;">Primary Key</th>
                    <th>Subsystem Role</th>
                </tr>
            </thead>
            <tbody>
                {"".join([f'''<tr>
                    <td style="text-align: center; font-weight: 600;">{t["table_no"]}</td>
                    <td><a href="#tbl-{t["table_name"]}" style="color: #b91c1c; text-decoration: none; font-family: 'JetBrains Mono', monospace; font-weight: 600;">{t["table_name"]}</a></td>
                    <td><code style="background: #f1f5f9; padding: 2px 6px; border-radius: 3px;">id</code></td>
                    <td>{t["description"]}</td>
                </tr>''' for t in DATA_DICTIONARY_TABLES])}
            </tbody>
        </table>
    </div>

    <!-- 13 INDIVIDUAL DATA DICTIONARY TABLES -->
    {"".join([f'''
    <div class="data-dict-unit" id="tbl-{t["table_name"]}">
        <div class="data-dict-title">
            <span>Table {t["table_no"]}: {t["table_name"]}</span>
            <span style="font-size: 12px; font-weight: 500; color: #64748b;">Engine: InnoDB | Collation: utf8mb4_unicode_ci</span>
        </div>
        <div class="dict-container">
            <div class="dict-header-box">
                <div class="meta-line"><strong>Table Name:</strong> {t["table_name"]}</div>
                <div class="meta-line"><strong>Description:</strong> {t["description"]}</div>
                <div class="meta-line"><strong>Constraints:</strong> {t["constraints"]}</div>
            </div>
            <table class="dict-table">
                <thead>
                    <tr>
                        <th class="center" style="width: 70px;">Field No.</th>
                        <th style="width: 150px;">Field Name</th>
                        <th class="center" style="width: 90px;">Type</th>
                        <th class="center" style="width: 60px;">Size</th>
                        <th style="width: 220px;">Constraints</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join([f"""<tr>
                        <td class="center">{f[0]}</td>
                        <td class="field-name{' pk' if 'id' in f[1] and 'PK' in f[4] else ''}">{f[1]}</td>
                        <td class="center">{f[2]}</td>
                        <td class="center">{f[3]}</td>
                        <td>{f[4]}</td>
                        <td>{f[5]}</td>
                    </tr>""" for f in t["fields"]])}
                </tbody>
            </table>
        </div>
        <div class="dict-notes">
            <strong>Relational Context & Integrity:</strong> Primary key <code>id</code> with auto-increment sequence. Cascading referential integrity enabled across associated child foreign relations (<code>ON DELETE CASCADE</code>).
        </div>
    </div>
    ''' for t in DATA_DICTIONARY_TABLES])}

</div>

</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Interactive HTML Data Dictionary generated at: {output_path}")

if __name__ == '__main__':
    target = r"d:\SCAS-HG-OR\scas-final\SCAS_Data_Dictionary.html"
    generate_html(target)
    
    import shutil
    root_target = r"d:\SCAS-HG-OR\SCAS_Data_Dictionary.html"
    shutil.copyfile(target, root_target)
    print(f"Copied HTML to root directory: {root_target}")

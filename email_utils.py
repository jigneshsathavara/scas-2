import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Path to local log file for sent emails
LOG_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sent_emails.log')

def send_credentials_email(to_email, name, role, username, password, is_reset=False):
    subject = "Smart College Portal - Temporary Password Reset" if is_reset else "Smart College Portal - Account Created"
    
    body = f"""Subject: {subject}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
To: {to_email} ({name})
------------------------------------------------------------
Hello {name},

Your account on the Smart College Analytics System has been {"reset" if is_reset else "created"}.

Here are your portal access credentials:
👉 Portal Role: {role.upper()}
👉 Username / ID: {username}
👉 Temporary Password: {password}

⚠️ IMPORTANT NOTICE: This is a system auto-generated or default password.
For security reasons, you are kindly requested to log in and change your password immediately.

Best regards,
Dean System Administrator
Smart College Portal Support Team
------------------------------------------------------------
"""
    
    # 1. Always write to console in a nice box
    try:
        print("\n" + "="*80)
        print("✉️  MOCK MAIL TRANSPORT ACTIVATED")
        print(body.strip())
        print("="*80 + "\n")
    except UnicodeEncodeError:
        print("\n" + "="*80)
        print("[MOCK MAIL TRANSPORT ACTIVATED]")
        try:
            print(body.strip())
        except UnicodeEncodeError:
            print(body.strip().encode('ascii', 'replace').decode('ascii'))
        print("="*80 + "\n")
    
    # 2. Always append to the sent_emails.log file
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"\n--- MAIL SENT ON {datetime.now()} ---\n")
            f.write(body)
            f.write("="*60 + "\n")
    except Exception as e:
        print(f"Error writing to sent_emails.log: {str(e)}")

    # 3. Attempt real SMTP delivery if config variables are set in environment or Config
    smtp_server = os.environ.get('SMTP_SERVER')
    smtp_port = os.environ.get('SMTP_PORT')
    smtp_user = os.environ.get('SMTP_USER')
    smtp_pass = os.environ.get('SMTP_PASS')
    
    if not smtp_server or not smtp_user or not smtp_pass:
        try:
            from config import Config
            smtp_server = smtp_server or Config.SMTP_SERVER
            smtp_port = smtp_port or Config.SMTP_PORT
            smtp_user = smtp_user or Config.SMTP_USER
            smtp_pass = smtp_pass or Config.SMTP_PASS
        except Exception:
            pass
            
    if smtp_port is None:
        smtp_port = 587
    else:
        smtp_port = int(smtp_port)
        
    if smtp_server and smtp_user and smtp_pass:
        try:
            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, to_email, msg.as_string())
            server.close()
            print(f"SMTP Success: Email sent to {to_email}")
        except Exception as e:
            print(f"SMTP Error: Failed to send real email to {to_email}. Error: {str(e)}")
            # Fail silently so app doesn't crash during offline presentation
            pass
            
    return True

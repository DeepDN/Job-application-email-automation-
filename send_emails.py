import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import time
from datetime import datetime

# Gmail Configuration
GMAIL_EMAIL = "your_email@gmail.com"
GMAIL_APP_PASSWORD = "your_app_password_here"

def load_companies():
    return pd.read_excel('data/companies.xlsx')

def load_template():
    with open('templates/email_template.html', 'r') as f:
        return f.read()

def personalize_email(template, name, company, role):
    return template.replace('{name}', name).replace('{company}', company).replace('{role}', role)

def attach_resume(msg, resume_file):
    resume_path = f'resumes/{resume_file}'
    if os.path.exists(resume_path):
        with open(resume_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {resume_file}')
        msg.attach(part)

def send_email(to_email, subject, html_content, resume_file):
    msg = MIMEMultipart('alternative')
    msg['From'] = GMAIL_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(html_content, 'html'))
    attach_resume(msg, resume_file)
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)
    server.send_message(msg)
    server.quit()

def log_sent_email(name, email, company, role):
    log_data = {
        'Name': [name],
        'Email': [email], 
        'Company': [company],
        'Role': [role],
        'Timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    }
    
    log_file = 'logs/sent_log.csv'
    if os.path.exists(log_file):
        pd.DataFrame(log_data).to_csv(log_file, mode='a', header=False, index=False)
    else:
        pd.DataFrame(log_data).to_csv(log_file, index=False)

def main():
    df = load_companies()
    template = load_template()
    
    for index, row in df.iterrows():
        if row['Status'] == 'Sent':
            continue
            
        try:
            html_content = personalize_email(template, row['Name'], row['Company'], row['Role'])
            subject = f"Application for {row['Role']} Position at {row['Company']}"
            
            send_email(row['Email'], subject, html_content, row['Resume'])
            
            df.at[index, 'Status'] = 'Sent'
            log_sent_email(row['Name'], row['Email'], row['Company'], row['Role'])
            
            print(f"Email sent to {row['Name']} at {row['Company']}")
            time.sleep(12)
            
        except Exception as e:
            print(f"Failed to send email to {row['Name']}: {str(e)}")
    
    df.to_excel('data/companies.xlsx', index=False)
    print("Process completed")

if __name__ == "__main__":
    main()

import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import time
from datetime import datetime

class EmailSender:
    def __init__(self, email, password, template_name='email_template'):
        self.email = email
        self.password = password
        self.template_name = template_name
        self.delay = 2
        self.batch_size = 10
        
    def set_delay(self, delay):
        self.delay = delay
        
    def set_batch_size(self, batch_size):
        self.batch_size = batch_size
        
    def load_template(self):
        template_path = f'templates/{self.template_name}.html'
        if os.path.exists(template_path):
            with open(template_path, 'r') as f:
                return f.read()
        return self.get_default_template()
    
    def get_default_template(self):
        return """
        <html>
        <body>
            <p>Dear {name},</p>
            <p>I hope this email finds you well. I am writing to express my interest in the {role} position at {company}.</p>
            <p>Please find my resume attached for your review.</p>
            <p>Best regards,<br>Your Name</p>
        </body>
        </html>
        """
    
    def personalize_email(self, template, name, company, role):
        return template.replace('{name}', name).replace('{company}', company).replace('{role}', role)
    
    def send_email(self, to_email, subject, html_content, resume_file=None):
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(html_content, 'html'))
        
        if resume_file and os.path.exists(f'resumes/{resume_file}'):
            with open(f'resumes/{resume_file}', "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {resume_file}')
            msg.attach(part)
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.email, self.password)
        server.send_message(msg)
        server.quit()
    
    def send_bulk_emails(self, excel_file):
        df = pd.read_excel(excel_file)
        template = self.load_template()
        results = {'sent': 0, 'failed': 0, 'skipped': 0}
        
        for index, row in df.iterrows():
            if pd.notna(row.get('Status')) and row['Status'] == 'Sent':
                results['skipped'] += 1
                continue
                
            try:
                html_content = self.personalize_email(template, row['Name'], row['Company'], row['Role'])
                subject = f"Application for {row['Role']} Position at {row['Company']}"
                
                self.send_email(row['Email'], subject, html_content, row.get('Resume'))
                
                df.at[index, 'Status'] = str('Sent')
                results['sent'] += 1
                time.sleep(self.delay)
                
            except Exception as e:
                results['failed'] += 1
                print(f"Failed to send to {row['Name']}: {str(e)}")
        
        df.to_excel(excel_file, index=False)
        return results

import json
import os
from datetime import datetime, timedelta
import threading
import time

class EmailScheduler:
    def __init__(self):
        self.schedule_file = 'data/scheduled_emails.json'
        self.running = False
        
    def schedule_email(self, email_data, send_time):
        scheduled_emails = self.load_scheduled_emails()
        
        email_job = {
            'id': str(int(time.time())),
            'email_data': email_data,
            'send_time': send_time.isoformat(),
            'status': 'scheduled'
        }
        
        scheduled_emails.append(email_job)
        self.save_scheduled_emails(scheduled_emails)
        return email_job['id']
    
    def load_scheduled_emails(self):
        if os.path.exists(self.schedule_file):
            with open(self.schedule_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_scheduled_emails(self, emails):
        os.makedirs('data', exist_ok=True)
        with open(self.schedule_file, 'w') as f:
            json.dump(emails, f, indent=2)
    
    def start_scheduler(self, email_sender):
        if self.running:
            return
        
        self.running = True
        def scheduler_loop():
            while self.running:
                self.process_scheduled_emails(email_sender)
                time.sleep(60)  # Check every minute
        
        thread = threading.Thread(target=scheduler_loop, daemon=True)
        thread.start()
    
    def process_scheduled_emails(self, email_sender):
        scheduled_emails = self.load_scheduled_emails()
        now = datetime.now()
        
        for email in scheduled_emails:
            if email['status'] == 'scheduled':
                send_time = datetime.fromisoformat(email['send_time'])
                if now >= send_time:
                    try:
                        data = email['email_data']
                        email_sender.send_email(
                            data['to_email'],
                            data['subject'], 
                            data['content'],
                            data.get('resume_file')
                        )
                        email['status'] = 'sent'
                    except Exception as e:
                        email['status'] = f'failed: {str(e)}'
        
        self.save_scheduled_emails(scheduled_emails)
    
    def get_scheduled_emails(self):
        return self.load_scheduled_emails()

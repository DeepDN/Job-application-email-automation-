from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import os
from datetime import datetime, timedelta
from email_sender import EmailSender
from scheduler import EmailScheduler
from analytics import Analytics
from email_validator import EmailValidator
from template_manager import TemplateManager
from config import Config
from models import db, EmailLog, ScheduledEmail, Company

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Initialize components
scheduler = EmailScheduler()
analytics = Analytics()
validator = EmailValidator()
template_manager = TemplateManager()

# Create tables
try:
    with app.app_context():
        db.create_all()
    print("Database connected successfully")
except Exception as e:
    print(f"Database connection failed: {e}")
    print("Running without database - using file-based storage")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/analytics')
def get_analytics():
    try:
        emails = EmailLog.query.all()
        
        if not emails:
            return jsonify({
                'total_sent': 0,
                'today_sent': 0,
                'week_sent': 0,
                'top_companies': {},
                'template_usage': {},
                'daily_stats': {}
            })
        
        now = datetime.utcnow()
        today = now.date()
        week_ago = now - timedelta(days=7)
        
        total_sent = len(emails)
        today_sent = sum(1 for e in emails if e.sent_at.date() == today)
        week_sent = sum(1 for e in emails if e.sent_at >= week_ago)
        
        # Top companies
        company_counts = {}
        for e in emails:
            company_counts[e.company] = company_counts.get(e.company, 0) + 1
        top_companies = dict(sorted(company_counts.items(), key=lambda x: x[1], reverse=True)[:5])
        
        # Template usage
        template_counts = {}
        for e in emails:
            template_counts[e.template_used] = template_counts.get(e.template_used, 0) + 1
        
        # Daily stats
        daily_counts = {}
        for e in emails:
            date_str = e.sent_at.strftime('%Y-%m-%d')
            daily_counts[date_str] = daily_counts.get(date_str, 0) + 1
        
        return jsonify({
            'total_sent': total_sent,
            'today_sent': today_sent,
            'week_sent': week_sent,
            'top_companies': top_companies,
            'template_usage': template_counts,
            'daily_stats': daily_counts
        })
    except Exception as e:
        print(f"Analytics error: {str(e)}")
        return jsonify({
            'total_sent': 0,
            'today_sent': 0,
            'week_sent': 0,
            'top_companies': {},
            'template_usage': {},
            'daily_stats': {}
        })

@app.route('/api/templates')
def get_templates():
    return jsonify(template_manager.get_available_templates())

@app.route('/api/validate-emails', methods=['POST'])
def validate_emails():
    data = request.json
    emails = data.get('emails', [])
    results = validator.validate_bulk(emails)
    return jsonify(results)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and file.filename.endswith('.xlsx'):
        filepath = os.path.join('uploads', file.filename)
        file.save(filepath)
        
        # Validate emails in uploaded file
        try:
            df = pd.read_excel(filepath)
            if 'Email' in df.columns:
                emails = df['Email'].tolist()
                validation_results = validator.validate_bulk(emails)
                invalid_count = sum(1 for r in validation_results if not r['valid'])
                
                return jsonify({
                    'message': 'File uploaded successfully',
                    'filename': file.filename,
                    'total_emails': len(emails),
                    'invalid_emails': invalid_count
                })
        except Exception as e:
            return jsonify({'error': f'Error processing file: {str(e)}'}), 400
    
    return jsonify({'error': 'Invalid file format'}), 400

@app.route('/send-emails', methods=['POST'])
def send_emails():
    data = request.json
    email = data.get('email') or os.environ.get('GMAIL_EMAIL')
    password = data.get('password') or os.environ.get('GMAIL_APP_PASSWORD')
    filename = data.get('filename')
    template = data.get('template', 'email_template')
    schedule_time = data.get('schedule_time')
    delay = int(data.get('delay', 5))
    batch_size = int(data.get('batch_size', 10))
    
    if not all([email, password, filename]):
        return jsonify({'error': 'Missing Gmail credentials or filename. Set in form or .env file'}), 400
    
    try:
        sender = EmailSender(email, password, template)
        if hasattr(sender, 'set_delay'):
            sender.set_delay(delay)
        if hasattr(sender, 'set_batch_size'):
            sender.set_batch_size(batch_size)
        
        if schedule_time:
            send_time = datetime.fromisoformat(schedule_time)
            job_id = scheduler.schedule_email({
                'filename': filename,
                'template': template,
                'delay': delay,
                'batch_size': batch_size
            }, send_time)
            return jsonify({'message': f'Emails scheduled for {send_time}', 'job_id': job_id})
        else:
            # Pass app to sender for database context
            sender.app = app
            result = sender.send_bulk_emails(f'uploads/{filename}')
            if not isinstance(result, dict):
                result = {'sent': 0, 'failed': 0, 'skipped': 0}
            result.setdefault('sent', 0)
            result.setdefault('failed', 0) 
            result.setdefault('skipped', 0)
            return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/scheduled-emails')
def get_scheduled_emails():
    return jsonify(scheduler.get_scheduled_emails())

@app.route('/template')
def download_template():
    template_path = 'static/template.xlsx'
    if not os.path.exists(template_path):
        # Create template if it doesn't exist
        data = {
            'Name': ['John Smith', 'Sarah Johnson'],
            'Email': ['john@company.com', 'sarah@startup.io'],
            'Company': ['TechCorp', 'StartupIO'],
            'Role': ['Software Engineer', 'Frontend Developer'],
            'Resume': ['resume_software.pdf', 'resume_frontend.pdf'],
            'Status': ['', '']
        }
        df = pd.DataFrame(data)
        os.makedirs('static', exist_ok=True)
        df.to_excel(template_path, index=False)
    
    return send_file(template_path, as_attachment=True)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    sender = EmailSender('', '')
    scheduler.start_scheduler(sender)
    app.run(debug=True, host='0.0.0.0', port=5000)

from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import os
from datetime import datetime, timedelta
from email_sender import EmailSender
from scheduler import EmailScheduler
from analytics import Analytics
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize components
scheduler = EmailScheduler()
analytics = Analytics()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/analytics')
def get_analytics():
    return jsonify(analytics.get_dashboard_data())

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
        return jsonify({'message': 'File uploaded successfully', 'filename': file.filename})
    
    return jsonify({'error': 'Invalid file format'}), 400

@app.route('/send-emails', methods=['POST'])
def send_emails():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    filename = data.get('filename')
    template = data.get('template', 'email_template')
    schedule_time = data.get('schedule_time')
    
    if not all([email, password, filename]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        sender = EmailSender(email, password, template)
        
        if schedule_time:
            send_time = datetime.fromisoformat(schedule_time)
            job_id = scheduler.schedule_email({
                'filename': filename,
                'template': template
            }, send_time)
            return jsonify({'message': f'Emails scheduled for {send_time}', 'job_id': job_id})
        else:
            result = sender.send_bulk_emails(f'uploads/{filename}')
            return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/scheduled-emails')
def get_scheduled_emails():
    return jsonify(scheduler.get_scheduled_emails())

@app.route('/template')
def download_template():
    return send_file('static/template.xlsx', as_attachment=True)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    sender = EmailSender('', '')  # Dummy sender for scheduler
    scheduler.start_scheduler(sender)
    app.run(debug=True, host='0.0.0.0', port=5000)

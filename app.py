from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import os
from email_sender import EmailSender
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    return render_template('index.html')

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
    
    if not all([email, password, filename]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        sender = EmailSender(email, password)
        result = sender.send_bulk_emails(f'uploads/{filename}')
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/template')
def download_template():
    return send_file('static/template.xlsx', as_attachment=True)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)

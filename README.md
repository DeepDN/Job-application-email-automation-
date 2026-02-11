# Job Application Email Automation System

## Prerequisites
- Python 3.8 or higher
- Gmail account with 2-Factor Authentication enabled
- Internet connection

## Step 1: Gmail App Password Setup
1. Go to https://myaccount.google.com/
2. Click **Security** → **2-Step Verification** (enable if not already enabled)
3. Go back to **Security** → **App passwords**
4. Select **Mail** from dropdown
5. Click **Generate**
6. Copy the 16-character password (save it securely)

## Step 2: Project Setup
```bash
# Navigate to project directory
cd job_automation

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Configuration
Edit `send_emails.py` and update these lines:
```python
GMAIL_EMAIL = "your_actual_email@gmail.com"
GMAIL_APP_PASSWORD = "your_16_character_app_password"
```

## Step 4: Prepare Your Data

### Add Resume Files
Place your PDF resume files in `resumes/` folder:
- `resume_devops.pdf`
- `resume_network.pdf`
- `resume_frontend.pdf` (add as needed)

### Update Company Data
Edit `data/companies.xlsx` with your target companies:

| Name | Email | Company | Role | Resume | Status |
|------|-------|---------|------|--------|--------|
| John Smith | john@company.com | TechCorp | DevOps Engineer | resume_devops.pdf | |
| Sarah Lee | sarah@startup.io | StartupIO | Frontend Developer | resume_frontend.pdf | |

**Required Columns:**
- **Name**: Recruiter/HR name
- **Email**: Contact email address
- **Company**: Company name
- **Role**: Job position title
- **Resume**: Resume filename (must exist in resumes/ folder)
- **Status**: Leave empty (will be updated to "Sent" automatically)

### Customize Email Template
Edit `templates/email_template.html` to personalize your message and update signature with your details.

## Step 5: Run the System
```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Run the automation
python send_emails.py
```

## What Happens When You Run
1. Reads Excel file and skips rows with Status = "Sent"
2. For each new row:
   - Personalizes email template with company/role details
   - Attaches specified resume file
   - Sends email via Gmail SMTP
   - Updates Status to "Sent" in Excel
   - Logs email details with timestamp to `logs/sent_log.csv`
   - Waits 12 seconds before next email

## File Structure
```
job_automation/
├── data/
│   └── companies.xlsx          # Company and recruiter details
├── resumes/
│   ├── resume_devops.pdf       # Your resume files
│   └── resume_network.pdf
├── templates/
│   └── email_template.html     # HTML email template
├── logs/
│   └── sent_log.csv           # Email sending log (auto-created)
├── venv/                      # Virtual environment
├── send_emails.py             # Main automation script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Troubleshooting

### Common Issues
- **"Authentication failed"**: Check Gmail App Password is correct
- **"File not found"**: Ensure resume file exists in resumes/ folder
- **"Permission denied"**: Make sure Excel file is not open in another program

### Safety Features
- Automatically skips already sent emails
- 12-second delay prevents Gmail rate limiting
- All sent emails are logged with timestamps
- Excel file is updated after each successful send

## Commands Reference
```bash
# Setup (one-time)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Daily usage
source venv/bin/activate
python send_emails.py

# Deactivate virtual environment
deactivate
```

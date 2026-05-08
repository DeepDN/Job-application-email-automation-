# Job Application Email Automation

[![Deploy to GitHub Pages](https://github.com/DeepDN/Job-application-email-automation-/actions/workflows/deploy.yml/badge.svg)](https://github.com/DeepDN/Job-application-email-automation-/actions/workflows/deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A free, open-source tool to automate your job application emails with personalization and resume attachments.Completely free for everyone.

![Homepage of the application](Images/image.png)

![Email Analysis Dashboard](Images/image-1.png)

![Sample template example](Images/image-3.png)


## Features

- **Bulk Email Sending** - Send personalized emails to multiple recruiters
- **Resume Attachments** - Automatically attach different resumes based on job type
- **Smart Personalization** - Customize emails with company and role details
- **Excel Integration** - Manage contacts via simple Excel spreadsheet
- **Status Tracking** - Avoid duplicate emails with automatic status updates
- **Email Logging** - Keep track of all sent emails with timestamps
- **Rate Limiting** - Built-in delays to prevent spam detection
- **Web Interface** - Easy-to-use web interface with Three.js animations
- **Email Scheduling** - Schedule emails for optimal timing
- **Analytics Dashboard** - Track performance with interactive charts
- **Email Validation** - Validate email addresses before sending    
- **Multiple Templates** - Professional, Casual, Formal, and Creative templates

## Quick Start

### Option 1: Web Interface (Recommended)

Visit our hosted version: **[Job Email Automation](https://deepdn.github.io/Job-application-email-automation-/)**

![Github Action Page](Images/image-2.png)

### Option 2: Docker (Recommended for Production)

```bash
# Clone the repository
git clone https://github.com/DeepDN/Job-application-email-automation-.git
cd Job-application-email-automation-

# Configure environment variables
cp .env.example .env
# Edit .env file with your credentials

# Run with Docker Compose
docker-compose up -d

# Access the application
# Visit http://localhost:5000
```

### Option 3: Local Installation

```bash
# Clone the repository
git clone https://github.com/DeepDN/Job-application-email-automation-.git
cd Job-application-email-automation-

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env file and set your SECRET_KEY

# Run web interface
python app.py
```

Visit `http://localhost:5000` in your browser.

### Option 4: Command Line (Original)

```bash
# Setup (same as Option 3)
# Edit send_emails.py with your credentials
python send_emails.py
```

##  Setup Instructions

### 1. Gmail App Password Setup

1. Enable 2-Factor Authentication on your Gmail account
2. Go to [Google Account Settings](https://myaccount.google.com/u/1/apppasswords?rapt=AEjHL4OZ3TgdDpLpdMqhjqTgT5vx3CG4F-dLMHAx75yEyUW_9ORN_fo28z7hqZ2xh0HNTptKVQZmNzkgzhumM5qraJnH8-ruBS5jHvx_vHD3oN79ue3mfas)
3. Generate a new app password for "Mail"
4. Save the 16-character password securely
 

### 2. Prepare Your Data

#### Excel File Format
Create an Excel file with these columns:

| Name | Email | Company | Role | Resume | Status |
|------|-------|---------|------|--------|--------|
| John Smith | john@company.com | TechCorp | DevOps Engineer | resume_devops.pdf | |
| Sarah Lee | sarah@startup.io | StartupIO | Frontend Developer | resume_frontend.pdf | |

**Required Columns:**
- **Name**: Recruiter/HR contact name
- **Email**: Contact email address  
- **Company**: Company name
- **Role**: Job position title
- **Resume**: Resume filename (must exist in `resumes/` folder)
- **Status**: Leave empty (auto-updated to "Sent")

#### Resume Files
Place your PDF resumes in the `resumes/` folder:
```
resumes/
├── resume_devops.pdf
├── resume_frontend.pdf
└── resume_data_science.pdf
```

#### Email Template
Customize `templates/email_template.html` with your personal message.

##  Deployment Options

### Docker Deployment (Recommended)

#### Prerequisites
- Docker and Docker Compose installed
- Git installed

#### Quick Setup
```bash
# Clone repository
git clone https://github.com/DeepDN/Job-application-email-automation-.git
cd Job-application-email-automation-

# Configure environment
cp .env.example .env
nano .env  # Edit with your settings

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### Environment Variables for Docker
Edit `.env` file before running:
```bash
SECRET_KEY=your-super-secret-key-here
GMAIL_EMAIL=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-character-app-password
DATABASE_URL=postgresql://jobapp:password@db:5432/jobapp_db
```

#### Docker Commands
```bash
# Build and start
docker-compose up --build -d

# View application logs
docker-compose logs app

# View database logs
docker-compose logs db

# Access database
docker-compose exec db psql -U jobapp -d jobapp_db

# Backup database
docker-compose exec db pg_dump -U jobapp jobapp_db > backup.sql

# Restore database
docker-compose exec -T db psql -U jobapp jobapp_db < backup.sql

# Update application
git pull
docker-compose up --build -d
```

#### Persistent Data
The following directories are mounted as volumes:
- `./uploads` - Uploaded Excel files
- `./resumes` - Resume PDF files  
- `./logs` - Application logs
- `postgres_data` - Database data (Docker volume)

### GitHub Pages (Free Hosting)

1. Fork this repository
2. Enable GitHub Pages in repository settings
3. GitHub Actions will automatically deploy your site
4. Access at `https://yourusername.github.io/Job-application-email-automation-/`

### Heroku (Free Tier)

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main
```

### Railway/Render (Free Tier)

1. Connect your GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `python app.py`
4. Deploy automatically

##  Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Edit the .env file with your preferred editor
nano .env
```

Required variables:
```
SECRET_KEY=your-super-secret-key-change-this-in-production
```

### Local Configuration

Edit `config.py` for local settings:

```python
class Config:
    SECRET_KEY = 'your-secret-key'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
```

##  Project Structure

```
Job-application-email-automation-/
├── app.py                     # Flask web application
├── email_sender.py           # Email sending logic
├── config.py                 # Configuration settings
├── send_emails.py           # Original CLI script
├── build_static.py          # Static site generator
├── requirements.txt         # Python dependencies
├── templates/
│   ├── index.html          # Web interface
│   └── email_template.html # Email template
├── static/
│   └── template.xlsx       # Excel template download
├── resumes/                # Your resume files
├── data/                   # Excel data files
├── logs/                   # Email logs
├── uploads/                # Uploaded files (web)
└── .github/
    └── workflows/
        └── deploy.yml      # GitHub Actions
```

##  Security & Privacy

- **No Data Storage**: Your emails and passwords are never stored
- **Local Processing**: All email sending happens from your machine
- **Open Source**: Full transparency - review the code yourself
- **Rate Limited**: Built-in delays prevent spam detection
- **Gmail App Passwords**: Secure authentication method

##  Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/Job-application-email-automation-.git
cd Job-application-email-automation-

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt

# Run tests (if available)
python -m pytest

# Run locally
python3 app.py
```

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Acknowledgments

- Inspired by [JobCopilot](https://jobcopilot.com/)
- Built for the job-seeking community
- Made with ❤️ for everyone who can't afford premium tools

##  Support

-  **Bug Reports**: [Open an issue](https://github.com/DeepDN/Job-application-email-automation-/issues)
-  **Feature Requests**: [Start a discussion](https://github.com/DeepDN/Job-application-email-automation-/discussions)
-  **Email**: Create an issue for support

## ⭐ Star History

If this project helped you land a job, please consider giving it a star! ⭐

---

**Made with love for job seekers worldwide by Deepak Nemade (DN) Good luck with your applications!**

# Deployment Guide

## GitHub Pages Deployment (Free)

### Step 1: Repository Setup
1. Push your code to GitHub
2. Go to repository Settings
3. Navigate to Pages section
4. Select "GitHub Actions" as source

### Step 2: Enable GitHub Actions
The workflow is already configured in `.github/workflows/deploy.yml`

### Step 3: Access Your Site
Your site will be available at: `https://yourusername.github.io/Job-application-email-automation-/`

## Alternative Deployment Options

### Heroku (Free Tier)
```bash
# Install Heroku CLI
npm install -g heroku

# Login
heroku login

# Create app
heroku create your-app-name

# Add Procfile
echo "web: python app.py" > Procfile

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### Railway
1. Connect GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `python app.py`
4. Deploy

### Render
1. Connect GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `python app.py`
4. Deploy

## Local Development
```bash
# Clone repository
git clone https://github.com/yourusername/Job-application-email-automation-.git
cd Job-application-email-automation-

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

## Environment Variables
For production deployments, set:
- `SECRET_KEY`: Random secret key for Flask sessions

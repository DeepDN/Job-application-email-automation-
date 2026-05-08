import os
import shutil

def create_static_site():
    # Create build directory
    if os.path.exists('build'):
        shutil.rmtree('build')
    os.makedirs('build', exist_ok=True)
    
    # Create static HTML
    static_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Application Email Automation</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <h1 class="text-center mb-4">Job Application Email Automation</h1>
                <p class="text-center text-muted">Free, open-source tool to automate your job application emails</p>
                
                <div class="alert alert-info">
                    <h5>Get Started:</h5>
                    <ol>
                        <li>Clone the repository: <code>git clone https://github.com/DeepDN/Job-application-email-automation-.git</code></li>
                        <li>Install dependencies: <code>pip install -r requirements.txt</code></li>
                        <li>Run locally: <code>python app.py</code></li>
                        <li>Visit <code>http://localhost:5000</code></li>
                    </ol>
                </div>
                
                <div class="card">
                    <div class="card-body">
                        <h5>Features:</h5>
                        <ul>
                            <li>Bulk email sending with personalization</li>
                            <li>Resume attachment support</li>
                            <li>Multiple email templates (Professional, Casual, Formal, Creative)</li>
                            <li>Email scheduling system</li>
                            <li>Analytics dashboard with charts</li>
                            <li>Excel-based contact management</li>
                            <li>Email tracking and logging</li>
                            <li>Rate limiting to prevent spam</li>
                            <li>Completely free and open source</li>
                        </ul>
                        
                        <div class="text-center mt-4">
                            <a href="https://github.com/DeepDN/Job-application-email-automation-" class="btn btn-primary btn-lg me-2">
                                Download & Run Locally
                            </a>
                            <a href="https://github.com/DeepDN/Job-application-email-automation-/releases" class="btn btn-outline-secondary">
                                Releases
                            </a>
                        </div>
                    </div>
                </div>
                
                <div class="mt-4 text-center">
                    <p class="text-muted">
                        <a href="https://github.com/DeepDN/Job-application-email-automation-" target="_blank">Star on GitHub</a> | 
                        Made with love for job seekers worldwide
                    </p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    # Write static HTML
    with open('build/index.html', 'w') as f:
        f.write(static_html)
    
    # Copy static assets if they exist
    if os.path.exists('static'):
        shutil.copytree('static', 'build/static', dirs_exist_ok=True)
    
    print("Static site built successfully!")

if __name__ == "__main__":
    create_static_site()

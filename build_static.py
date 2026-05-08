import os
import shutil
from jinja2 import Template

def create_static_site():
    # Create build directory
    os.makedirs('build', exist_ok=True)
    
    # Read the template
    with open('templates/index.html', 'r') as f:
        template_content = f.read()
    
    # Create static version with client-side processing
    static_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Application Email Automation</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
</head>
<body>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <h1 class="text-center mb-4">Job Application Email Automation</h1>
                <p class="text-center text-muted">Free, open-source tool to automate your job application emails</p>
                
                <div class="alert alert-info">
                    <h5>How to use:</h5>
                    <ol>
                        <li>Download the desktop application from <a href="https://github.com/DeepDN/Job-application-email-automation-/releases">GitHub Releases</a></li>
                        <li>Or clone the repository and run locally</li>
                        <li>Follow the setup instructions in README.md</li>
                    </ol>
                </div>
                
                <div class="card">
                    <div class="card-body">
                        <h5>Features:</h5>
                        <ul>
                            <li>✅ Bulk email sending with personalization</li>
                            <li>✅ Resume attachment support</li>
                            <li>✅ Excel-based contact management</li>
                            <li>✅ Email tracking and logging</li>
                            <li>✅ Rate limiting to prevent spam</li>
                            <li>✅ Free and open source</li>
                        </ul>
                        
                        <div class="text-center mt-4">
                            <a href="https://github.com/DeepDN/Job-application-email-automation-" class="btn btn-primary btn-lg">
                                Get Started on GitHub
                            </a>
                        </div>
                    </div>
                </div>
                
                <div class="mt-4 text-center">
                    <p class="text-muted">
                        <a href="https://github.com/DeepDN/Job-application-email-automation-" target="_blank">
                            View on GitHub
                        </a> | 
                        Made with ❤️ for job seekers
                    </p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
    """
    
    # Write static HTML
    with open('build/index.html', 'w') as f:
        f.write(static_html)
    
    # Copy static assets
    if os.path.exists('static'):
        shutil.copytree('static', 'build/static', dirs_exist_ok=True)
    
    print("Static site built successfully!")

if __name__ == "__main__":
    create_static_site()

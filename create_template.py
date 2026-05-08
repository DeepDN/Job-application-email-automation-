import pandas as pd
import os

# Create static directory if it doesn't exist
os.makedirs('static', exist_ok=True)

# Create sample template data
data = {
    'Name': ['John Smith', 'Sarah Johnson', 'Mike Chen'],
    'Email': ['john@techcorp.com', 'sarah@startup.io', 'mike@company.net'],
    'Company': ['TechCorp', 'StartupIO', 'InnovateCo'],
    'Role': ['Software Engineer', 'Frontend Developer', 'Data Scientist'],
    'Resume': ['resume_software.pdf', 'resume_frontend.pdf', 'resume_data.pdf'],
    'Status': ['', '', '']
}

# Create DataFrame and save as Excel
df = pd.DataFrame(data)
df.to_excel('static/template.xlsx', index=False)

print("Template created successfully!")

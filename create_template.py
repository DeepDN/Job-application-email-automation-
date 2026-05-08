import pandas as pd

# Create sample template
data = {
    'Name': ['John Smith', 'Sarah Johnson'],
    'Email': ['john@company.com', 'sarah@startup.io'],
    'Company': ['TechCorp', 'StartupIO'],
    'Role': ['DevOps Engineer', 'Frontend Developer'],
    'Resume': ['resume_devops.pdf', 'resume_frontend.pdf'],
    'Status': ['', '']
}

df = pd.DataFrame(data)
df.to_excel('static/template.xlsx', index=False)
print("Template created successfully!")

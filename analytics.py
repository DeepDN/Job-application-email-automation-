import pandas as pd
import json
import os
from datetime import datetime, timedelta

class Analytics:
    def __init__(self):
        self.analytics_file = 'data/analytics.json'
        
    def log_email_sent(self, company, role, template_used):
        data = self.load_analytics()
        
        entry = {
            'timestamp': datetime.now().isoformat(),
            'company': company,
            'role': role,
            'template': template_used,
            'status': 'sent'
        }
        
        data['emails'].append(entry)
        self.save_analytics(data)
    
    def load_analytics(self):
        if os.path.exists(self.analytics_file):
            with open(self.analytics_file, 'r') as f:
                return json.load(f)
        return {'emails': [], 'responses': []}
    
    def save_analytics(self, data):
        os.makedirs('data', exist_ok=True)
        with open(self.analytics_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_dashboard_data(self):
        data = self.load_analytics()
        emails = data['emails']
        
        if not emails:
            return {
                'total_sent': 0,
                'today_sent': 0,
                'week_sent': 0,
                'top_companies': [],
                'template_usage': {},
                'daily_stats': []
            }
        
        df = pd.DataFrame(emails)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        now = datetime.now()
        today = now.date()
        week_ago = now - timedelta(days=7)
        
        return {
            'total_sent': len(emails),
            'today_sent': len(df[df['timestamp'].dt.date == today]),
            'week_sent': len(df[df['timestamp'] >= week_ago]),
            'top_companies': df['company'].value_counts().head(5).to_dict(),
            'template_usage': df['template'].value_counts().to_dict(),
            'daily_stats': df.groupby(df['timestamp'].dt.date).size().tail(7).to_dict()
        }

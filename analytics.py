import pandas as pd
import json
import os
from datetime import datetime, timedelta

class Analytics:
    def __init__(self):
        self.analytics_file = 'data/analytics.json'
        
    def get_dashboard_data(self):
        try:
            from models import db, EmailLog
            from flask import current_app
            
            with current_app.app_context():
                emails = EmailLog.query.all()
                
                if not emails:
                    return self._empty_dashboard()
                
                now = datetime.utcnow()
                today = now.date()
                week_ago = now - timedelta(days=7)
                
                total_sent = len(emails)
                today_sent = sum(1 for e in emails if e.sent_at.date() == today)
                week_sent = sum(1 for e in emails if e.sent_at >= week_ago)
                
                # Top companies
                company_counts = {}
                for e in emails:
                    company_counts[e.company] = company_counts.get(e.company, 0) + 1
                top_companies = dict(sorted(company_counts.items(), key=lambda x: x[1], reverse=True)[:5])
                
                # Template usage
                template_counts = {}
                for e in emails:
                    template_counts[e.template_used] = template_counts.get(e.template_used, 0) + 1
                
                # Daily stats
                daily_counts = {}
                for e in emails:
                    date_str = e.sent_at.strftime('%Y-%m-%d')
                    daily_counts[date_str] = daily_counts.get(date_str, 0) + 1
                
                return {
                    'total_sent': total_sent,
                    'today_sent': today_sent,
                    'week_sent': week_sent,
                    'top_companies': top_companies,
                    'template_usage': template_counts,
                    'daily_stats': daily_counts
                }
        except Exception as e:
            print(f"Database analytics failed: {str(e)}")
            return self._empty_dashboard()
    
    def _empty_dashboard(self):
        return {
            'total_sent': 0,
            'today_sent': 0,
            'week_sent': 0,
            'top_companies': {},
            'template_usage': {},
            'daily_stats': {}
        }

import re
import dns.resolver
import smtplib
from email.mime.text import MIMEText

class EmailValidator:
    def __init__(self):
        self.email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    def validate_format(self, email):
        return bool(self.email_regex.match(email))
    
    def validate_domain(self, email):
        try:
            domain = email.split('@')[1]
            dns.resolver.resolve(domain, 'MX')
            return True
        except:
            return False
    
    def validate_bulk(self, emails):
        results = []
        for email in emails:
            result = {
                'email': email,
                'valid_format': self.validate_format(email),
                'valid_domain': self.validate_domain(email)
            }
            result['valid'] = result['valid_format'] and result['valid_domain']
            results.append(result)
        return results

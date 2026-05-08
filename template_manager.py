import os
import json

class TemplateManager:
    def __init__(self):
        self.templates_dir = 'templates'
        self.custom_templates_file = 'data/custom_templates.json'
    
    def get_available_templates(self):
        templates = []
        for file in os.listdir(self.templates_dir):
            if file.endswith('_template.html'):
                name = file.replace('_template.html', '').replace('_', ' ').title()
                templates.append({
                    'id': file.replace('.html', ''),
                    'name': name,
                    'type': 'built-in'
                })
        
        # Add custom templates
        custom_templates = self.load_custom_templates()
        for template in custom_templates:
            templates.append({
                'id': template['id'],
                'name': template['name'],
                'type': 'custom'
            })
        
        return templates
    
    def load_custom_templates(self):
        if os.path.exists(self.custom_templates_file):
            with open(self.custom_templates_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_custom_template(self, name, content):
        custom_templates = self.load_custom_templates()
        template_id = name.lower().replace(' ', '_')
        
        template = {
            'id': template_id,
            'name': name,
            'content': content
        }
        
        # Update existing or add new
        existing = next((t for t in custom_templates if t['id'] == template_id), None)
        if existing:
            existing.update(template)
        else:
            custom_templates.append(template)
        
        os.makedirs('data', exist_ok=True)
        with open(self.custom_templates_file, 'w') as f:
            json.dump(custom_templates, f, indent=2)
        
        return template_id
    
    def get_template_content(self, template_id):
        # Check built-in templates
        template_path = f'{self.templates_dir}/{template_id}.html'
        if os.path.exists(template_path):
            with open(template_path, 'r') as f:
                return f.read()
        
        # Check custom templates
        custom_templates = self.load_custom_templates()
        template = next((t for t in custom_templates if t['id'] == template_id), None)
        if template:
            return template['content']
        
        return None

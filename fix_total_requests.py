#!/usr/bin/env python3
import json

# Read the dashboard
with open('monitoring/grafana/dashboards/django-requests-dashboard.json', 'r') as f:
    dashboard = json.load(f)

# Find and update the Total Requests panel (ID 8)
for panel in dashboard['panels']:
    if panel.get('id') == 8:
        print(f"Found Total Requests panel: {panel['title']}")
        print(f"Current position: {panel['gridPos']}")
        print(f"Current query: {panel['targets'][0]['expr']}")
        
        # Update to position it clearly (first row, position 5)
        panel['gridPos'] = {'h': 5, 'w': 4, 'x': 20, 'y': 0}
        
        # Ensure it uses the correct metric and displays well
        panel['fieldConfig']['defaults']['custom'] = {'hideFrom': {'tooltip': False, 'viz': False, 'legend': False}}
        panel['options']['reduceOptions']['values'] = True
        panel['options']['reduceOptions']['calcs'] = ['lastNotNull']
        
        print(f"Updated position to: {panel['gridPos']}")
        print("✅ Total Requests panel fixed!")
        break

# Write back
with open('monitoring/grafana/dashboards/django-requests-dashboard.json', 'w') as f:
    json.dump(dashboard, f, indent=2)

print("Dashboard updated successfully!")

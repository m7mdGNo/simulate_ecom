#!/usr/bin/env python3
import json

# Read the dashboard
with open('monitoring/grafana/dashboards/django-requests-dashboard.json', 'r') as f:
    dashboard = json.load(f)

panels = dashboard['panels']

# Separate stat panels and chart panels
stat_panels = [p for p in panels if p['type'] == 'stat']
chart_panels = [p for p in panels if p['type'] != 'stat']

print(f"Stat panels: {len(stat_panels)}")
print(f"Chart panels: {len(chart_panels)}")

# Sort by panel ID to maintain order
stat_panels.sort(key=lambda x: x['id'])
chart_panels.sort(key=lambda x: x['id'])

# Reorganize stats: 6 per row, width=4, height=5
new_y = 0
row_position = 0

for panel in stat_panels:
    x = (row_position % 6) * 4  # 6 cards per row (6*4=24)
    panel['gridPos'] = {'h': 5, 'w': 4, 'x': x, 'y': new_y}
    row_position += 1
    if row_position % 6 == 0:
        new_y += 5

# Reorganize charts: after stats
chart_y = new_y

# Arrange charts: timeseries full width, pie charts side by side
for i, panel in enumerate(chart_panels):
    if panel['type'] == 'timeseries':
        # Full width for timeseries
        panel['gridPos'] = {'h': 7, 'w': 24, 'x': 0, 'y': chart_y}
        chart_y += 7
    else:
        # Side by side for pie/bar charts
        x = (i % 2) * 12
        panel['gridPos'] = {'h': 8, 'w': 12, 'x': x, 'y': chart_y}
        if (i + 1) % 2 == 0:
            chart_y += 8

# Write back
with open('monitoring/grafana/dashboards/django-requests-dashboard.json', 'w') as f:
    json.dump(dashboard, f, indent=2)

print("\nReorganized layout:")
print(f"Total stat rows: {(len(stat_panels) + 5) // 6}")
print(f"Stats end at y: {new_y}")
print(f"Charts start at y: {chart_y - sum(p['gridPos']['h'] for p in chart_panels)}")
print("✅ Dashboard reorganized successfully!")

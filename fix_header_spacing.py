#!/usr/bin/env python3
"""
Fix header spacing - remove gap from top
"""

import os
import re
from pathlib import Path

def fix_header_spacing(file_path):
    """Add CSS to remove header top spacing"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Add CSS to remove header spacing
        header_fix_css = '''
<style>
/* Fix header spacing - aggressive approach */
html {
    margin: 0 !important;
    padding: 0 !important;
}

body {
    margin: 0 !important;
    padding: 0 !important;
    margin-top: 0 !important;
    padding-top: 0 !important;
}

body::before,
body::after {
    display: none !important;
}

header.fl-builder-content,
header[role="banner"] {
    margin: 0 !important;
    padding-top: 0 !important;
    margin-top: 0 !important;
    top: 0 !important;
}

.fl-builder-content {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

.fl-row:first-child,
.CustomHeaderRow,
.CustomHeader-parentRow {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

.fl-page-header-wrap,
.fl-page-header {
    margin-top: 0 !important;
    padding-top: 0 !important;
}
</style>
'''
        
        # Insert CSS before </head> if not already present
        if '</head>' in content and 'Fix header spacing' not in content:
            content = content.replace('</head>', f'{header_fix_css}\n</head>')
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# Fix both pages
html_files = [
    'PumaPulse.rocks/case-studies/index.html',
    'PumaPulse.rocks/resources/index.html',
]

print("🔧 FIXING HEADER SPACING...\n")

for html_file in html_files:
    if Path(html_file).exists():
        if fix_header_spacing(html_file):
            print(f"✓ Fixed: {html_file}")

print("\n✅ HEADER SPACING FIXED!")
print("No more gap at the top.")

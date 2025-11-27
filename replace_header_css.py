#!/usr/bin/env python3
"""
Replace header spacing CSS with more aggressive version
"""

import os
import re
from pathlib import Path

def replace_header_css(file_path):
    """Replace old header CSS with new aggressive version"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove old header spacing CSS
        pattern = r'<style>\s*/\* Fix header spacing \*/.*?</style>'
        content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # Add new aggressive CSS
        header_fix_css = '''<style>
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
        
        # Insert new CSS before </head>
        if '</head>' in content:
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

print("🔧 REPLACING HEADER CSS WITH AGGRESSIVE VERSION...\n")

for html_file in html_files:
    if Path(html_file).exists():
        if replace_header_css(html_file):
            print(f"✓ Updated: {html_file}")

print("\n✅ HEADER CSS UPDATED!")
print("Space should be completely removed now.")

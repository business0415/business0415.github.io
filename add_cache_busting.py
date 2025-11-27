#!/usr/bin/env python3
"""
Add cache-busting meta tags to force browsers to reload
"""

import os
from pathlib import Path

CACHE_BUST_META = '''<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
'''

def add_cache_busting(file_path):
    """Add cache-busting meta tags"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already has cache busting
        if 'no-cache, no-store, must-revalidate' in content:
            return False
        
        # Add after <head> tag
        if '<head>' in content:
            content = content.replace('<head>', f'<head>\n{CACHE_BUST_META}', 1)
            
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# Fix priority pages
priority_files = [
    'PumaPulse.rocks/case-studies/index.html',
    'PumaPulse.rocks/resources/index.html',
]

print("Adding cache-busting meta tags...\n")
for file_path in priority_files:
    if Path(file_path).exists():
        if add_cache_busting(file_path):
            print(f"✓ Added to: {file_path}")

print("\n✅ Done! These pages will now force browsers to reload.")
